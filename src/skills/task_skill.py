"""Task skill helpers for Claude agent.

Each skill contains a prompt template that Claude can invoke by name.
This file provides helper functions that can be referenced from the agent prompt.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from src.utils.vault import list_tasks, move_task, vault_path


def list_needs_action() -> List[str]:
    tasks = list_tasks("Needs_Action")
    return [t.name for t in tasks]


def read_task(task_name: str) -> str:
    path = vault_path("Needs_Action", task_name)
    return path.read_text(encoding="utf-8")


def complete_task(task_name: str) -> None:
    """Mark a task as completed by moving it to Done."""
    path = vault_path("Needs_Action", task_name)
    move_task(path, "Done")


def require_approval(task_name: str) -> None:
    """Move a task to Pending_Approval."""
    path = vault_path("Needs_Action", task_name)
    move_task(path, "Pending_Approval")


def approve_task(task_name: str) -> None:
    path = vault_path("Pending_Approval", task_name)
    move_task(path, "Approved")


def reject_task(task_name: str) -> None:
    path = vault_path("Pending_Approval", task_name)
    move_task(path, "Rejected")
