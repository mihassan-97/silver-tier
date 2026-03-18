"""Configuration and environment helpers."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Vault and file paths
    VAULT_PATH: Path = Path("Vault")

    # Claude (Anthropic)
    CLAUDE_API_KEY: str | None = None
    CLAUDE_MODEL: str = "claude-2.1"


    # Gmail (optional)
    GMAIL_CREDENTIALS_PATH: Path = Path("credentials.json")
    GMAIL_TOKEN_PATH: Path = Path("state/gmail_token.json")
    GMAIL_USER_ID: str = "me"

    # Email sending (for MCP server actions)
    EMAIL_SMTP_HOST: str | None = None
    EMAIL_SMTP_PORT: int | None = None
    EMAIL_SMTP_USER: str | None = None
    EMAIL_SMTP_PASS: str | None = None

    # File system watcher
    WATCH_FOLDER: Path | None = None

    # LinkedIn automation
    LINKEDIN_EMAIL: str | None = None
    LINKEDIN_PASSWORD: str | None = None

    # Scheduling
    DAILY_SCHEDULE_CRON: str = "0 9 * * *"
    WEEKLY_SUMMARY_CRON: str = "0 17 * * MON"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

