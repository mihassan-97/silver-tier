"""Run approval workflow (execute approved actions)."""

from __future__ import annotations

from src.approval import execute_approved_actions


def main() -> None:
    execute_approved_actions()


if __name__ == "__main__":
    main()
