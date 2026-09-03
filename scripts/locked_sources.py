#!/usr/bin/env python3
"""Fetch immutable, explicitly licensed source revisions (never upstream HEAD)."""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get_sources() -> dict:
    sources = json.loads((ROOT / "sources.lock.json").read_text(encoding="utf-8"))
    for key, source in sources.items():
        if not re.fullmatch(r"[a-z0-9_]+", key):
            raise ValueError(f"Invalid source key: {key}")
        repository = source.get("repository", "")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError(f"Invalid repository for {key}")
        if source.get("url") != f"https://github.com/{repository}":
            raise ValueError(f"Unexpected source URL for {key}")
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            raise ValueError(f"Source {key} must use a full immutable commit SHA")
        if not source.get("license"):
            raise ValueError(f"Missing source license for {key}")
    return sources


def clone_locked(key: str, destination: Path, sparse: list[str] | None = None) -> None:
    source = get_sources()[key]
    commit = source["commit"]
    # Optional local cache for repeated verification. Never trust a dirty or
    # differently pinned checkout. The temporary symlink is safe to remove.
    cache_root = os.environ.get("LEETCODE_SOURCE_CACHE")
    if cache_root:
        cached = Path(cache_root).resolve() / key
        if cached.is_dir():
            head = subprocess.check_output(["git", "-C", str(cached), "rev-parse", "HEAD"], text=True).strip()
            dirty = subprocess.check_output(["git", "-C", str(cached), "status", "--porcelain"], text=True)
            if head != commit or dirty:
                raise ValueError(f"Cache {key} must be clean and pinned at {commit}")
            destination.symlink_to(cached, target_is_directory=True)
            return

    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(destination), *args], check=True,
                       stdout=subprocess.DEVNULL)

    subprocess.run(["git", "init", "--quiet", str(destination)], check=True)
    git("remote", "add", "origin", source["url"] + ".git")
    if sparse:
        git("sparse-checkout", "init", "--cone")
        git("sparse-checkout", "set", *sparse)
    git("fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", commit)
    git("checkout", "--quiet", "--detach", commit)
    actual = subprocess.check_output(["git", "-C", str(destination), "rev-parse", "HEAD"], text=True).strip()
    if actual != commit:
        raise RuntimeError(f"Source checkout mismatch for {key}: {actual}")


def safe_source_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Source path escapes checkout: {relative}")
    return path
