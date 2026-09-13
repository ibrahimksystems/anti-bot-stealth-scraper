import asyncio
import logging
from typing import Optional, Dict, Any
from camoufox.async_api import AsyncCamoufox
from src.config import settings

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(settings.APP_NAME)


class StealthEngine:
    """
    Anti-Bot Bypass Browser Engine powered by Camoufox and Playwright.
    """

    def __init__(self):
        self.settings = settings

    async def fetch_page_content(
        self, 
        url: str, 
        wait_selector: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Connects to the specified URL using a stealth browser, circumvents anti-bot measures, 
        and returns the raw HTML content along with request metadata.
        """
        proxy_config = None
        if self.settings.PROXY_SERVER:
            proxy_config = {"server": self.settings.PROXY_SERVER}

        retries = 0
        backoff = 1.0

        while retries <= self.settings.MAX_RETRIES:
            try:
                logger.info(f"Initiating stealth connection (Attempt {retries + 1}/{self.settings.MAX_RETRIES + 1}): {url}")

                async with AsyncCamoufox(
                    headless=self.settings.HEADLESS,
                    humanize=self.settings.HUMANIZE,
                    os=self.settings.TARGET_OS,
                    proxy=proxy_config,
                    locale=self.settings.LOCALE,
                ) as browser:
                    
                    page = await browser.new_page()
                    
                    # Navigate to target page and wait for DOM content
                    response = await page.goto(url, timeout=self.settings.TIMEOUT_SECONDS, wait_until="domcontentloaded")
                    
                    # Wait for specific selector if specified (e.g., post-captcha resolution element)
                    if wait_selector:
                        await page.wait_for_selector(wait_selector, timeout=self.settings.TIMEOUT_SECONDS)

                    status_code = response.status if response else 0

                    # Check for explicit Anti-Bot blocking status codes
                    if status_code in [403, 429]:
                        logger.warning(f"Anti-bot protection triggered! Status Code: {status_code}")
                        raise Exception(f"Anti-Bot Blocked: HTTP {status_code}")

                    content = await page.content()
                    title = await page.title()

                    logger.info(f"Successfully extracted payload. Title: '{title}' | Status: {status_code}")
                    return {
                        "url": url,
                        "status_code": status_code,
                        "title": title,
                        "html": content,
                        "success": True
                    }

            except Exception as e:
                retries += 1
                if retries > self.settings.MAX_RETRIES:
                    logger.error(f"Maximum retry attempts reached. Error: {str(e)}")
                    return {
                        "url": url,
                        "status_code": 0,
                        "error": str(e),
                        "success": False
                    }
                
                sleep_time = backoff * (self.settings.BACKOFF_FACTOR ** (retries - 1))
                logger.info(f"Request failed, retrying in {sleep_time} seconds... (Reason: {str(e)})")
                await asyncio.sleep(sleep_time)


# Singleton instance for global scope
stealth_engine = StealthEngine()