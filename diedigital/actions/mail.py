"""E-posta eylemleri: envanterdeki her hizmete silme dilekçesi gönderme ve serbest e-posta."""

from __future__ import annotations

from .. import letters, mailer
from ..inventory import OPEN_STATUSES, Inventory
from . import DONE, INCOMPLETE, ActionContext, ActionError, result


def _recipients(params: dict, ctx: ActionContext) -> tuple[Inventory, list[dict]]:
    inv = Inventory(ctx.path(params.get("inventory", "accounts.json")))
    statuses = params.get("statuses", OPEN_STATUSES)
    return inv, [a for a in inv.accounts if a.get("status") in statuses and a.get("privacy_email")]


def describe_send_letters(params: dict) -> str:
    tpl = params.get("template") or "otomatik: KVKK/GDPR, daha önce talep edilenlere hatırlatma"
    return f"envanterdeki hizmetlere silme dilekçesi gönder (şablon: {tpl})"


def check_send_letters(params: dict, ctx: ActionContext) -> str:
    profile = letters.load_profile(ctx.path(params.get("profile", "profile.json")), ctx.environ)
    if not profile.get("name") or not profile.get("email"):
        raise ActionError("Profilde 'name' ve 'email' olmalı (DIEDIGITAL_PROFILE_JSON veya profile.json).")
    _, targets = _recipients(params, ctx)
    if not targets:
        raise ActionError("Gönderilecek dilekçe yok: envanterde 'privacy_email' alanı dolu açık hesap bulunamadı.")
    return f"{len(targets)} dilekçe hazır; {mailer.check(ctx.environ)}"


def run_send_letters(params: dict, ctx: ActionContext) -> dict:
    profile = letters.load_profile(ctx.path(params.get("profile", "profile.json")), ctx.environ)
    _, targets = _recipients(params, ctx)
    sent = ctx.memory.setdefault("sent", [])
    errors = []
    for acc in targets:
        key = str(acc["id"])
        if key in sent:
            continue
        if ctx.out_of_time():
            return result(INCOMPLETE, f"{len(sent)} dilekçe gönderildi; süre doldu")
        # Daha önce talep gönderilmiş hesaplara ilk dilekçe yerine hatırlatma gider.
        template = params.get("template") or letters.auto_template(acc, reminder=acc.get("status") == "requested")
        try:
            subject, body = letters.render(template, profile, acc, environ=ctx.environ)
            mailer.send([acc["privacy_email"]], subject, body, environ=ctx.environ, bcc_self=True,
                        reply_to=profile.get("email"), dry_run=ctx.dry_run, log=ctx.log)
        except (letters.LetterError, mailer.MailError) as e:
            errors.append(f"{acc['service']}: {e}")
            continue
        if not ctx.dry_run:
            sent.append(key)
    if errors:
        raise ActionError("; ".join(errors))
    return result(DONE, f"{len(targets)} hizmete dilekçe {'gönderilecek' if ctx.dry_run else 'gönderildi'}")


def _body(params: dict, ctx: ActionContext) -> str:
    if params.get("body_file"):
        return ctx.path(params["body_file"]).read_text(encoding="utf-8")
    return params.get("body", "")


def describe_email(params: dict) -> str:
    return f"e-posta gönder → {', '.join(params.get('to', []))}: {params.get('subject', '')}"


def check_email(params: dict, ctx: ActionContext) -> str:
    if not params.get("to"):
        raise ActionError("'to' listesi boş.")
    _body(params, ctx)
    return mailer.check(ctx.environ)


def run_email(params: dict, ctx: ActionContext) -> dict:
    try:
        mailer.send(params["to"], params.get("subject", ""), _body(params, ctx), environ=ctx.environ,
                    dry_run=ctx.dry_run, log=ctx.log)
    except mailer.MailError as e:
        raise ActionError(str(e)) from e
    return result(DONE, f"e-posta {'gönderilecek' if ctx.dry_run else 'gönderildi'}: {', '.join(params['to'])}")
