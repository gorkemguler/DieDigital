"""Ortak yardımcılar: zaman, JSON dosyaları, alan adları."""

from __future__ import annotations

import copy
import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"

# Alan adını ayıklarken tek parça sayılmayan yaygın son ekler (ör. trendyol.com.tr değil trendyol.com).
SECOND_LEVEL_SUFFIXES = {
    "com.tr", "net.tr", "org.tr", "gen.tr", "biz.tr", "info.tr", "web.tr", "av.tr",
    "bel.tr", "gov.tr", "edu.tr", "k12.tr", "pol.tr", "tsk.tr", "name.tr", "tv.tr",
    "co.uk", "org.uk", "ac.uk", "gov.uk", "me.uk",
    "com.au", "net.au", "org.au", "co.nz",
    "co.jp", "ne.jp", "or.jp", "co.kr",
    "com.br", "com.cn", "com.mx", "com.ar", "co.in", "co.za",
    "com.sg", "com.hk", "com.tw", "com.ua", "com.cy",
}

TRUTHY = {"1", "true", "yes", "on", "evet"}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: Any) -> datetime | None:
    """ISO 8601 metni (veya yalnızca tarih) UTC datetime'a çevirir."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if text.endswith(("Z", "z")):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fmt_time(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt_human(dt: datetime | None) -> str:
    if dt is None:
        return "-"
    return dt.astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")


def human_delta(delta: timedelta) -> str:
    seconds = int(delta.total_seconds())
    if seconds <= 0:
        return "süre doldu"
    days, rest = divmod(seconds, 86400)
    hours, rest = divmod(rest, 3600)
    minutes = rest // 60
    parts = []
    if days:
        parts.append(f"{days} gün")
    if hours:
        parts.append(f"{hours} saat")
    if not days and minutes:
        parts.append(f"{minutes} dakika")
    return " ".join(parts) or "1 dakikadan az"


def load_json(path: str | Path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return copy.deepcopy(default)
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str | Path, data: Any) -> None:
    """Yarım kalmış yazma dosyayı bozmasın diye geçici dosya + yeniden adlandırma kullanır."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=f".{p.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def env(name: str, default: str | None = None, environ: Mapping[str, str] | None = None) -> str | None:
    value = (environ if environ is not None else os.environ).get(name)
    return value if value not in (None, "") else default


def env_flag(name: str, environ: Mapping[str, str] | None = None) -> bool:
    return (env(name, "", environ) or "").strip().lower() in TRUTHY


def registrable_domain(host: str | None) -> str | None:
    """mail.google.com -> google.com, www.trendyol.com.tr -> trendyol.com.tr"""
    if not host:
        return None
    host = host.strip().strip(".").lower()
    if host.startswith("[") or re.fullmatch(r"[\d.]+", host):
        return host
    labels = host.split(".")
    if len(labels) <= 2:
        return host
    if ".".join(labels[-2:]) in SECOND_LEVEL_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def domain_of(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return None
    return registrable_domain(parsed.hostname)


def fold(text: str | None) -> str:
    """Karşılaştırma için: küçük harf, aksansız (ğ->g, ı->i)."""
    text = (text or "").replace("ı", "i").replace("İ", "i")
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).casefold().strip()
