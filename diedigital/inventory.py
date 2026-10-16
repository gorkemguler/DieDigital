"""Hesap envanteri: hangi hesap nerede, hangi aşamada."""

from __future__ import annotations

import csv
from datetime import timedelta
from pathlib import Path

from .catalog import DIFFICULTY, Catalog
from .util import domain_of, fmt_human, fmt_time, fold, load_json, parse_time, save_json, utcnow

DEFAULT_PATH = "accounts.json"

STATUSES = {
    "active": "Aktif",
    "exported": "Yedeği alındı",
    "wiped": "İçerik temizlendi",
    "requested": "Silme talep edildi",
    "deleted": "Silindi",
    "blocked": "Silinemiyor",
}
OPEN_STATUSES = ["active", "exported", "wiped", "requested"]

# Parola yöneticisi dışa aktarımlarındaki sütun adları (küçük harfe çevrilmiş).
URL_COLUMNS = ["url", "login_uri", "web site", "website", "login url", "uri", "location"]
NAME_COLUMNS = ["name", "title", "account", "hesap"]
USER_COLUMNS = ["username", "login_username", "login name", "user name", "user", "login", "email", "e-mail"]


class Inventory:
    def __init__(self, path: str | Path = DEFAULT_PATH, catalog: Catalog | None = None):
        self.path = Path(path)
        self.catalog = catalog or Catalog.load()
        data = load_json(self.path, {"accounts": []})
        self.accounts: list[dict] = data.get("accounts", [])

    def save(self) -> None:
        save_json(self.path, {"accounts": self.accounts})

    def _next_id(self) -> int:
        return max((a.get("id", 0) for a in self.accounts), default=0) + 1

    def find(self, key: str | int) -> dict | None:
        text = str(key).strip()
        if text.isdigit():
            for a in self.accounts:
                if a.get("id") == int(text):
                    return a
        k = fold(text)
        for a in self.accounts:
            if k in (fold(a.get("service")), fold(a.get("catalog_id"))):
                return a
        return None

    def _dedupe_key(self, acc: dict) -> tuple[str, str]:
        where = acc.get("catalog_id") or domain_of(acc.get("url")) or fold(acc.get("service"))
        who = fold(acc.get("username") or acc.get("email"))
        return where, who

    def exists(self, acc: dict) -> bool:
        key = self._dedupe_key(acc)
        return any(self._dedupe_key(a) == key for a in self.accounts)

    def add(self, service: str, *, url: str | None = None, username: str | None = None,
            email: str | None = None, privacy_email: str | None = None,
            jurisdiction: str | None = None, notes: str | None = None,
            status: str = "active", source: str = "manual") -> dict:
        entry = self.catalog.match(service, url)
        now = fmt_time(utcnow())
        acc = {
            "id": self._next_id(),
            "service": entry["name"] if entry and fold(service) in (fold(entry["id"]), fold(entry["name"])) else service,
            "catalog_id": entry["id"] if entry else None,
            "url": url or None,
            "username": username or None,
            "email": email or None,
            "privacy_email": privacy_email or (entry or {}).get("privacy_email"),
            "jurisdiction": jurisdiction or (entry or {}).get("jurisdiction"),
            "status": status,
            "notes": notes or None,
            "source": source,
            "requested_at": None,
            "history": [{"at": now, "status": status}],
        }
        self.accounts.append(acc)
        return acc

    def set_status(self, acc: dict, status: str, note: str | None = None) -> None:
        if status not in STATUSES:
            raise ValueError(f"Geçersiz durum: {status}. Seçenekler: {', '.join(STATUSES)}")
        now = fmt_time(utcnow())
        acc["status"] = status
        if status == "requested" and not acc.get("requested_at"):
            acc["requested_at"] = now
        event = {"at": now, "status": status}
        if note:
            event["note"] = note
        acc.setdefault("history", []).append(event)

    def overdue(self, days: int = 30) -> list[dict]:
        limit = utcnow() - timedelta(days=days)
        return [
            a for a in self.accounts
            if a.get("status") == "requested" and a.get("requested_at")
            and parse_time(a["requested_at"]) <= limit
        ]


def _pick(row: dict, columns: list[str]) -> str:
    for c in columns:
        value = (row.get(c) or "").strip()
        if value:
            return value
    return ""


def import_csv(inv: Inventory, path: str | Path) -> tuple[int, int]:
    """Parola yöneticisi (Bitwarden, 1Password, Chrome, Firefox, KeePass...) CSV'sinden hesap ekler.

    Parolalar hiçbir zaman okunmaz ve kaydedilmez. Dışa aktarılan CSV'yi işin bitince güvenle sil.
    """
    added = skipped = 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row = {(k or "").strip().lower(): v for k, v in raw.items() if k}
            # Bitwarden'da bir kayıtta birden çok adres olabilir; ilkini al.
            url = _pick(row, URL_COLUMNS).split(",")[0].strip()
            name = _pick(row, NAME_COLUMNS)
            user = _pick(row, USER_COLUMNS)
            domain = domain_of(url)
            if not domain and not name:
                skipped += 1
                continue
            entry = inv.catalog.match(name, url)
            service = entry["name"] if entry else (domain or name)
            email = user if "@" in user else None
            username = None if email else (user or None)
            candidate = {"catalog_id": entry["id"] if entry else None, "url": url or None,
                         "service": service, "username": username, "email": email}
            if inv.exists(candidate):
                skipped += 1
                continue
            inv.add(service, url=url or None, username=username, email=email, source=f"csv:{Path(path).name}")
            added += 1
    return added, skipped


def report_markdown(inv: Inventory) -> str:
    counts = {s: 0 for s in STATUSES}
    for a in inv.accounts:
        counts[a.get("status", "active")] = counts.get(a.get("status", "active"), 0) + 1
    lines = [
        "# Hesap envanteri",
        "",
        f"Oluşturulma: {fmt_human(utcnow())}",
        "",
        " · ".join(f"{STATUSES[s]}: {n}" for s, n in counts.items() if n) or "Envanter boş.",
        "",
    ]
    for status, title in STATUSES.items():
        group = [a for a in inv.accounts if a.get("status") == status]
        if not group:
            continue
        lines += [f"## {title}", ""]
        for a in sorted(group, key=lambda x: fold(x.get("service"))):
            box = "x" if status in ("deleted", "blocked") else " "
            who = ", ".join(x for x in (a.get("username"), a.get("email")) if x)
            lines.append(f"- [{box}] **{a['service']}** (#{a['id']}){f' — {who}' if who else ''}")
            entry = inv.catalog.get(a.get("catalog_id"))
            details = []
            if entry:
                if entry.get("delete_url"):
                    details.append(f"[silme]({entry['delete_url']})")
                if entry.get("export_url"):
                    details.append(f"[yedek]({entry['export_url']})")
                if entry.get("grace_days") is not None:
                    details.append(f"bekleme {entry['grace_days']} gün")
                if entry.get("difficulty"):
                    details.append(f"zorluk: {DIFFICULTY.get(entry['difficulty'], entry['difficulty'])}")
            if a.get("privacy_email"):
                details.append(f"gizlilik: {a['privacy_email']}")
            if a.get("requested_at"):
                details.append(f"talep: {fmt_human(parse_time(a['requested_at']))}")
            if details:
                lines.append(f"  - {' · '.join(details)}")
            if entry and entry.get("notes") and status in OPEN_STATUSES:
                lines.append(f"  - {entry['notes']}")
            if a.get("notes"):
                lines.append(f"  - Not: {a['notes']}")
        lines.append("")
    return "\n".join(lines)
