"""KVKK / GDPR silme dilekçeleri.

Şablonlar `diedigital/templates/*.txt` içinde. İlk satır "Konu:" ya da "Subject:" ile başlar.
Kendi şablonlarını `./templates/` klasörüne aynı adla koyarsan onlar kullanılır.

Yer tutucular: $name $email $address $phone $national_id $service $username
$account_email $identifiers $date $request_date $urls
Bir satırdaki tüm yer tutucular boşsa satır tamamen atlanır (ör. T.C. kimlik no vermediysen).
"""

from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from .util import PACKAGE_DIR, load_json, parse_time

BUILTIN_DIR = PACKAGE_DIR / "templates"
PLACEHOLDER = re.compile(r"\$(?:\{(\w+)\}|(\w+))")
SUBJECT_PREFIXES = ("konu:", "subject:")


class LetterError(Exception):
    pass


def template_dirs(environ: Mapping[str, str] | None = None) -> list[Path]:
    environ = environ if environ is not None else os.environ
    dirs = []
    if environ.get("DIEDIGITAL_TEMPLATES"):
        dirs.append(Path(environ["DIEDIGITAL_TEMPLATES"]))
    dirs += [Path("templates"), BUILTIN_DIR]
    return dirs


def list_templates(environ: Mapping[str, str] | None = None) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for d in reversed(template_dirs(environ)):
        if d.is_dir():
            for p in sorted(d.glob("*.txt")):
                found[p.stem] = p
    return found


def load_template(name: str, environ: Mapping[str, str] | None = None) -> tuple[str, str]:
    path = list_templates(environ).get(name)
    if not path:
        raise LetterError(f"Şablon bulunamadı: {name}. Mevcut: {', '.join(list_templates(environ))}")
    lines = path.read_text(encoding="utf-8").splitlines()
    subject = ""
    if lines and lines[0].strip().lower().startswith(SUBJECT_PREFIXES):
        subject = lines[0].split(":", 1)[1].strip()
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return subject, "\n".join(lines).rstrip() + "\n"


def load_profile(path: str | Path | None = None, environ: Mapping[str, str] | None = None) -> dict:
    """Kişisel bilgiler: önce DIEDIGITAL_PROFILE_JSON ortam değişkeni, sonra profile.json."""
    environ = environ if environ is not None else os.environ
    raw = environ.get("DIEDIGITAL_PROFILE_JSON")
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise LetterError(f"DIEDIGITAL_PROFILE_JSON geçerli JSON değil: {e}") from e
    return load_json(path or "profile.json", {})


def _unique(items: Iterable[str | None]) -> list[str]:
    seen, out = set(), []
    for item in items:
        if item and item.strip() and item.strip().lower() not in seen:
            seen.add(item.strip().lower())
            out.append(item.strip())
    return out


def identifiers(profile: dict, account: dict | None = None) -> list[str]:
    account = account or {}
    return _unique([
        account.get("email"),
        account.get("username"),
        *(account.get("identifiers") or []),
        profile.get("email"),
        *(profile.get("emails") or []),
        profile.get("phone"),
        *(profile.get("phones") or []),
        *(profile.get("usernames") or []),
    ])


def _fmt_date(value) -> str:
    dt = parse_time(value) if value else None
    return dt.strftime("%d.%m.%Y") if dt else ""


def build_fields(profile: dict, account: dict | None = None, extra: Mapping[str, str] | None = None,
                 today: date | None = None, urls: Iterable[str] = ()) -> dict[str, str]:
    account = account or {}
    today = today or date.today()
    fields = {
        "name": profile.get("name", ""),
        "email": profile.get("email", ""),
        "address": profile.get("address", ""),
        "phone": profile.get("phone", ""),
        "national_id": profile.get("national_id", ""),
        "service": account.get("service", ""),
        "username": account.get("username") or "",
        "account_email": account.get("email") or "",
        "identifiers": "\n".join(f"- {i}" for i in identifiers(profile, account)),
        "date": today.strftime("%d.%m.%Y"),
        "request_date": _fmt_date(account.get("requested_at")),
        "urls": "\n".join(f"- {u}" for u in urls),
    }
    fields.update({k: v for k, v in (extra or {}).items() if v is not None})
    return fields


def render_text(text: str, fields: Mapping[str, str]) -> str:
    out = []
    for line in text.splitlines():
        names = [a or b for a, b in PLACEHOLDER.findall(line)]
        if names and all(not fields.get(n) for n in names):
            continue
        out.append(PLACEHOLDER.sub(lambda m: fields.get(m.group(1) or m.group(2), m.group(0)), line))
    return "\n".join(out).strip() + "\n"


def render(name: str, profile: dict, account: dict | None = None, *, extra: Mapping[str, str] | None = None,
           urls: Iterable[str] = (), today: date | None = None,
           environ: Mapping[str, str] | None = None) -> tuple[str, str]:
    if not profile.get("name"):
        raise LetterError("Profilde 'name' yok. profile.json oluştur (örnek: examples/profile.example.json).")
    subject_tpl, body_tpl = load_template(name, environ)
    fields = build_fields(profile, account, extra, today, urls)
    subject = render_text(subject_tpl, fields).strip()
    if fields.get("service") and fields["service"] not in subject:
        subject = f"{subject} - {fields['service']}"
    return subject, render_text(body_tpl, fields)


def auto_template(account: dict | None, reminder: bool = False) -> str:
    turkish = ((account or {}).get("jurisdiction") or "").lower() == "tr"
    if reminder:
        return "kvkk-hatirlatma" if turkish else "gdpr-reminder"
    return "kvkk-silme" if turkish else "gdpr-erasure"
