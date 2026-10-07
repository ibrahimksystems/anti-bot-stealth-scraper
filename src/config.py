<<<<<<< HEAD
=======
from typing import Optional

>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    """Runtime configuration for authorized browser-based data extraction."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AuthorizedDataExtractionEngine"
    DEBUG: bool = False

    HEADLESS: bool = True
    HUMANIZE: bool = True
    TARGET_OS: str = "windows"
    LOCALE: str = "en-US"

<<<<<<< HEAD
    PROXY_SERVER: str | None = Field(
=======
    PROXY_SERVER: Optional[str] = Field(
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
        default=None,
        description="Operator-controlled proxy for an authorized environment.",
    )
    TIMEOUT_SECONDS: int = 30000

    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: float = 2.0

    # Safety-by-default: demonstrations and fresh installations may only target
    # explicitly allowed hosts. Expand this list only for systems the operator
    # is authorized to access.
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"

    def allowed_hosts(self) -> set[str]:
<<<<<<< HEAD
        return {host.strip().lower() for host in self.ALLOWED_HOSTS.split(",") if host.strip()}
=======
        return {
            host.strip().lower()
            for host in self.ALLOWED_HOSTS.split(",")
            if host.strip()
        }
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97


settings = ScraperSettings()
