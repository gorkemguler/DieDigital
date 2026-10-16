"""GitHub: kendi repolarını ve gist'lerini siler, profili boşaltır; en sonda bu deponun kendisini siler.

Gerekli token (klasik PAT): repo, delete_repo, gist ve (profil için) user kapsamları.
Fine-grained token kullanıyorsan: Administration (yazma), Gists (yazma), Profile (yazma).
"""

from __future__ import annotations

from fnmatch import fnmatch

from .. import net
from . import DONE, INCOMPLETE, ActionContext, ActionError, result

API = "https://api.github.com"
DEFAULT_TOKEN_ENV = "GH_WIPE_TOKEN"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _token(params: dict, ctx: ActionContext) -> str:
    return ctx.secret(params.get("token_env", DEFAULT_TOKEN_ENV))


def _get(url: str, token: str, ctx: ActionContext, **params) -> net.Response:
    r = net.request("GET", url, headers=_headers(token), params=params, max_wait=ctx.wait_budget())
    if r.status == 401:
        raise ActionError("GitHub token geçersiz veya süresi dolmuş.")
    return r.raise_for_status()


def _paginate(url: str, token: str, ctx: ActionContext, **params) -> list[dict]:
    items, page = [], 1
    while True:
        batch = _get(url, token, ctx, per_page=100, page=page, **params).json() or []
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def _matches(repo: dict, include: list[str], exclude: list[str]) -> bool:
    names = (repo["full_name"].lower(), repo["name"].lower())
    hit = lambda patterns: any(fnmatch(n, p.lower()) for n in names for p in patterns)
    return hit(include) and not hit(exclude)


def describe_wipe(params: dict) -> str:
    parts = []
    if params.get("repos", True):
        inc = ", ".join(params.get("include", ["*"]))
        exc = ", ".join(params.get("exclude", []))
        parts.append(f"GitHub repolarını sil ({inc}{f'; hariç: {exc}' if exc else ''})")
    if params.get("gists", True):
        parts.append("gist'leri sil")
    if params.get("scrub_profile", False):
        parts.append("profil bilgilerini boşalt")
    return ", ".join(parts) or "GitHub: hiçbir şey seçilmedi"


def check_wipe(params: dict, ctx: ActionContext) -> str:
    token = _token(params, ctx)
    r = _get(f"{API}/user", token, ctx)
    login = r.json()["login"]
    scopes = r.headers.get("x-oauth-scopes")
    if scopes is not None:  # klasik token; fine-grained token bu başlığı göndermez
        have = {s.strip() for s in scopes.split(",")}
        need = set()
        if params.get("repos", True):
            need.add("delete_repo")
        if params.get("gists", True):
            need.add("gist")
        if params.get("scrub_profile", False):
            need.add("user")
        missing = need - have
        if missing:
            raise ActionError(f"Token'da eksik kapsam: {', '.join(sorted(missing))}")
    return f"GitHub: {login} olarak erişim tamam"


def run_wipe(params: dict, ctx: ActionContext) -> dict:
    token = _token(params, ctx)
    login = _get(f"{API}/user", token, ctx).json()["login"]
    self_repo = (ctx.environ.get("GITHUB_REPOSITORY") or "").lower()
    include = params.get("include", ["*"])
    exclude = params.get("exclude", [])
    verb = "silinecek" if ctx.dry_run else "silindi"
    repos = gists = 0

    if params.get("repos", True):
        for repo in _paginate(f"{API}/user/repos", token, ctx, affiliation="owner"):
            name = repo["full_name"]
            if name.lower() == self_repo:
                ctx.log(f"  {name} atlandı (bu depo en sonda self_destruct ile silinir)")
                continue
            if not _matches(repo, include, exclude):
                continue
            if ctx.out_of_time():
                return result(INCOMPLETE, f"{repos} repo, {gists} gist {verb}; süre doldu")
            if not ctx.dry_run:
                r = net.request("DELETE", f"{API}/repos/{name}", headers=_headers(token), max_wait=ctx.wait_budget())
                if r.status == 403:
                    raise ActionError(f"{name} silinemedi: yetki yok (delete_repo kapsamı?)")
                if r.status not in (204, 404):
                    r.raise_for_status()
            ctx.log(f"  repo {verb}: {name}")
            repos += 1

    if params.get("gists", True):
        for gist in _paginate(f"{API}/gists", token, ctx):
            if ctx.out_of_time():
                return result(INCOMPLETE, f"{repos} repo, {gists} gist {verb}; süre doldu")
            if not ctx.dry_run:
                r = net.request("DELETE", f"{API}/gists/{gist['id']}", headers=_headers(token), max_wait=ctx.wait_budget())
                if r.status not in (204, 404):
                    r.raise_for_status()
            ctx.log(f"  gist {verb}: {gist.get('description') or gist['id']}")
            gists += 1

    if params.get("scrub_profile", False):
        blank = {"name": "", "bio": "", "blog": "", "company": "", "location": "", "twitter_username": "", "hireable": False}
        if not ctx.dry_run:
            net.request("PATCH", f"{API}/user", headers=_headers(token), json_body=blank).raise_for_status()
        ctx.log(f"  profil bilgileri {'boşaltılacak' if ctx.dry_run else 'boşaltıldı'}")

    return result(DONE, f"{login}: {repos} repo, {gists} gist {verb}")


def _self_repo(params: dict, ctx: ActionContext) -> str:
    repo = params.get("repo") or ctx.environ.get("GITHUB_REPOSITORY")
    if not repo:
        raise ActionError("Silinecek depo bilinmiyor: 'repo' parametresini \"kullanıcı/depo\" olarak ver.")
    return repo


def describe_self_destruct(params: dict) -> str:
    return f"bu depoyu sil ({params.get('repo') or 'GITHUB_REPOSITORY'})"


def check_self_destruct(params: dict, ctx: ActionContext) -> str:
    token = _token(params, ctx)
    repo = _self_repo(params, ctx)
    data = _get(f"{API}/repos/{repo}", token, ctx).json()
    if not (data.get("permissions") or {}).get("admin"):
        raise ActionError(f"Token'ın {repo} üzerinde yönetici yetkisi yok; depo silinemez.")
    return f"{repo} silinebilir"


def run_self_destruct(params: dict, ctx: ActionContext) -> dict:
    token = _token(params, ctx)
    repo = _self_repo(params, ctx)
    if ctx.dry_run:
        return result(DONE, f"{repo} silinecek")
    r = net.request("DELETE", f"{API}/repos/{repo}", headers=_headers(token), max_wait=ctx.wait_budget())
    if r.status == 403:
        raise ActionError(f"{repo} silinemedi: yetki yok")
    if r.status not in (204, 404):
        r.raise_for_status()
    return result(DONE, f"{repo} silindi")
