"""Ayak izi taraması: kullanıcı adı hangi sitelerde var, e-posta nerede görünüyor, ne aranmalı.

Bu araç yalnızca kendi izini bulmak içindir; sadece herkese açık profil sayfalarına bakar.
"""

from __future__ import annotations

import hashlib
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from . import net
from .util import DATA_DIR, load_json

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

ENGINES = {
    "Google": "https://www.google.com/search?q={q}",
    "Bing": "https://www.bing.com/search?q={q}",
    "DuckDuckGo": "https://duckduckgo.com/?q={q}",
    "Yandex": "https://yandex.com.tr/search/?text={q}",
}


@dataclass
class SiteResult:
    name: str
    url: str
    state: str  # found | absent | unknown | manual
    detail: str = ""


def load_sites() -> list[dict]:
    return load_json(DATA_DIR / "sites.json", {"sites": []})["sites"]


def check_site(site: dict, username: str, timeout: float = 15) -> SiteResult:
    quoted = urllib.parse.quote(username, safe="")
    profile = site["url"].format(u=quoted)
    method = site.get("method", "status")
    if method == "manual":
        return SiteResult(site["name"], profile, "manual", "elle kontrol et")
    check = site.get("check", site["url"]).format(u=quoted)
    try:
        r = net.request("GET", check, headers={"User-Agent": BROWSER_UA}, timeout=timeout, retries=1, max_wait=5)
    except Exception as e:
        return SiteResult(site["name"], profile, "unknown", type(e).__name__)
    text = r.text if r.body else ""
    if r.status in (403, 429) or r.status >= 500:
        return SiteResult(site["name"], profile, "unknown", f"HTTP {r.status}")
    if method == "status":
        state = "absent" if r.status in (404, 410) else "found" if r.ok else "unknown"
    elif method == "absent_text":
        state = "absent" if r.status == 404 or site["text"] in text else "found" if r.ok else "unknown"
    elif method == "present_text":
        state = "found" if r.ok and site["text"] in text else "absent" if r.ok or r.status == 404 else "unknown"
    elif method == "json_null":
        state = "absent" if r.status == 404 or text.strip() in ("", "null") else "found" if r.ok else "unknown"
    elif method == "json_empty":
        state = "absent" if r.status == 404 or text.strip() in ("", "[]", "{}") else "found" if r.ok else "unknown"
    else:
        state = "unknown"
    return SiteResult(site["name"], profile, state, f"HTTP {r.status}")


def check_username(username: str, workers: int = 8, sites: list[dict] | None = None) -> list[SiteResult]:
    sites = sites if sites is not None else load_sites()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda s: check_site(s, username), sites))


def gravatar(email_address: str) -> str | None:
    """E-postaya bağlı herkese açık Gravatar varsa adresini döndürür."""
    digest = hashlib.sha256(email_address.strip().lower().encode("utf-8")).hexdigest()
    url = f"https://gravatar.com/avatar/{digest}?d=404"
    r = net.request("GET", url, retries=1)
    return f"https://gravatar.com/{digest}" if r.ok else None


def hibp_breaches(email_address: str, api_key: str) -> list[dict]:
    """Have I Been Pwned: e-postanın yer aldığı veri sızıntıları. Ücretli API anahtarı gerekir."""
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + urllib.parse.quote(email_address)
    r = net.request("GET", url, params={"truncateResponse": "false"}, headers={"hibp-api-key": api_key})
    if r.status == 404:
        return []
    if r.status == 401:
        raise RuntimeError("HIBP API anahtarı geçersiz.")
    return r.raise_for_status().json() or []


def phone_variants(phone: str) -> list[str]:
    """+90 532 123 45 67 numarasının ilanlarda/PDF'lerde görülebilecek yazılışları."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("90") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) != 10:
        return [phone]
    a, b, c, d = digits[:3], digits[3:6], digits[6:8], digits[8:]
    return list(dict.fromkeys([
        f"0{a} {b} {c} {d}", f"0{digits}", digits, f"+90 {a} {b} {c} {d}", f"+90{digits}",
        f"({a}) {b} {c} {d}", f"0 ({a}) {b} {c} {d}", f"0{a} {b}{c}{d}", f"{a} {b} {c} {d}",
    ]))


def dork_queries(name: str | None = None, emails=(), usernames=(), phones=(), city: str | None = None) -> list[tuple[str, str]]:
    """(açıklama, sorgu) çiftleri."""
    q: list[tuple[str, str]] = []
    if name:
        n = f'"{name}"'
        q += [
            ("Adın", n),
            ("Adın + şehir", f"{n} \"{city}\"") if city else None,
            ("Sosyal medyada adın", f"{n} (site:linkedin.com OR site:facebook.com OR site:instagram.com OR site:x.com OR site:twitter.com OR site:tiktok.com)"),
            ("Belgelerde adın (CV, listeler, sonuçlar)", f"{n} (filetype:pdf OR filetype:doc OR filetype:docx)"),
            ("Tablolarda adın", f"{n} (filetype:xls OR filetype:xlsx OR filetype:csv)"),
            ("Satış veri platformlarında adın", f"{n} (site:zoominfo.com OR site:rocketreach.co OR site:apollo.io OR site:signalhire.com OR site:contactout.com OR site:lusha.com)"),
            ("Forum ve sözlüklerde adın", f"{n} (site:eksisozluk.com OR site:reddit.com OR site:quora.com)"),
            ("Haber sitelerinde adın", f"{n} (haber OR news)"),
            ("Arşivlerde adın", f"{n} site:web.archive.org"),
        ]
    for e in emails:
        q += [("E-posta adresin", f'"{e}"'), ("E-posta adresinin kullanıcı kısmı", f'"{e.split("@")[0]}"')]
    for u in usernames:
        q += [("Kullanıcı adın", f'"{u}"'), ("Kullanıcı adın (büyük siteler hariç)", f'"{u}" -site:github.com -site:x.com -site:instagram.com')]
    for p in phones:
        variants = phone_variants(p)
        q.append(("Telefon numaran", " OR ".join(f'"{v}"' for v in variants[:5])))
        q.append(("İlan sitelerinde telefonun", f'"{variants[0]}" (site:sahibinden.com OR site:letgo.com OR site:dolap.com)'))
    return [x for x in q if x]


def dork_markdown(queries: list[tuple[str, str]]) -> str:
    lines = ["# Arama kontrol listesi", "",
             "Her sorguyu tüm arama motorlarında aç. Bulduğun her sonucu not et: kaynağı sil/düzelt, "
             "sonra arama motorundan kaldırma iste (bkz. docs/04-arama-motorlari-ve-arsivler.md).", ""]
    for title, query in queries:
        links = " · ".join(f"[{eng}]({url.format(q=urllib.parse.quote_plus(query))})" for eng, url in ENGINES.items())
        lines += [f"- [ ] **{title}**: `{query}`", f"  - {links}"]
    lines += ["", "Görseller için: Google Görseller, Bing Görsel Arama ve Yandex Görseller'de kendi "
              "fotoğraflarınla tersine görsel araması yap."]
    return "\n".join(lines) + "\n"
