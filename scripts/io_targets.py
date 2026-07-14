#!/usr/bin/env python3
"""
Helpers for reading/writing local files or ssh:// targets.
"""

from __future__ import annotations

import os
import posixpath
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import unquote, urlparse


def _parse_ssh_target(target: str) -> Optional[Tuple[str, Optional[int], str]]:
    raw = str(target)
    parsed = urlparse(raw)
    if parsed.scheme != "ssh":
        return None
    if not parsed.hostname:
        raise ValueError(f"ssh target is missing a host: {raw}")
    if not parsed.path or not parsed.path.startswith("/"):
        raise ValueError(f"ssh target must include an absolute path: {raw}")
    host = parsed.hostname
    if parsed.username:
        host = f"{parsed.username}@{host}"
    return host, parsed.port, unquote(parsed.path)


def _ssh_cmd(host: str, port: Optional[int], remote_cmd: str) -> list[str]:
    cmd = ["ssh", "-o", "BatchMode=yes"]
    control_path = os.environ.get("EXPLAINRX_SSH_CONTROL_PATH", "").strip()
    if control_path:
        cmd.extend(["-S", control_path])
    if port:
        cmd.extend(["-p", str(port)])
    cmd.extend([host, remote_cmd])
    return cmd


def _run_ssh(host: str, port: Optional[int], remote_cmd: str, input_bytes: Optional[bytes] = None) -> bytes:
    proc = subprocess.run(
        _ssh_cmd(host, port, remote_cmd),
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"ssh command failed ({proc.returncode}): {stderr or remote_cmd}")
    return proc.stdout


def read_text(target: str, encoding: str = "utf-8") -> str:
    parsed = _parse_ssh_target(str(target))
    if not parsed:
        path = Path(target)
        if not path.exists():
            return ""
        return path.read_text(encoding=encoding)
    host, port, remote_path = parsed
    remote_cmd = f"if [ -f {sh_quote(remote_path)} ]; then cat {sh_quote(remote_path)}; fi"
    return _run_ssh(host, port, remote_cmd).decode(encoding, errors="replace")


def append_text(target: str, text: str, encoding: str = "utf-8") -> None:
    parsed = _parse_ssh_target(str(target))
    if not parsed:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding=encoding) as fh:
            fh.write(text)
        return

    host, port, remote_path = parsed
    parent = posixpath.dirname(remote_path)
    lock_path = f"{remote_path}.lock"
    remote_cmd = (
        "set -euo pipefail\n"
        f"mkdir -p {sh_quote(parent)}\n"
        "if command -v flock >/dev/null 2>&1; then\n"
        f"  exec 9>>{sh_quote(lock_path)}\n"
        "  flock -x 9\n"
        "fi\n"
        f"cat >> {sh_quote(remote_path)}\n"
    )
    _run_ssh(host, port, remote_cmd, input_bytes=text.encode(encoding))


def write_text_atomic(target: str, text: str, encoding: str = "utf-8") -> None:
    write_bytes_atomic(target, text.encode(encoding))


def write_bytes_atomic(target: str, data: bytes) -> None:
    parsed = _parse_ssh_target(str(target))
    if not parsed:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        tmp.replace(path)
        return

    host, port, remote_path = parsed
    parent = posixpath.dirname(remote_path)
    lock_path = f"{remote_path}.lock"
    tmp_path = f"{remote_path}.tmp.{os.getpid()}"
    remote_cmd = (
        "set -euo pipefail\n"
        f"mkdir -p {sh_quote(parent)}\n"
        f"cat > {sh_quote(tmp_path)}\n"
        "if command -v flock >/dev/null 2>&1; then\n"
        f"  exec 9>>{sh_quote(lock_path)}\n"
        "  flock -x 9\n"
        "fi\n"
        f"mv {sh_quote(tmp_path)} {sh_quote(remote_path)}\n"
    )
    _run_ssh(host, port, remote_cmd, input_bytes=data)


def copy_target_to_local(target: str, local_path: Path) -> None:
    parsed = _parse_ssh_target(str(target))
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if not parsed:
        src = Path(target)
        if not src.exists():
            local_path.write_text("")
            return
        shutil.copyfile(src, local_path)
        return
    local_path.write_text(read_text(target), encoding="utf-8")


def sh_quote(text: str) -> str:
    return "'" + text.replace("'", "'\"'\"'") + "'"
