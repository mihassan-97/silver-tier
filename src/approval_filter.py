from __future__ import annotations

from pathlib import Path

VAULT = Path("Vault")


def requires_approval(task_content: str) -> bool:
    keywords = ["payment", "send email", "invoice"]
    return any(k in task_content.lower() for k in keywords)


def create_approval_file(task_file: Path, content: str) -> None:
    approval_path = VAULT / "Pending_Approval" / task_file.name
    approval_path.write_text(content, encoding="utf-8")
    print("Approval required:", approval_path)


def filter_tasks_for_approval(tasks: list[Path]) -> list[Path]:
    """Move tasks needing approval to Pending_Approval and return remaining tasks."""
    remaining: list[Path] = []
    for task in tasks:
        content = task.read_text(encoding="utf-8")
        if requires_approval(content):
            create_approval_file(task, content)
            task.unlink()  # remove from Needs_Action
        else:
            remaining.append(task)
    return remaining
