"""Vault helpers for reading/writing task markdown files."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from src.config import settings


def vault_path(*parts: str) -> Path:
    """Get a Path inside the vault."""
    return settings.VAULT_PATH.joinpath(*parts)


def ensure_vault_structure() -> None:
    """Ensure the vault folders exist."""
    for sub in [
        "Inbox",
        "Needs_Action",
        "Done",
        "Plans",
        "Pending_Approval",
        "Approved",
        "Rejected",
    ]:
        vault_path(sub).mkdir(parents=True, exist_ok=True)


def list_tasks(folder: str) -> list[Path]:
    """List markdown tasks in a vault folder."""
    base = vault_path(folder)
    if not base.exists():
        return []
    return sorted([p for p in base.glob("*.md") if p.is_file()])


def write_task(folder: str, name: str, content: str) -> Path:
    """Write a markdown task file and return its path."""
    ensure_vault_structure()
    path = vault_path(folder, name)
    path.write_text(content, encoding="utf-8")
    return path


def move_task(src: Path, dest_folder: str) -> Path:
    """Move a task file from one vault folder to another."""
    ensure_vault_structure()
    dest = vault_path(dest_folder, src.name)
    src.replace(dest)
    return dest


def timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")


def task_header(title: str, metadata: dict[str, str] | None = None) -> str:
    metadata = metadata or {}
    meta_lines = "\n".join(f"- **{k}**: {v}" for k, v in metadata.items())
    return f"# {title}\n\n{meta_lines}\n\n" if metadata else f"# {title}\n\n"


def normalize_filename(title: str) -> str:
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in title)
    return safe[:200] + ".md" if not safe.endswith(".md") else safe
