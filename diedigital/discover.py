"""Unuttuğun hesapları bul: e-posta kutundaki "hoş geldin / doğrula / şifre sıfırla" mesajlarını tarar.

Sadece başlıklar (From, Subject, Date) okunur; mesaj gövdeleri indirilmez ve hiçbir şey
işaretlenmez/silinmez (posta kutusu salt okunur açılır).
Gmail için: Google Hesabı > Güvenlik > Uygulama şifreleri ile bir IMAP şifresi oluştur.
"""

from __future__ import annotations

import email
import email.policy
import imaplib
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from email.utils import parseaddr, parsedate_to_datetime

from .util import fold, registrable_domain

SIGNUP_KEYWORDS = [
    "welcome", "verify", "verification", "confirm your", "confirm email", "activate", "activation",
    "account created", "registration", "sign up", "signup", "password reset", "reset your password",
    "new sign-in", "new login", "your account",
    "hos geldin", "hosgeldin", "dogrula", "dogrulama", "onayla", "onay kodu", "uyelik", "uyeliginiz",
    "hesabiniz", "kaydiniz", "kayit", "sifre sifirlama", "sifrenizi", "aktivasyon", "giris yapildi",
]
# Kişisel e-posta sağlayıcıları; buradan gelen postalar bir hizmet kaydı değil, insanlardır.
FREEMAIL = {
    "gmail.com", "googlemail.com", "hotmail.com", "outlook.com", "live.com", "msn.com", "yahoo.com",
    "icloud.com", "me.com", "aol.com", "yandex.com", "yandex.ru", "mail.ru", "proton.me",
    "protonmail.com", "gmx.com", "gmx.de", "web.de", "hotmail.com.tr", "windowslive.com",
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LIST_RE = re.compile(rb'\((?P<flags>[^)]*)\) (?:"[^"]*"|NIL) (?P<name>.+)$')


@dataclass
class Sender:
    domain: str
    count: int = 0
    signup_hits: int = 0
    first: datetime | None = None
    last: datetime | None = None
    samples: list = field(default_factory=list)

    @property
    def score(self) -> int:
        return self.signup_hits * 10 + self.count


def imap_since(d: date) -> str:
    return f"{d.day:02d}-{MONTHS[d.month - 1]}-{d.year}"


def find_all_mail(conn: imaplib.IMAP4) -> str:
    """Gmail'de tüm postaları içeren klasör (\\All) varsa onu, yoksa INBOX'ı seçer."""
    typ, data = conn.list()
    if typ == "OK":
        for line in data or []:
            m = LIST_RE.match(line or b"")
            if m and b"\\All" in m.group("flags"):
                return m.group("name").decode("utf-8", errors="replace").strip()
    return "INBOX"


def is_signup(subject: str) -> bool:
    s = fold(subject)
    return any(k in s for k in SIGNUP_KEYWORDS)


def add_header(senders: dict[str, Sender], raw: bytes) -> None:
    try:
        msg = email.message_from_bytes(raw, policy=email.policy.default)
        _, addr = parseaddr(str(msg.get("From", "")))
        subject = str(msg.get("Subject", "") or "")
    except Exception:
        return
    domain = registrable_domain(addr.rsplit("@", 1)[-1]) if "@" in addr else None
    if not domain or domain in FREEMAIL:
        return
    s = senders.setdefault(domain, Sender(domain))
    s.count += 1
    if is_signup(subject):
        s.signup_hits += 1
        if len(s.samples) < 3:
            s.samples.append(subject[:100])
    try:
        when = parsedate_to_datetime(str(msg.get("Date")))
    except (TypeError, ValueError):
        when = None
    if when:
        when = when.replace(tzinfo=None)
        s.first = min(s.first, when) if s.first else when
        s.last = max(s.last, when) if s.last else when


def scan_imap(host: str, user: str, password: str, *, folder: str | None = None, since: date | None = None,
              port: int = 993, chunk: int = 500, progress=print) -> list[Sender]:
    conn = imaplib.IMAP4_SSL(host, port)
    try:
        conn.login(user, password)
        folder = folder or find_all_mail(conn)
        quoted = folder if folder.startswith('"') else f'"{folder}"'
        typ, _ = conn.select(quoted, readonly=True)
        if typ != "OK":
            raise RuntimeError(f"Klasör açılamadı: {folder}")
        criteria = f"SINCE {imap_since(since)}" if since else "ALL"
        typ, data = conn.uid("SEARCH", None, criteria)
        uids = (data[0] or b"").split() if typ == "OK" else []
        progress(f"{folder}: {len(uids)} mesaj taranacak")
        senders: dict[str, Sender] = {}
        for i in range(0, len(uids), chunk):
            batch = b",".join(uids[i:i + chunk]).decode()
            typ, data = conn.uid("FETCH", batch, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if typ != "OK":
                continue
            for part in data:
                if isinstance(part, tuple) and len(part) > 1:
                    add_header(senders, part[1])
            progress(f"  {min(i + chunk, len(uids))}/{len(uids)}")
        return sorted(senders.values(), key=lambda s: s.score, reverse=True)
    finally:
        try:
            conn.logout()
        except Exception:
            pass
