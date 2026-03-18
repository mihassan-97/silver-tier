"""Background scheduler for periodic tasks.

This script runs a simple scheduler that:
- creates a LinkedIn post task every day at 10:00
- runs approved actions every minute

Run:
    python -m src.scheduled_runner
"""

from __future__ import annotations

import time

import schedule

from src.agents.linkedin_agent import create_linkedin_task
from src.approval_executor import process_approved


def main() -> None:
    schedule.every().day.at("10:00").do(create_linkedin_task)
    schedule.every(1).minutes.do(process_approved)

    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()
