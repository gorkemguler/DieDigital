"""Mastodon: tüm gönderileri siler, paylaşımları (boost) geri alır.

Token: Tercihler > Geliştirme > Yeni uygulama; "read" ve "write:statuses" kapsamları yeterli.
Mastodon gönderi silmeyi sınırlar (varsayılan: 30 dakikada 30 silme). Büyük hesaplarda iş
birkaç güne yayılır; eylem `incomplete` döner ve sonraki çalıştırmada devam eder.

Not: Mastodon 4.x'te Tercihler > Otomatik gönderi silme ile eski gönderileri sunucunun
kendisine sildirebilirsin; hesabı ise Tercihler > Hesap > Hesabı sil ile kapatırsın.
"""

from __future__ import annotations

from datetime import timedelta

from .. import net
from ..util import parse_time, utcnow
from . import DONE, INCOMPLETE, ActionContext, ActionError, result

DEFAULT_TOKEN_ENV = "MASTODON_TOKEN"


def _client(params: dict, ctx: ActionContext) -> tuple[str, dict]:
    instance = (params.get("instance") or "").rstrip("/")
    if not instance.startswith("https://"):
        raise ActionError("'instance' parametresi https://sunucu.adi biçiminde olmalı.")
    token = ctx.secret(params.get("token_env", DEFAULT_TOKEN_ENV))
    return instance, {"Authorization": f"Bearer {token}"}


def _me(instance: str, headers: dict, ctx: ActionContext) -> dict:
    r = net.request("GET", f"{instance}/api/v1/accounts/verify_credentials", headers=headers,
                    max_wait=ctx.wait_budget())
    if r.status == 401:
        raise ActionError("Mastodon token geçersiz.")
    return r.raise_for_status().json()


def describe(params: dict) -> str:
    extra = f", {params['older_than_days']} günden eski olanlar" if params.get("older_than_days") else ""
    return f"Mastodon gönderilerini sil ({params.get('instance', '?')}{extra})"


def check(params: dict, ctx: ActionContext) -> str:
    instance, headers = _client(params, ctx)
    return f"Mastodon: @{_me(instance, headers, ctx)['acct']} olarak erişim tamam"


def run_wipe(params: dict, ctx: ActionContext) -> dict:
    instance, headers = _client(params, ctx)
    me = _me(instance, headers, ctx)
    keep_pinned = bool(params.get("keep_pinned", False))
    cutoff = None
    if params.get("older_than_days"):
        cutoff = utcnow() - timedelta(days=float(params["older_than_days"]))
    count = ctx.memory.get("count", 0)
    verb = "silinecek" if ctx.dry_run else "silindi"
    max_id = None

    while True:
        r = net.request("GET", f"{instance}/api/v1/accounts/{me['id']}/statuses", headers=headers,
                        params={"limit": 40, "max_id": max_id}, max_wait=ctx.wait_budget())
        statuses = r.raise_for_status().json()
        if not statuses:
            break
        for status in statuses:
            max_id = status["id"]
            if keep_pinned and status.get("pinned"):
                continue
            if cutoff and parse_time(status["created_at"]) > cutoff:
                continue
            if ctx.out_of_time():
                ctx.memory["count"] = count
                return result(INCOMPLETE, f"{count} gönderi {verb}; süre doldu")
            if not ctx.dry_run:
                if status.get("reblog"):
                    url = f"{instance}/api/v1/statuses/{status['reblog']['id']}/unreblog"
                    r = net.request("POST", url, headers=headers, max_wait=ctx.wait_budget())
                else:
                    r = net.request("DELETE", f"{instance}/api/v1/statuses/{status['id']}", headers=headers,
                                    max_wait=ctx.wait_budget())
                if r.status == 429:
                    # Hız sınırının sıfırlanmasını bekleyecek kadar süre kalmadı.
                    ctx.memory["count"] = count
                    return result(INCOMPLETE, f"{count} gönderi {verb}; hız sınırı, sonra devam edecek")
                if r.status not in (200, 404):
                    r.raise_for_status()
            count += 1

    ctx.memory["count"] = count
    return result(DONE, f"@{me['acct']}: {count} gönderi {verb}")
