"""Komut satırı arayüzü: `diedigital <komut> ...` ya da `python -m diedigital <komut> ...`"""

from __future__ import annotations

import argparse
import getpass
import os
import shutil
import sys
from datetime import date
from pathlib import Path

from . import __version__, deadman, footprint, letters, mailer
from .actions import ActionContext, ActionError, registry
from .catalog import Catalog, describe
from .inventory import STATUSES, Inventory, import_csv, report_markdown
from .util import DATA_DIR, env, env_flag, fmt_time, parse_time, utcnow


def _inventory(args) -> Inventory:
    return Inventory(args.inventory)


def _write_or_print(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"Yazıldı: {out}")
    else:
        print(text)


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        print("Onay için etkileşimli terminal gerekli; --yes ile atlayabilirsin.")
        return False
    return input(f"{prompt} Devam etmek için SIL yaz: ").strip().upper() == "SIL"


# --- catalog ---------------------------------------------------------------------------------

def cmd_catalog(args) -> int:
    cat = Catalog.load()
    entries = cat.search(args.query) if args.query else cat.entries
    if not entries:
        print("Eşleşen hizmet yok. Genel yöntem: hesap ayarlarında 'sil/kapat' ara, yoksa KVKK/GDPR dilekçesi gönder.")
        return 1
    for e in entries:
        print(describe(e) if args.query else f"{e['id']:<20} {e['name']}")
        if args.query:
            print()
    return 0


# --- inventory -------------------------------------------------------------------------------

def cmd_inv_add(args) -> int:
    inv = _inventory(args)
    acc = inv.add(args.service, url=args.url, username=args.username, email=args.email,
                  privacy_email=args.privacy_email, jurisdiction=args.jurisdiction, notes=args.notes)
    inv.save()
    print(f"Eklendi: #{acc['id']} {acc['service']}" + (" (katalogda var)" if acc["catalog_id"] else ""))
    entry = inv.catalog.get(acc["catalog_id"])
    if entry:
        print(describe(entry))
    return 0


def cmd_inv_import(args) -> int:
    inv = _inventory(args)
    added, skipped = import_csv(inv, args.csv)
    inv.save()
    print(f"{added} hesap eklendi, {skipped} satır atlandı (tekrar veya adres yok).")
    print("Parolalar okunmadı ve kaydedilmedi. Dışa aktardığın CSV'yi şimdi güvenle sil.")
    return 0


def cmd_inv_list(args) -> int:
    inv = _inventory(args)
    rows = [a for a in inv.accounts if not args.status or a.get("status") == args.status]
    if not rows:
        print("Envanter boş." if not inv.accounts else "Bu durumda hesap yok.")
        return 0
    for a in rows:
        who = a.get("username") or a.get("email") or ""
        print(f"#{a['id']:<4} {STATUSES.get(a['status'], a['status']):<20} {a['service']:<30} {who}")
    return 0


def cmd_inv_set(args) -> int:
    inv = _inventory(args)
    acc = inv.find(args.account)
    if not acc:
        print(f"Bulunamadı: {args.account}")
        return 1
    if args.privacy_email:
        acc["privacy_email"] = args.privacy_email
    if args.status:
        inv.set_status(acc, args.status, args.note)
    inv.save()
    print(f"#{acc['id']} {acc['service']}: {STATUSES[acc['status']]}")
    return 0


def cmd_inv_report(args) -> int:
    _write_or_print(report_markdown(_inventory(args)), args.out)
    return 0


def cmd_inv_overdue(args) -> int:
    late = _inventory(args).overdue(args.days)
    if not late:
        print(f"{args.days} günü geçen cevapsız talep yok.")
        return 0
    for a in late:
        print(f"#{a['id']} {a['service']} — talep: {a['requested_at']}")
        print(f"   hatırlatma: diedigital letters send --account {a['id']} --reminder --execute")
    print("\nHatırlatmaya da cevap gelmezse: KVKK Kurulu'na / ilgili denetim makamına şikâyet (docs/06-hukuki-haklar.md).")
    return 0


# --- discover --------------------------------------------------------------------------------

def cmd_discover_imap(args) -> int:
    from .discover import scan_imap

    password = env("IMAP_PASSWORD") or getpass.getpass(f"{args.user} için IMAP şifresi: ")
    since = date.fromisoformat(args.since) if args.since else None
    senders = scan_imap(args.host, args.user, password, folder=args.folder, since=since, port=args.port)
    hits = [s for s in senders if s.signup_hits or args.all]
    cat = Catalog.load()
    print(f"\n{len(hits)} olası hesap (toplam {len(senders)} gönderen alan adı):\n")
    for s in hits[: args.top]:
        entry = cat.by_domain(s.domain)
        span = f"{s.first:%Y-%m}..{s.last:%Y-%m}" if s.first and s.last else ""
        print(f"{s.domain:<30} kayıt maili: {s.signup_hits:<3} toplam: {s.count:<5} {span:<17} {entry['name'] if entry else ''}")
        for sample in s.samples:
            print(f"    · {sample}")
    if args.add:
        inv = _inventory(args)
        added = 0
        for s in hits[: args.top]:
            entry = cat.by_domain(s.domain)
            candidate = {"catalog_id": entry["id"] if entry else None, "url": f"https://{s.domain}",
                         "service": entry["name"] if entry else s.domain, "email": args.user}
            if not inv.exists(candidate):
                inv.add(candidate["service"], url=candidate["url"], email=args.user, source="imap")
                added += 1
        inv.save()
        print(f"\nEnvantere {added} hesap eklendi: {inv.path}")
    return 0


# --- footprint -------------------------------------------------------------------------------

def cmd_fp_username(args) -> int:
    results = footprint.check_username(args.username)
    order = {"found": 0, "unknown": 1, "manual": 2, "absent": 3}
    labels = {"found": "VAR", "unknown": "?", "manual": "elle bak", "absent": "yok"}
    for r in sorted(results, key=lambda r: order[r.state]):
        if r.state == "absent" and not args.all:
            continue
        print(f"{labels[r.state]:<9} {r.name:<28} {r.url}{f'  ({r.detail})' if r.state == 'unknown' else ''}")
    print(f"\n{sum(r.state == 'found' for r in results)} sitede bulundu. 'elle bak' satırlarını tarayıcıda aç.")
    return 0


def cmd_fp_email(args) -> int:
    g = footprint.gravatar(args.email)
    print(f"Gravatar: {g + ' (herkese açık profil/avatar var, kaldır!)' if g else 'yok'}")
    key = env("HIBP_API_KEY")
    if not key:
        print("Sızıntılar: HIBP_API_KEY tanımlı değil. Elle kontrol: https://haveibeenpwned.com")
        return 0
    breaches = footprint.hibp_breaches(args.email, key)
    print(f"Sızıntılar: {len(breaches)}")
    for b in breaches:
        print(f"  {b.get('BreachDate', '?'):<11} {b.get('Name')} ({b.get('Domain') or '-'})")
    if args.add and breaches:
        inv = _inventory(args)
        added = 0
        for b in breaches:
            if not b.get("Domain"):
                continue
            candidate = {"url": f"https://{b['Domain']}", "service": b.get("Title") or b["Domain"], "email": args.email}
            entry = inv.catalog.match(candidate["service"], candidate["url"])
            candidate["catalog_id"] = entry["id"] if entry else None
            if not inv.exists(candidate):
                inv.add(candidate["service"], url=candidate["url"], email=args.email, source="hibp",
                        notes=f"Sızıntı: {b.get('BreachDate')}")
                added += 1
        inv.save()
        print(f"Envantere {added} hesap eklendi.")
    return 0


def cmd_fp_dorks(args) -> int:
    queries = footprint.dork_queries(args.name, args.email or [], args.username or [], args.phone or [], args.city)
    if not queries:
        print("En az bir bilgi ver: --name, --email, --username veya --phone")
        return 1
    _write_or_print(footprint.dork_markdown(queries), args.out)
    return 0


# --- letters ---------------------------------------------------------------------------------

def _letter(args, inv: Inventory | None = None):
    profile = letters.load_profile(args.profile)
    account = None
    if getattr(args, "account", None):
        inv = inv or _inventory(args)
        account = inv.find(args.account)
        if not account:
            raise letters.LetterError(f"Envanterde bulunamadı: {args.account}")
    elif getattr(args, "service", None):
        entry = Catalog.load().match(args.service) or {}
        account = {"service": entry.get("name", args.service), "jurisdiction": entry.get("jurisdiction"),
                   "privacy_email": entry.get("privacy_email")}
    template = args.template or letters.auto_template(account, getattr(args, "reminder", False))
    subject, body = letters.render(template, profile, account, urls=getattr(args, "url", None) or [])
    return account, subject, body


def cmd_letters_list(args) -> int:
    for name, path in letters.list_templates().items():
        print(f"{name:<20} {path}")
    return 0


def cmd_letters_render(args) -> int:
    _, subject, body = _letter(args)
    _write_or_print(f"Konu: {subject}\n\n{body}", args.out)
    return 0


def cmd_letters_send(args) -> int:
    inv = _inventory(args)
    account, subject, body = _letter(args, inv)
    to = args.to or (account or {}).get("privacy_email")
    if not to:
        print("Alıcı yok: --to ver ya da envanterde privacy_email doldur (inventory set ... --privacy-email).")
        return 1
    profile = letters.load_profile(args.profile)
    if not args.execute:
        print(f"Alıcı: {to}\nKonu: {subject}\n\n{body}\n(Deneme. Göndermek için --execute ekle.)")
        return 0
    mailer.send([to], subject, body, bcc_self=True, reply_to=profile.get("email"))
    if account and account.get("id") and not args.reminder:
        inv.set_status(account, "requested", f"dilekçe: {to}")
        inv.save()
    return 0


def cmd_letters_bulk(args) -> int:
    inv = _inventory(args)
    profile = letters.load_profile(args.profile)
    if args.reminder:
        targets = inv.overdue(args.days)
    else:
        statuses = args.status or ["active", "exported", "wiped"]
        targets = [a for a in inv.accounts if a.get("status") in statuses]
    targets = [a for a in targets if a.get("privacy_email")]
    if not targets:
        print("Gönderilecek kimse yok (privacy_email alanı dolu hesap bulunamadı).")
        return 0
    print(f"{len(targets)} dilekçe: " + ", ".join(a["service"] for a in targets))
    if args.execute and not _confirm(f"{len(targets)} e-posta gönderilecek.", args.yes):
        return 1
    failures = 0
    for acc in targets:
        try:
            subject, body = letters.render(args.template or letters.auto_template(acc, args.reminder), profile, acc)
            mailer.send([acc["privacy_email"]], subject, body, bcc_self=True,
                        reply_to=profile.get("email"), dry_run=not args.execute)
        except (letters.LetterError, mailer.MailError) as e:
            print(f"HATA {acc['service']}: {e}")
            failures += 1
            continue
        if args.execute and not args.reminder:
            inv.set_status(acc, "requested", f"dilekçe: {acc['privacy_email']}")
    inv.save()
    if not args.execute:
        print("(Deneme. Göndermek için --execute ekle.)")
    return 1 if failures else 0


# --- wipe ------------------------------------------------------------------------------------

def _run_action(kind: str, params: dict, args) -> int:
    spec = registry()[kind]
    print(spec.describe(params))
    if args.execute and not _confirm("Bu işlem geri alınamaz.", args.yes):
        return 1
    ctx = ActionContext(dry_run=not args.execute)
    try:
        res = spec.run(params, ctx)
    except ActionError as e:
        print(f"HATA: {e}")
        return 1
    print(f"{res['status']}: {res['summary']}")
    if not args.execute:
        print("(Deneme. Gerçekten silmek için --execute ekle.)")
    return 0


def cmd_wipe_github(args) -> int:
    return _run_action("github_wipe", {
        "include": args.include or ["*"], "exclude": args.exclude or [],
        "repos": not args.no_repos, "gists": not args.no_gists, "scrub_profile": args.scrub_profile,
    }, args)


def cmd_wipe_reddit(args) -> int:
    return _run_action("reddit_wipe", {
        "overwrite": not args.no_overwrite, "overwrite_text": args.text, "ids_files": args.ids_file or [],
    }, args)


def cmd_wipe_mastodon(args) -> int:
    return _run_action("mastodon_wipe", {
        "instance": args.instance, "keep_pinned": args.keep_pinned, "older_than_days": args.older_than_days,
    }, args)


# --- deadman ---------------------------------------------------------------------------------

def _now(args):
    return parse_time(args.now) if getattr(args, "now", None) else utcnow()


def cmd_dm_init(args) -> int:
    target = Path(args.config)
    if target.exists() and not args.force:
        print(f"{target} zaten var (--force ile üzerine yazılır).")
        return 1
    shutil.copyfile(DATA_DIR / "deadman.example.json", target)
    cfg = deadman.Config.load(target)
    state = deadman.new_state(_now(args))
    deadman.save_state(cfg, state)
    print(f"Oluşturuldu: {target} ve {cfg.state_path}")
    print("Şimdi deadman.json'u düzenle, sonra: diedigital deadman preflight")
    return 0


def _load(args):
    cfg = deadman.Config.load(args.config)
    now = _now(args)
    return cfg, deadman.load_state(cfg, now), now


def cmd_dm_checkin(args) -> int:
    cfg, state, now = _load(args)
    print(deadman.checkin(cfg, state, now))
    deadman.save_state(cfg, state)
    if not os.environ.get("GITHUB_ACTIONS"):
        print(f"\nGitHub Actions kullanıyorsan şunu da yap: git add {cfg.state_path} && git commit -m checkin && git push")
    return 0


def cmd_dm_status(args) -> int:
    cfg, state, now = _load(args)
    print(deadman.status_report(cfg, state, now))
    return 0


def cmd_dm_preflight(args) -> int:
    cfg, state, now = _load(args)
    results = deadman.preflight(cfg, os.environ)
    for r in results:
        print(f"{'tamam' if r.ok else 'HATA ':<6} {r.action:<20} {r.message}")
    if cfg.notify.get("emails"):
        try:
            print(f"tamam  {'bildirim':<20} {mailer.check()}")
        except mailer.MailError as e:
            print(f"HATA   {'bildirim':<20} {e}")
            results.append(deadman.CheckResult("bildirim", False, str(e)))
    state["last_preflight"] = fmt_time(now)
    deadman.save_state(cfg, state)
    return 0 if all(r.ok for r in results) else 1


def cmd_dm_dry_run(args) -> int:
    cfg, state, now = _load(args)
    print("Deneme: tetiklenmiş gibi davranıp tüm eylemleri hiçbir şey silmeden çalıştırıyor.\n")
    deadman.execute_actions(cfg, state, now, dry_run=True, environ=os.environ, save=lambda s: None, log=print)
    return 0


def cmd_dm_run(args) -> int:
    cfg, state, now = _load(args)
    armed = args.armed or env_flag("DEADMAN_ARMED")
    deadman.run(cfg, state, now, armed=armed, environ=os.environ, save=lambda s: deadman.save_state(cfg, s))
    deadman.save_state(cfg, state)
    return 0


# --- parser ----------------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="diedigital", description="Dijital ayak izini bul, temizle ve sil.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--inventory", default=env("DIEDIGITAL_INVENTORY", "accounts.json"), help="envanter dosyası")
    p.add_argument("--profile", default=env("DIEDIGITAL_PROFILE", "profile.json"), help="kişisel bilgiler dosyası")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("catalog", help="bilinen hizmetlerin silme bağlantıları")
    c.add_argument("query", nargs="?")
    c.set_defaults(func=cmd_catalog)

    inv = sub.add_parser("inventory", help="hesap envanteri").add_subparsers(dest="sub", required=True)
    a = inv.add_parser("add", help="hesap ekle")
    a.add_argument("service")
    a.add_argument("--url")
    a.add_argument("--username")
    a.add_argument("--email")
    a.add_argument("--privacy-email", help="KVKK/GDPR başvuru adresi")
    a.add_argument("--jurisdiction", choices=["tr", "eu", "other"])
    a.add_argument("--notes")
    a.set_defaults(func=cmd_inv_add)
    a = inv.add_parser("import", help="parola yöneticisi CSV'sinden içe aktar (parolalar okunmaz)")
    a.add_argument("csv")
    a.set_defaults(func=cmd_inv_import)
    a = inv.add_parser("list", help="listele")
    a.add_argument("--status", choices=list(STATUSES))
    a.set_defaults(func=cmd_inv_list)
    a = inv.add_parser("set", help="durum güncelle")
    a.add_argument("account", help="#id veya hizmet adı")
    a.add_argument("status", nargs="?", choices=list(STATUSES))
    a.add_argument("--note")
    a.add_argument("--privacy-email")
    a.set_defaults(func=cmd_inv_set)
    a = inv.add_parser("report", help="Markdown kontrol listesi")
    a.add_argument("--out")
    a.set_defaults(func=cmd_inv_report)
    a = inv.add_parser("overdue", help="cevapsız kalan silme talepleri")
    a.add_argument("--days", type=int, default=30)
    a.set_defaults(func=cmd_inv_overdue)

    d = sub.add_parser("discover", help="unuttuğun hesapları bul").add_subparsers(dest="sub", required=True)
    a = d.add_parser("imap", help="e-posta kutusunu kayıt mesajları için tara (salt okunur)")
    a.add_argument("--host", required=True, help="ör. imap.gmail.com, outlook.office365.com")
    a.add_argument("--user", required=True)
    a.add_argument("--port", type=int, default=993)
    a.add_argument("--folder", help="varsayılan: Gmail'de Tüm Postalar, diğerlerinde INBOX")
    a.add_argument("--since", help="YYYY-AA-GG")
    a.add_argument("--top", type=int, default=200)
    a.add_argument("--all", action="store_true", help="kayıt maili olmayan gönderenleri de göster")
    a.add_argument("--add", action="store_true", help="bulunanları envantere ekle")
    a.set_defaults(func=cmd_discover_imap)

    f = sub.add_parser("footprint", help="ayak izi taraması").add_subparsers(dest="sub", required=True)
    a = f.add_parser("username", help="kullanıcı adının hangi sitelerde olduğunu kontrol et")
    a.add_argument("username")
    a.add_argument("--all", action="store_true", help="bulunmayanları da göster")
    a.set_defaults(func=cmd_fp_username)
    a = f.add_parser("email", help="Gravatar ve veri sızıntısı kontrolü")
    a.add_argument("email")
    a.add_argument("--add", action="store_true", help="sızıntıdaki hizmetleri envantere ekle")
    a.set_defaults(func=cmd_fp_email)
    a = f.add_parser("dorks", help="arama motoru kontrol listesi üret")
    a.add_argument("--name")
    a.add_argument("--email", action="append")
    a.add_argument("--username", action="append")
    a.add_argument("--phone", action="append")
    a.add_argument("--city")
    a.add_argument("--out")
    a.set_defaults(func=cmd_fp_dorks)

    lt = sub.add_parser("letters", help="KVKK/GDPR dilekçeleri").add_subparsers(dest="sub", required=True)
    a = lt.add_parser("list", help="şablonlar")
    a.set_defaults(func=cmd_letters_list)
    for name, func, text in (("render", cmd_letters_render, "dilekçeyi ekrana/dosyaya yaz"),
                             ("send", cmd_letters_send, "dilekçeyi e-postayla gönder")):
        a = lt.add_parser(name, help=text)
        a.add_argument("--template")
        a.add_argument("--account", help="envanterdeki #id veya hizmet adı")
        a.add_argument("--service", help="envanterde olmayan hizmet adı")
        a.add_argument("--url", action="append", help="archive-removal şablonu için URL (tekrarlanabilir)")
        a.add_argument("--reminder", action="store_true", help="hatırlatma şablonunu kullan")
        if name == "render":
            a.add_argument("--out")
        else:
            a.add_argument("--to", help="alıcı (varsayılan: envanterdeki privacy_email)")
            a.add_argument("--execute", action="store_true")
        a.set_defaults(func=func)
    a = lt.add_parser("bulk", help="envanterdeki tüm uygun hesaplara dilekçe gönder")
    a.add_argument("--template")
    a.add_argument("--status", action="append", choices=list(STATUSES))
    a.add_argument("--reminder", action="store_true", help="cevapsız taleplere hatırlatma gönder")
    a.add_argument("--days", type=int, default=30)
    a.add_argument("--execute", action="store_true")
    a.add_argument("--yes", action="store_true")
    a.set_defaults(func=cmd_letters_bulk)

    w = sub.add_parser("wipe", help="içerik silme araçları (varsayılan deneme modu)").add_subparsers(dest="sub", required=True)
    a = w.add_parser("github", help="repolar, gist'ler, profil (GH_WIPE_TOKEN)")
    a.add_argument("--include", action="append", help="glob, ör. 'eski-*'")
    a.add_argument("--exclude", action="append")
    a.add_argument("--no-repos", action="store_true")
    a.add_argument("--no-gists", action="store_true")
    a.add_argument("--scrub-profile", action="store_true")
    a.set_defaults(func=cmd_wipe_github)
    a = w.add_parser("reddit", help="yorum ve gönderiler (REDDIT_* değişkenleri)")
    a.add_argument("--no-overwrite", action="store_true")
    a.add_argument("--text", default=".")
    a.add_argument("--ids-file", action="append", help="veri dışa aktarımındaki comments.csv / posts.csv")
    a.set_defaults(func=cmd_wipe_reddit)
    a = w.add_parser("mastodon", help="gönderiler (MASTODON_TOKEN)")
    a.add_argument("--instance", required=True, help="ör. https://mastodon.social")
    a.add_argument("--keep-pinned", action="store_true")
    a.add_argument("--older-than-days", type=float)
    a.set_defaults(func=cmd_wipe_mastodon)
    for parser in w.choices.values():
        parser.add_argument("--execute", action="store_true", help="gerçekten sil")
        parser.add_argument("--yes", action="store_true", help="onay sorma")

    dm = sub.add_parser("deadman", help="ölü adam anahtarı").add_subparsers(dest="sub", required=True)
    for name, func, text in (
        ("init", cmd_dm_init, "örnek yapılandırmayı oluştur"),
        ("checkin", cmd_dm_checkin, "hayattayım: sayacı sıfırla"),
        ("status", cmd_dm_status, "durum ve kalan süre"),
        ("preflight", cmd_dm_preflight, "token/parolaları şimdi dene"),
        ("dry-run", cmd_dm_dry_run, "tetiklenmiş gibi, ama hiçbir şey silmeden çalıştır"),
        ("run", cmd_dm_run, "zamanlanmış çalıştırma (cron / GitHub Actions)"),
    ):
        a = dm.add_parser(name, help=text)
        a.add_argument("--config", default=deadman.DEFAULT_CONFIG)
        a.add_argument("--now", help=argparse.SUPPRESS)  # test için
        if name == "init":
            a.add_argument("--force", action="store_true")
        if name == "run":
            a.add_argument("--armed", action="store_true", help="gerçekten sil (yoksa deneme)")
        a.set_defaults(func=func)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args) or 0
    except (deadman.ConfigError, letters.LetterError, mailer.MailError, ActionError, ValueError, OSError) as e:
        print(f"HATA: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nİptal edildi.", file=sys.stderr)
        return 130
