"""Reddit: yorum ve gönderilerin üzerine anlamsız metin yazar, sonra siler.

Neden önce üzerine yazmak? Silinen içeriğin son hâli bazı üçüncü taraf arşivlerde kalabiliyor;
üzerine yazmak en azından son sürümün anlamsız olmasını sağlar.

Kurulum: https://www.reddit.com/prefs/apps adresinden "script" tipi bir uygulama oluştur.
Ortam değişkenleri: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD
(İki adımlı doğrulama açıksa script uygulamalarıyla parola girişi çalışmayabilir.)

Reddit listeleri en fazla ~1000 öğe gösterir. Daha eskileri için reddit.com/settings/data-request
üzerinden verini iste ve gelen comments.csv / posts.csv dosyalarını `ids_files` ile ver.
"""

from __future__ import annotations

import csv

from .. import __version__, net
from . import DONE, INCOMPLETE, ActionContext, ActionError, result

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API = "https://oauth.reddit.com"
DEFAULT_SORTS = ["new", "top", "controversial", "hot"]


class Reddit:
    def __init__(self, params: dict, ctx: ActionContext):
        self.ctx = ctx
        self.client_id = ctx.secret(params.get("client_id_env", "REDDIT_CLIENT_ID"))
        self.client_secret = ctx.secret(params.get("client_secret_env", "REDDIT_CLIENT_SECRET"))
        self.username = ctx.secret(params.get("username_env", "REDDIT_USERNAME"))
        self.password = ctx.secret(params.get("password_env", "REDDIT_PASSWORD"))
        self.user_agent = f"script:diedigital:{__version__} (by /u/{self.username})"
        self.pause = float(params.get("pause_seconds", 1.0))
        self.token: str | None = None

    def login(self) -> None:
        r = net.request(
            "POST", TOKEN_URL, auth=(self.client_id, self.client_secret),
            form={"grant_type": "password", "username": self.username, "password": self.password},
            headers={"User-Agent": self.user_agent},
        )
        data = r.json() if r.body else {}
        if not r.ok or "access_token" not in (data or {}):
            raise ActionError(f"Reddit girişi başarısız: {(data or {}).get('error', r.status)}")
        self.token = data["access_token"]

    def call(self, method: str, path: str, **kwargs) -> net.Response:
        if not self.token:
            self.login()
        for _ in range(2):
            headers = {"Authorization": f"bearer {self.token}", "User-Agent": self.user_agent}
            r = net.request(method, API + path, headers=headers, max_wait=self.ctx.wait_budget(), **kwargs)
            if r.status == 401:
                self.login()
                continue
            self._throttle(r)
            return r
        raise ActionError("Reddit oturumu yenilenemedi.")

    def _throttle(self, r: net.Response) -> None:
        try:
            remaining = float(r.headers.get("x-ratelimit-remaining", "10"))
            reset = float(r.headers.get("x-ratelimit-reset", "0"))
        except ValueError:
            return
        if remaining < 2 and reset > 0:
            self.ctx.sleep(min(reset + 1, self.ctx.wait_budget()))

    def listing(self, kind: str, sort: str):
        after = None
        while True:
            params = {"limit": 100, "sort": sort, "raw_json": 1, "after": after}
            if sort in ("top", "controversial"):
                params["t"] = "all"
            r = self.call("GET", f"/user/{self.username}/{kind}", params=params).raise_for_status()
            data = r.json()["data"]
            for child in data["children"]:
                yield child["data"]
            after = data.get("after")
            if not after:
                return

    def scrub(self, fullname: str, editable: bool, text: str | None) -> None:
        if editable and text is not None:
            # Bağlantı gönderileri düzenlenemez; hata dönerse yine de silmeye geçeriz.
            self.call("POST", "/api/editusertext", form={"thing_id": fullname, "text": text, "api_type": "json"})
            self.ctx.sleep(self.pause)
        r = self.call("POST", "/api/del", form={"id": fullname})
        if not r.ok:
            raise ActionError(f"{fullname} silinemedi: HTTP {r.status}")
        self.ctx.sleep(self.pause)


def describe(params: dict) -> str:
    kinds = ", ".join(params.get("kinds", ["comments", "submitted"]))
    extra = f" + {len(params.get('ids_files', []))} dışa aktarım dosyası" if params.get("ids_files") else ""
    return f"Reddit içeriklerinin üzerine yaz ve sil ({kinds}{extra})"


def check(params: dict, ctx: ActionContext) -> str:
    client = Reddit(params, ctx)
    client.login()
    me = client.call("GET", "/api/v1/me").raise_for_status().json()
    return f"Reddit: u/{me.get('name')} olarak giriş tamam"


def _ids_from_file(path, kind_hint: str | None) -> list[str]:
    kind = kind_hint or ("t1" if "comment" in str(path).lower() else "t3")
    prefix = {"comment": "t1", "comments": "t1", "post": "t3", "posts": "t3"}.get(kind, kind)
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [f"{prefix}_{row['id'].strip()}" for row in csv.DictReader(f) if (row.get("id") or "").strip()]


def run_wipe(params: dict, ctx: ActionContext) -> dict:
    client = Reddit(params, ctx)
    client.login()
    text = params.get("overwrite_text", ".") if params.get("overwrite", True) else None
    kinds = params.get("kinds", ["comments", "submitted"])
    sorts = params.get("sorts", DEFAULT_SORTS)
    max_passes = int(params.get("max_passes", 10))
    count = ctx.memory.get("count", 0)
    seen: set[str] = set()
    verb = "silinecek" if ctx.dry_run else "silindi"

    def stop() -> dict:
        ctx.memory["count"] = count
        return result(INCOMPLETE, f"{count} öğe {verb}; süre doldu, sonraki çalıştırmada devam edecek")

    for _ in range(1 if ctx.dry_run else max_passes):
        found = 0
        for kind in kinds:
            for sort in sorts:
                for item in client.listing(kind, sort):
                    name = item["name"]
                    if name in seen:
                        continue
                    seen.add(name)
                    if ctx.out_of_time():
                        return stop()
                    editable = name.startswith("t1_") or bool(item.get("is_self"))
                    if not ctx.dry_run:
                        client.scrub(name, editable, text)
                    found += 1
                    count += 1
        ctx.memory["count"] = count
        if found == 0:
            break

    # Veri dışa aktarımındaki kimlikler; hangi satırda kaldığımızı hafızada tutarız.
    offsets = ctx.memory.setdefault("files", {})
    for spec in params.get("ids_files", []):
        path = spec["path"] if isinstance(spec, dict) else spec
        kind = spec.get("kind") if isinstance(spec, dict) else None
        ids = _ids_from_file(ctx.path(path), kind)
        start = offsets.get(str(path), 0)
        for i, fullname in enumerate(ids[start:], start):
            if ctx.out_of_time():
                offsets[str(path)] = i
                return stop()
            if not ctx.dry_run:
                client.scrub(fullname, True, text)
            count += 1
        if not ctx.dry_run:
            offsets[str(path)] = len(ids)

    ctx.memory["count"] = count
    return result(DONE, f"u/{client.username}: {count} öğe {verb}")
