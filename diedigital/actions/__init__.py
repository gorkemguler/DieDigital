"""Silme eylemleri. Hem `diedigital wipe ...` komutları hem de ölü adam anahtarı bunları kullanır.

Her eylem tipi üç fonksiyon sağlar:
  run(params, ctx)      -> {"status": done|incomplete, "summary": "..."}; hata durumunda ActionError
  check(params, ctx)    -> ön kontrol (kimlik bilgileri geçerli mi?), metin döndürür
  describe(params)      -> insanların okuyacağı tek satırlık açıklama

`incomplete` dönen eylem bir sonraki çalıştırmada kaldığı yerden devam eder; `ctx.memory`
çalıştırmalar arasında saklanır.
"""

from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

DONE = "done"
INCOMPLETE = "incomplete"
FAILED = "failed"
GAVE_UP = "gave_up"


class ActionError(Exception):
    pass


class ActionContext:
    def __init__(self, *, dry_run: bool = True, memory: dict | None = None, deadline: float | None = None,
                 environ: Mapping[str, str] | None = None, log: Callable[[str], None] | None = None,
                 base_dir: str | Path = ".", sleep: Callable[[float], None] = time.sleep):
        self.dry_run = dry_run
        self.memory = memory if memory is not None else {}
        self.deadline = deadline
        self.environ = environ if environ is not None else os.environ
        self.log = log or (lambda msg: print(msg, flush=True))
        self.base_dir = Path(base_dir)
        self.sleep = sleep

    def remaining(self) -> float:
        return math.inf if self.deadline is None else self.deadline - time.monotonic()

    def out_of_time(self, reserve: float = 60) -> bool:
        return self.remaining() <= reserve

    def wait_budget(self, reserve: float = 120) -> float:
        """Hız sınırı için en fazla ne kadar beklenebilir."""
        return max(0.0, min(self.remaining() - reserve, 3600.0))

    def secret(self, name: str, required: bool = True) -> str | None:
        value = self.environ.get(name) or None
        if required and not value:
            raise ActionError(f"'{name}' ortam değişkeni tanımlı değil.")
        return value

    def path(self, value: str | Path) -> Path:
        p = Path(value)
        return p if p.is_absolute() else self.base_dir / p


def result(status: str, summary: str) -> dict:
    return {"status": status, "summary": summary}


@dataclass
class ActionSpec:
    run: Callable[[dict, ActionContext], dict]
    check: Callable[[dict, ActionContext], str]
    describe: Callable[[dict], str]


def registry() -> dict[str, ActionSpec]:
    from . import command, github, mail, mastodon, reddit

    return {
        "github_wipe": ActionSpec(github.run_wipe, github.check_wipe, github.describe_wipe),
        "self_destruct": ActionSpec(github.run_self_destruct, github.check_self_destruct, github.describe_self_destruct),
        "reddit_wipe": ActionSpec(reddit.run_wipe, reddit.check, reddit.describe),
        "mastodon_wipe": ActionSpec(mastodon.run_wipe, mastodon.check, mastodon.describe),
        "send_letters": ActionSpec(mail.run_send_letters, mail.check_send_letters, mail.describe_send_letters),
        "email": ActionSpec(mail.run_email, mail.check_email, mail.describe_email),
        "command": ActionSpec(command.run, command.check, command.describe),
    }
