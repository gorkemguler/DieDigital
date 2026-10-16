"""Uyarı bildirimleri: e-posta ve isteğe bağlı webhook (ntfy, Discord, Slack)."""

from __future__ import annotations

from typing import Callable, Mapping

from . import mailer, net


def _webhook_payload(fmt: str, subject: str, body: str) -> dict:
    text = f"{subject}\n\n{body}"
    if fmt == "discord":
        return {"json_body": {"content": text[:1900]}}
    if fmt == "slack":
        return {"json_body": {"text": text}}
    # ntfy.sh gibi düz metin kabul eden servisler
    return {"headers": {"Content-Type": "text/plain; charset=utf-8"}, "data": text.encode("utf-8")}


def send(cfg: Mapping, subject: str, body: str, *, environ: Mapping[str, str],
         dry_run: bool = False, log: Callable[[str], None] = print) -> list[str]:
    """Bildirimi tüm kanallara göndermeyi dener, hataları liste olarak döndürür (asla fırlatmaz)."""
    errors = []
    emails = list(cfg.get("emails") or [])
    url = environ.get(cfg.get("webhook_env", "DEADMAN_WEBHOOK_URL")) or None

    if emails:
        try:
            mailer.send(emails, subject, body, environ=environ, dry_run=dry_run, log=log)
        except Exception as e:  # bildirim hatası asıl işi durdurmamalı
            errors.append(f"e-posta: {e}")

    if url:
        payload = _webhook_payload(cfg.get("webhook_format", "text"), subject, body)
        if dry_run:
            log(f"[deneme] webhook bildirimi: {subject}")
        else:
            try:
                r = net.request("POST", url, retries=2, **payload)
                if not r.ok:
                    errors.append(f"webhook: HTTP {r.status}")
            except Exception as e:
                errors.append(f"webhook: {e}")

    if not emails and not url:
        errors.append("bildirim kanalı tanımlı değil (notify.emails veya webhook)")
    for e in errors:
        log(f"UYARI: bildirim gönderilemedi - {e}")
    return errors

