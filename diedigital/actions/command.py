"""Serbest komut: araçta karşılığı olmayan işler için (ör. `rclone purge`, kendi betiğin)."""

from __future__ import annotations

import shlex
import shutil
import subprocess

from . import DONE, ActionContext, ActionError, result


def _argv(params: dict) -> list[str]:
    argv = params.get("argv")
    if isinstance(argv, str):
        argv = shlex.split(argv)
    if not argv:
        raise ActionError("'argv' boş.")
    return [str(a) for a in argv]


def describe(params: dict) -> str:
    return f"komut çalıştır: {' '.join(_argv(params))}"


def check(params: dict, ctx: ActionContext) -> str:
    argv = _argv(params)
    if not shutil.which(argv[0]) and not ctx.path(argv[0]).exists():
        raise ActionError(f"Komut bulunamadı: {argv[0]}")
    return f"{argv[0]} bulundu"


def run(params: dict, ctx: ActionContext) -> dict:
    argv = _argv(params)
    if ctx.dry_run:
        return result(DONE, f"çalıştırılacak: {' '.join(argv)}")
    timeout = min(float(params.get("timeout_minutes", 60)) * 60, max(ctx.remaining() - 60, 60))
    try:
        proc = subprocess.run(argv, cwd=ctx.base_dir, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise ActionError(f"Komut zaman aşımına uğradı: {argv[0]}") from e
    except OSError as e:
        raise ActionError(f"Komut çalıştırılamadı: {e}") from e
    if proc.returncode != 0:
        raise ActionError(f"Komut {proc.returncode} koduyla bitti: {' '.join(argv)}")
    return result(DONE, f"çalıştı: {' '.join(argv)}")
