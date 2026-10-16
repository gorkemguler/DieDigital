"""SMTP üzerinden e-posta gönderimi. Ayarlar ortam değişkenlerinden okunur."""

from __future__ import annotations

import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from typing import Callable, Iterable, Mapping

from .util import env


class MailError(Exception):
    pass


@dataclass
class SMTPConfig:
    host: str
    port: int
    user: str | None
    password: str | None
    sender: str
    use_ssl: bool

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "SMTPConfig":
        host = env("SMTP_HOST", environ=environ)
        if not host:
            raise MailError("SMTP_HOST tanımlı değil (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM).")
        port = int(env("SMTP_PORT", "587", environ))
        user = env("SMTP_USER", environ=environ)
        sender = env("SMTP_FROM", user, environ)
        if not sender:
            raise MailError("Gönderen adresi yok: SMTP_FROM veya SMTP_USER tanımla.")
        return cls(host, port, user, env("SMTP_PASSWORD", environ=environ), sender, port == 465)

    def connect(self) -> smtplib.SMTP:
        context = ssl.create_default_context()
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port, timeout=60, context=context)
        else:
            server = smtplib.SMTP(self.host, self.port, timeout=60)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        if self.user:
            server.login(self.user, self.password or "")
        return server


def build_message(sender: str, to: Iterable[str], subject: str, body: str,
                  reply_to: str | None = None) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=False)
    msg["Message-ID"] = make_msgid(domain=sender.rsplit("@", 1)[-1].strip(">") or None)
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body)
    return msg


def send(to: Iterable[str], subject: str, body: str, *, environ: Mapping[str, str] | None = None,
         bcc_self: bool = False, reply_to: str | None = None, dry_run: bool = False,
         log: Callable[[str], None] = print) -> None:
    to = [t for t in to if t]
    if not to:
        raise MailError("Alıcı yok.")
    if dry_run:
        log(f"[deneme] e-posta → {', '.join(to)} | {subject}")
        return
    cfg = SMTPConfig.from_env(environ)
    msg = build_message(cfg.sender, to, subject, body, reply_to)
    # Bcc başlık olarak eklenmez; sadece zarf alıcısıdır. Başvurunun kanıtı olarak kendine kopya.
    recipients = to + ([cfg.sender] if bcc_self and cfg.sender not in to else [])
    try:
        with cfg.connect() as server:
            server.send_message(msg, from_addr=cfg.sender, to_addrs=recipients)
    except (smtplib.SMTPException, OSError) as e:
        raise MailError(f"Gönderilemedi ({', '.join(to)}): {e}") from e
    log(f"e-posta gönderildi → {', '.join(to)} | {subject}")


def check(environ: Mapping[str, str] | None = None) -> str:
    cfg = SMTPConfig.from_env(environ)
    try:
        with cfg.connect():
            pass
    except (smtplib.SMTPException, OSError) as e:
        raise MailError(f"SMTP bağlantısı başarısız ({cfg.host}:{cfg.port}): {e}") from e
    return f"SMTP {cfg.host}:{cfg.port} ({cfg.sender}) tamam"
