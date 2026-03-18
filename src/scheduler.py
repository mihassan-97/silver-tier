"""Scheduling helpers (daily processing, weekly summary)."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.vault import list_tasks, task_header, vault_path


def daily_processing() -> None:
    """Run the daily processing pipeline."""
    # This will process tasks and generate a plan.
    from src.claude_agent import process_tasks

    process_tasks()


def weekly_summary() -> None:
    """Generate a weekly summary of completed tasks."""
    done_tasks = list_tasks("Done")
    if not done_tasks:
        print("No completed tasks to summarize.")
        return

    # Sort by modification time, newest first.
    done_tasks.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    recent = done_tasks[:20]

    text_lines = ["# Weekly Summary\n"]
    text_lines.append(f"Generated: {datetime.utcnow().isoformat()}\n")
    text_lines.append("## Most recent completed tasks\n")

    for task in recent:
        text_lines.append(f"- {task.name} (last modified: {datetime.utcfromtimestamp(task.stat().st_mtime).isoformat()})")

    summary_path = vault_path("Plans", "Weekly_Summary.md")
    summary_path.write_text("\n".join(text_lines), encoding="utf-8")
    print(f"Written weekly summary to {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scheduler helper for the Personal AI Employee.")
    parser.add_argument("command", choices=["daily", "weekly"], help="Which schedule to run.")
    args = parser.parse_args()

    if args.command == "daily":
        daily_processing()
    elif args.command == "weekly":
        weekly_summary()


if __name__ == "__main__":
    main()
