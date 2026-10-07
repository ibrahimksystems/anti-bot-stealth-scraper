import asyncio
import logging
<<<<<<< HEAD
from typing import Any
=======
from typing import Optional, Dict, Any
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
from urllib.parse import urlparse

from camoufox.async_api import AsyncCamoufox

from src.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(settings.APP_NAME)


class StealthEngine:
    """Authorized browser automation engine for permitted data-extraction targets.

    The engine is safety-by-default: only hosts listed in ALLOWED_HOSTS may be
    contacted. Anti-bot or access-control bypass is not a project objective.
    """

    def __init__(self):
        self.settings = settings

    def validate_target(self, url: str) -> None:
        """Allow only explicitly configured hosts and HTTP(S) URLs."""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Target must be an absolute HTTP(S) URL.")

        host = parsed.hostname.lower()
        if host not in self.settings.allowed_hosts():
            raise PermissionError(
                f"Target host '{host}' is not in ALLOWED_HOSTS. "
                "Only authorized targets may be configured."
            )

    async def fetch_page_content(
        self,
        url: str,
<<<<<<< HEAD
        wait_selector: str | None = None,
    ) -> dict[str, Any]:
=======
        wait_selector: Optional[str] = None,
    ) -> Dict[str, Any]:
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
        """Fetch a permitted page and return structured browser metadata."""
        self.validate_target(url)

        proxy_config = None
        if self.settings.PROXY_SERVER:
            proxy_config = {"server": self.settings.PROXY_SERVER}

        retries = 0
        while retries <= self.settings.MAX_RETRIES:
            try:
                logger.info(
                    "Authorized browser request (attempt %s/%s): %s",
                    retries + 1,
                    self.settings.MAX_RETRIES + 1,
                    url,
                )

                async with AsyncCamoufox(
                    headless=self.settings.HEADLESS,
                    humanize=self.settings.HUMANIZE,
                    os=self.settings.TARGET_OS,
                    proxy=proxy_config,
                    locale=self.settings.LOCALE,
                ) as browser:
                    page = await browser.new_page()
                    response = await page.goto(
                        url,
                        timeout=self.settings.TIMEOUT_SECONDS,
                        wait_until="domcontentloaded",
                    )

                    if wait_selector:
                        await page.wait_for_selector(
                            wait_selector,
                            timeout=self.settings.TIMEOUT_SECONDS,
                        )

                    status_code = response.status if response else 0
                    content = await page.content()
                    title = await page.title()

                    logger.info(
                        "Extraction completed. Title: '%s' | Status: %s",
                        title,
                        status_code,
                    )
                    return {
                        "url": url,
                        "status_code": status_code,
                        "title": title,
                        "html": content,
                        "success": 200 <= status_code < 400,
                    }

            except Exception as exc:
                retries += 1
                if retries > self.settings.MAX_RETRIES:
                    logger.error("Maximum retry attempts reached: %s", exc)
                    return {
                        "url": url,
                        "status_code": 0,
                        "error": str(exc),
                        "success": False,
                    }

                sleep_time = self.settings.BACKOFF_FACTOR ** (retries - 1)
                logger.info(
                    "Request failed; retrying in %.1f seconds: %s",
                    sleep_time,
                    exc,
                )
                await asyncio.sleep(sleep_time)

<<<<<<< HEAD
        return {
            "url": url,
            "status_code": 0,
            "error": "Max retries exceeded without result.",
            "success": False,
        }


stealth_engine = StealthEngine()
=======

stealth_engine = StealthEngine()
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
