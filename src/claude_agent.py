"""Claude agent for processing tasks and generating plans."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.utils.claude import claude_complete
from src.utils.vault import (
    ensure_vault_structure,
    list_tasks,
    move_task,
    task_header,
    timestamp,
    vault_path,
)


def build_prompt(tasks: list[Path]) -> str:
    if not tasks:
        return "You are a personal AI assistant. There are no tasks to process."

    tasks_text = []
    for t in tasks:
        tasks_text.append(f"---\n{t.read_text(encoding='utf-8')}\n")

    prompt = (
        "You are a personal AI employee managing an Obsidian vault. "
        "A set of tasks has been placed into Vault/Needs_Action. "
        "For each task, provide a short plan with steps, prioritize items, and identify any sensitive actions that require human approval. "
        "Output a Markdown plan with headers and actionable steps. "
        "Also, if a task can be marked as completed, include a section 'Completed Tasks' listing the filenames.\n\n"
        "Here are the tasks:\n"
        + "\n".join(tasks_text)
        + "\nPlease produce a clear plan in Markdown." 
    )
    return prompt


def write_plan(plan_text: str) -> Path:
    ensure_vault_structure()
    plan_path = vault_path("Plans", "Plan.md")
    content = task_header("Plan", {"generated": timestamp()}) + plan_text.strip() + "\n"
    plan_path.write_text(content, encoding="utf-8")
    return plan_path


def process_tasks() -> None:
    ensure_vault_structure()
    tasks = list_tasks("Needs_Action")
    if not tasks:
        print("No tasks in Vault/Needs_Action.")
        return

    prompt = build_prompt(tasks)
    print(f"Calling Claude with {len(tasks)} task(s)...")
    plan = claude_complete(prompt)
    print("Claude response received. Writing plan...")
    write_plan(plan)

    # Move tasks to Done after processing to avoid duplicate work.
    for task in tasks:
        move_task(task, "Done")

    print(f"Moved {len(tasks)} task(s) to Vault/Done.")


if __name__ == "__main__":
    process_tasks()
