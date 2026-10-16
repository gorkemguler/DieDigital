"""Küçük HTTP istemcisi: yeniden deneme ve hız sınırı (rate limit) desteğiyle."""

from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Mapping

from . import __version__
from .util import parse_time

USER_AGENT = f"diedigital/{__version__}"
RETRY_STATUSES = {429, 500, 502, 503, 504}


class Response:
    def __init__(self, method: str, url: str, status: int, headers: Mapping[str, str], body: bytes):
        self.method = method
        self.url = url
        self.status = status
        self.headers = {k.lower(): v for k, v in headers.items()}
        self.body = body

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.body) if self.body else None

    def raise_for_status(self) -> "Response":
        if not self.ok:
            raise HTTPError(self)
        return self


class HTTPError(Exception):
    def __init__(self, response: Response):
        self.response = response
        super().__init__(
            f"HTTP {response.status} ({response.method} {response.url}): {response.text[:300]}"
        )


def retry_delay(headers: Mapping[str, str], attempt: int, now: float | None = None) -> float:
    """Sunucunun istediği bekleme süresi (saniye). Bilgi yoksa üstel geri çekilme."""
    now = time.time() if now is None else now
    headers = {k.lower(): v for k, v in headers.items()}

    value = headers.get("retry-after")
    if value:
        try:
            return max(0.0, float(value))
        except ValueError:
            try:
                return max(0.0, parsedate_to_datetime(value).timestamp() - now)
            except (TypeError, ValueError):
                pass

    reset = headers.get("x-ratelimit-reset")
    if reset:
        try:
            number = float(reset)
            # GitHub epoch saniyesi, Reddit "kaç saniye kaldı" gönderir.
            return max(0.0, number - now) if number > 1e9 else max(0.0, number)
        except ValueError:
            try:
                return max(0.0, parse_time(reset).timestamp() - now)  # Mastodon: ISO 8601
            except (TypeError, ValueError):
                pass

    return float(min(2 ** attempt, 60))


def request(
    method: str,
    url: str,
    *,
    headers: Mapping[str, str] | None = None,
    params: Mapping[str, Any] | None = None,
    json_body: Any = None,
    form: Mapping[str, Any] | None = None,
    data: bytes | None = None,
    auth: tuple[str, str] | None = None,
    timeout: float = 30,
    retries: int = 4,
    max_wait: float = 900,
    sleep: Callable[[float], None] = time.sleep,
) -> Response:
    """İsteği gönderir; 429/5xx ve ağ hatalarında bekleyip tekrar dener.

    Sunucu `max_wait` saniyeden uzun beklememizi isterse yanıtı olduğu gibi döndürür;
    bu durumda ne yapılacağına çağıran karar verir.
    """
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{url}{'&' if '?' in url else '?'}{query}"

    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json, */*"}
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    elif form is not None:
        data = urllib.parse.urlencode(form).encode("utf-8")
        hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    if auth:
        token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode("utf-8")).decode("ascii")
        hdrs["Authorization"] = f"Basic {token}"
    hdrs.update(headers or {})

    attempt = 0
    while True:
        req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = Response(method, url, r.status, dict(r.headers.items()), r.read())
        except urllib.error.HTTPError as e:
            resp = Response(method, url, e.code, dict(e.headers.items()), e.read())
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt >= retries:
                raise
            attempt += 1
            sleep(min(2 ** attempt, 60))
            continue

        if resp.status in RETRY_STATUSES and attempt < retries:
            delay = retry_delay(resp.headers, attempt + 1)
            if delay > max_wait:
                return resp
            attempt += 1
            sleep(delay + 1)
            continue
        return resp
