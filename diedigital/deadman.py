"""Ölü adam anahtarı.

İki tetikleme biçimi var (ikisi birlikte de kullanılabilir, hangisi önce gelirse):
  - checkin_interval_days: bu kadar gün check-in yapmazsan,
  - trigger_at: belirli bir tarihte.
Tetiklenmeden önce `grace_days` boyunca uyarı gönderilir. Tetiklenince `actions` listesindeki
eylemler sırayla çalıştırılır; yarım kalanlar bir sonraki çalıştırmada devam eder.
`self_destruct` (bu deponun silinmesi) yalnızca diğer tüm eylemler bittikten sonra çalışır.

Güvenlik: `--armed` (veya DEADMAN_ARMED=true) verilmedikçe hiçbir şey silinmez, sadece
ne yapılacağı yazdırılır.
"""

from __future__ import annotations

import copy
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Mapping

from . import notify
from .actions import DONE, FAILED, GAVE_UP, ActionContext, ActionError, ActionSpec, registry
from .util import fmt_human, fmt_time, human_delta, load_json, parse_time, save_json

DEFAULT_CONFIG = "deadman.json"
DEFAULT_STATE = ".deadman/state.json"
FINISHED = {DONE, GAVE_UP}
LOG_LIMIT = 200

Log = Callable[[str], None]


class ConfigError(Exception):
    pass


def action_id(action: dict, index: int) -> str:
    return str(action.get("id") or f"{action['type']}-{index + 1}")


@dataclass
class Config:
    path: Path
    checkin_interval_days: float | None
    trigger_at: datetime | None
    grace_days: float
    warn_every_hours: float
    preflight_every_days: float
    max_runtime_minutes: float
    notify: dict
    actions: list[dict]
    state_path: Path

    @property
    def base_dir(self) -> Path:
        return self.path.parent

    @classmethod
    def load(cls, path: str | Path = DEFAULT_CONFIG) -> "Config":
        path = Path(path)
        if not path.exists():
            raise ConfigError(f"{path} bulunamadı. Başlamak için: diedigital deadman init")
        return cls.from_dict(load_json(path), path)

    @classmethod
    def from_dict(cls, data: dict, path: str | Path = DEFAULT_CONFIG,
                  known: Mapping[str, ActionSpec] | None = None) -> "Config":
        path = Path(path)
        interval = data.get("checkin_interval_days")
        try:
            trigger_at = parse_time(data.get("trigger_at"))
        except ValueError as e:
            raise ConfigError(f"trigger_at okunamadı: {e}") from e
        if not interval and not trigger_at:
            raise ConfigError("En az biri gerekli: 'checkin_interval_days' veya 'trigger_at'.")
        if interval is not None and float(interval) <= 0:
            raise ConfigError("'checkin_interval_days' pozitif olmalı.")

        known = known if known is not None else registry()
        actions = [a for a in data.get("actions") or [] if a.get("enabled", True)]
        ids = set()
        for i, a in enumerate(actions):
            if a.get("type") not in known:
                raise ConfigError(f"{i + 1}. eylemin tipi bilinmiyor: {a.get('type')!r}. Seçenekler: {', '.join(known)}")
            aid = action_id(a, i)
            if aid in ids:
                raise ConfigError(f"Aynı id iki kez kullanılmış: {aid}")
            ids.add(aid)
        destruct = [i for i, a in enumerate(actions) if a["type"] == "self_destruct"]
        if destruct and destruct != [len(actions) - 1]:
            raise ConfigError("'self_destruct' tek olmalı ve listenin en sonunda yer almalı.")

        return cls(
            path=path,
            checkin_interval_days=float(interval) if interval else None,
            trigger_at=trigger_at,
            grace_days=float(data.get("grace_days", 7)),
            warn_every_hours=float(data.get("warn_every_hours", 24)),
            preflight_every_days=float(data.get("preflight_every_days", 7)),
            max_runtime_minutes=float(data.get("max_runtime_minutes", 120)),
            notify=data.get("notify") or {},
            actions=actions,
            state_path=path.parent / data.get("state_file", DEFAULT_STATE),
        )


# --- durum dosyası -----------------------------------------------------------------------------

def new_state(now: datetime) -> dict:
    return {
        "version": 1,
        "created_at": fmt_time(now),
        "last_checkin": fmt_time(now),
        "last_warning": None,
        "warnings_sent": 0,
        "last_preflight": None,
        "triggered_at": None,
        "actions": {},
        "log": [],
    }


def load_state(cfg: Config, now: datetime) -> dict:
    """Durum dosyası yoksa sayaç şimdi başlar; böylece dosyanın kaybolması asla erken tetiklemez."""
    state = load_json(cfg.state_path, None)
    if state is None:
        return new_state(now)
    for key, value in new_state(now).items():
        state.setdefault(key, value)
    return state


def save_state(cfg: Config, state: dict) -> None:
    save_json(cfg.state_path, state)


def log_event(state: dict, now: datetime, message: str) -> None:
    state["log"].append({"at": fmt_time(now), "msg": message})
    del state["log"][:-LOG_LIMIT]


# --- değerlendirme ----------------------------------------------------------------------------

@dataclass
class Evaluation:
    phase: str  # "ok" | "warning" | "trigger"
    trigger_time: datetime
    warn_from: datetime
    remaining: timedelta


def evaluate(cfg: Config, state: dict, now: datetime) -> Evaluation:
    candidates = []
    if cfg.trigger_at:
        candidates.append(cfg.trigger_at)
    if cfg.checkin_interval_days:
        base = parse_time(state.get("last_checkin")) or parse_time(state.get("created_at")) or now
        candidates.append(base + timedelta(days=cfg.checkin_interval_days + cfg.grace_days))
    trigger = min(candidates)
    warn_from = trigger - timedelta(days=cfg.grace_days)
    if state.get("triggered_at") or now >= trigger:
        phase = "trigger"
    elif now >= warn_from:
        phase = "warning"
    else:
        phase = "ok"
    return Evaluation(phase, trigger, warn_from, trigger - now)


def warning_due(cfg: Config, state: dict, now: datetime) -> bool:
    last = parse_time(state.get("last_warning"))
    return last is None or now - last >= timedelta(hours=cfg.warn_every_hours)


def preflight_due(cfg: Config, state: dict, now: datetime) -> bool:
    last = parse_time(state.get("last_preflight"))
    return last is None or now - last >= timedelta(days=cfg.preflight_every_days)


def checkin_hint(environ: Mapping[str, str]) -> str:
    repo = environ.get("GITHUB_REPOSITORY")
    if repo:
        server = environ.get("GITHUB_SERVER_URL", "https://github.com")
        return f"{server}/{repo}/actions/workflows/deadman.yml adresinde 'Run workflow' > checkin"
    return "diedigital deadman checkin"


# --- komutlar ---------------------------------------------------------------------------------

def checkin(cfg: Config, state: dict, now: datetime) -> str:
    aborted = bool(state.get("triggered_at"))
    state.update(last_checkin=fmt_time(now), last_warning=None, warnings_sent=0, triggered_at=None)
    log_event(state, now, "check-in" + (" (devam eden silme süreci durduruldu)" if aborted else ""))
    ev = evaluate(cfg, state, now)
    lines = [f"Check-in kaydedildi: {fmt_human(now)}",
             f"Sonraki tetikleme: {fmt_human(ev.trigger_time)} ({human_delta(ev.remaining)} sonra)"]
    if aborted:
        lines.append("Tetiklenmiş süreç durduruldu. Tamamlanmış eylemler geri alınamaz.")
    if cfg.trigger_at and ev.trigger_time == cfg.trigger_at:
        lines.append("Not: 'trigger_at' sabit bir tarih; check-in onu ertelemez. Ertelemek için deadman.json'u düzenle.")
    return "\n".join(lines)


def describe_actions(cfg: Config, known: Mapping[str, ActionSpec] | None = None) -> list[str]:
    known = known if known is not None else registry()
    out = []
    for i, a in enumerate(cfg.actions):
        try:
            text = known[a["type"]].describe(a)
        except Exception as e:
            text = f"{a['type']} (açıklanamadı: {e})"
        delay = f" [tetiklemeden {a['delay_days']} gün sonra]" if a.get("delay_days") else ""
        out.append(f"{i + 1}. {action_id(a, i)}: {text}{delay}")
    return out


def status_report(cfg: Config, state: dict, now: datetime) -> str:
    ev = evaluate(cfg, state, now)
    phase = {"ok": "Normal", "warning": "UYARI DÖNEMİ", "trigger": "TETİKLENDİ"}[ev.phase]
    lines = [
        f"Durum            : {phase}",
        f"Son check-in     : {fmt_human(parse_time(state.get('last_checkin')))}",
        f"Check-in aralığı : {f'{cfg.checkin_interval_days:g} gün' if cfg.checkin_interval_days else '-'}",
        f"Sabit tarih      : {fmt_human(cfg.trigger_at)}",
        f"Uyarılar başlar  : {fmt_human(ev.warn_from)}",
        f"Tetikleme        : {fmt_human(ev.trigger_time)}"
        + (f" ({human_delta(ev.remaining)} sonra)" if ev.phase != "trigger" else ""),
        f"Son ön kontrol   : {fmt_human(parse_time(state.get('last_preflight')))}",
        "",
        "Eylemler:",
    ]
    for i, desc in enumerate(describe_actions(cfg)):
        rec = state["actions"].get(action_id(cfg.actions[i], i), {})
        mark = rec.get("status", "bekliyor")
        if rec.get("summary"):
            mark += f" ({rec['summary']})"
        lines.append(f"  {desc}  -> {mark}")
    return "\n".join(lines)


@dataclass
class CheckResult:
    action: str
    ok: bool
    message: str


def preflight(cfg: Config, environ: Mapping[str, str], known: Mapping[str, ActionSpec] | None = None) -> list[CheckResult]:
    """Her eylemin kimlik bilgilerini dener. Süresi dolmuş token tetikleme gününde fark edilmesin diye."""
    known = known if known is not None else registry()
    results = []
    for i, a in enumerate(cfg.actions):
        ctx = ActionContext(dry_run=True, environ=environ, base_dir=cfg.base_dir, log=lambda _m: None)
        try:
            results.append(CheckResult(action_id(a, i), True, known[a["type"]].check(a, ctx) or "tamam"))
        except Exception as e:
            results.append(CheckResult(action_id(a, i), False, str(e)))
    return results


def execute_actions(cfg: Config, state: dict, now: datetime, *, dry_run: bool, environ: Mapping[str, str],
                    save: Callable[[dict], None], log: Log, known: Mapping[str, ActionSpec] | None = None,
                    clock: Callable[[], float] = time.monotonic) -> bool:
    """Eylemleri sırayla çalıştırır. Hepsi bittiyse True döner."""
    known = known if known is not None else registry()
    deadline = clock() + cfg.max_runtime_minutes * 60
    triggered_at = parse_time(state.get("triggered_at")) or now
    records = state["actions"]

    for i, a in enumerate(cfg.actions):
        aid = action_id(a, i)
        rec = copy.deepcopy(records.get(aid, {})) if dry_run else records.setdefault(aid, {})
        if rec.get("status") in FINISHED:
            continue

        due = triggered_at + timedelta(days=float(a.get("delay_days", 0) or 0))
        if not dry_run and now < due:
            log(f"[{aid}] {fmt_human(due)} tarihini bekliyor")
            continue
        if a["type"] == "self_destruct" and not a.get("force"):
            pending = [action_id(o, j) for j, o in enumerate(cfg.actions[:i])
                       if records.get(action_id(o, j), {}).get("status") not in FINISHED]
            if pending and not dry_run:
                log(f"[{aid}] diğer eylemler bitmeden çalışmaz; bekleyenler: {', '.join(pending)}")
                continue
        if clock() >= deadline - 60:
            log("Çalışma süresi doldu; kalan eylemler bir sonraki çalıştırmada.")
            break

        ctx = ActionContext(dry_run=dry_run, memory=rec.setdefault("memory", {}), deadline=deadline,
                            environ=environ, base_dir=cfg.base_dir, log=lambda m, p=aid: log(f"[{p}] {m}"))
        log(f"[{aid}] başlıyor{' (deneme)' if dry_run else ''}: {known[a['type']].describe(a)}")
        try:
            res = known[a["type"]].run(a, ctx) or {"status": DONE, "summary": ""}
            status, summary = res["status"], res.get("summary", "")
        except ActionError as e:
            status, summary = FAILED, str(e)
        except Exception as e:  # beklenmeyen hata diğer eylemleri durdurmasın
            status, summary = FAILED, f"{type(e).__name__}: {e}"
        log(f"[{aid}] {status}: {summary}")
        if dry_run:
            continue

        rec.update(status=status, summary=summary, at=fmt_time(now))
        if status == FAILED:
            rec["attempts"] = rec.get("attempts", 0) + 1
            if rec["attempts"] >= int(a.get("max_attempts", 7)):
                rec["status"] = GAVE_UP
                log(f"[{aid}] {rec['attempts']} denemeden sonra vazgeçildi")
        log_event(state, now, f"{aid}: {rec['status']} - {summary}")
        save(state)
        if status == FAILED and a.get("stop_on_error"):
            break

    return all(records.get(action_id(a, i), {}).get("status") in FINISHED for i, a in enumerate(cfg.actions))


def run(cfg: Config, state: dict, now: datetime, *, armed: bool, environ: Mapping[str, str],
        save: Callable[[dict], None], log: Log = print, known: Mapping[str, ActionSpec] | None = None) -> str:
    """Zamanlanmış çalıştırma: duruma göre hiçbir şey yapmaz, uyarır ya da eylemleri çalıştırır."""
    ev = evaluate(cfg, state, now)
    hint = checkin_hint(environ)
    log(f"Durum: {ev.phase} | tetikleme: {fmt_human(ev.trigger_time)}")

    if ev.phase != "trigger" and preflight_due(cfg, state, now):
        results = preflight(cfg, environ, known)
        state["last_preflight"] = fmt_time(now)
        failed = [r for r in results if not r.ok]
        for r in results:
            log(f"  ön kontrol {'tamam' if r.ok else 'HATA'} [{r.action}]: {r.message}")
        if failed:
            body = "\n".join(f"- {r.action}: {r.message}" for r in failed)
            notify.send(cfg.notify, "Ölü adam anahtarı: ön kontrol başarısız",
                        f"Tetikleme anında çalışmayacak eylemler var:\n\n{body}\n\n"
                        f"Token/parolaları yenile, sonra 'preflight' ile tekrar dene.",
                        environ=environ, log=log)
        log_event(state, now, f"ön kontrol: {len(results) - len(failed)}/{len(results)} tamam")
        save(state)

    if ev.phase == "ok":
        log(f"Her şey yolunda. Uyarılar {fmt_human(ev.warn_from)} tarihinde başlar.")
        return ev.phase

    if ev.phase == "warning":
        if warning_due(cfg, state, now):
            plan = "\n".join(describe_actions(cfg, known))
            errors = notify.send(
                cfg.notify,
                f"Ölü adam anahtarı: {human_delta(ev.remaining)} kaldı",
                f"Son check-in: {fmt_human(parse_time(state.get('last_checkin')))}\n"
                f"Silme işlemleri {fmt_human(ev.trigger_time)} tarihinde başlayacak.\n\n"
                f"Durdurmak için check-in yap: {hint}\n\nPlanlanan eylemler:\n{plan}\n",
                environ=environ, log=log,
            )
            state["last_warning"] = fmt_time(now)
            state["warnings_sent"] = state.get("warnings_sent", 0) + 1
            log_event(state, now, f"uyarı #{state['warnings_sent']}"
                      + (f" gönderilemedi: {'; '.join(errors)}" if errors else " gönderildi"))
            save(state)
        return ev.phase

    if not armed:
        log("TETİKLENDİ, ama anahtar kurulu değil (--armed / DEADMAN_ARMED=true yok). Deneme modunda çalışıyor.")
        if warning_due(cfg, state, now):
            notify.send(cfg.notify, "Ölü adam anahtarı tetiklendi (deneme modu)",
                        "Süre doldu ama DEADMAN_ARMED=true olmadığı için hiçbir şey silinmedi.\n"
                        f"Ya check-in yap ({hint}) ya da anahtarı kur.", environ=environ, log=log)
            state["last_warning"] = fmt_time(now)
            save(state)
        execute_actions(cfg, state, now, dry_run=True, environ=environ, save=save, log=log, known=known)
        return ev.phase

    if not state.get("triggered_at"):
        state["triggered_at"] = fmt_time(now)
        log_event(state, now, "TETİKLENDİ")
        save(state)
        notify.send(cfg.notify, "Ölü adam anahtarı tetiklendi",
                    "Silme işlemleri başladı.\n\n" + "\n".join(describe_actions(cfg, known)) +
                    f"\n\nKalan eylemleri durdurmak için hâlâ check-in yapabilirsin: {hint}",
                    environ=environ, log=log)

    finished = execute_actions(cfg, state, now, dry_run=False, environ=environ, save=save, log=log, known=known)
    if finished:
        log("Tüm eylemler tamamlandı.")
    return ev.phase
