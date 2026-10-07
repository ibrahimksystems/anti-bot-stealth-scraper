import logging

from pydantic import BaseModel, Field

from src.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(settings.APP_NAME)


class ProxyConfig(BaseModel):
    """Pydantic v2 validated proxy configuration record."""

    url: str = Field(..., description="Proxy endpoint URL (e.g. http://proxy.example.com:8080)")
    is_active: bool = True
    latency_ms: float = 0.0
    fail_count: int = 0
    max_fails: int = 3


class DynamicProxyOrchestrator:
    """Enterprise proxy pool manager with health monitoring and failover routing."""

    def __init__(self, raw_proxies: list[str] | None = None):
        self.settings = settings
        self._pool: list[ProxyConfig] = []

        if raw_proxies:
            for p_url in raw_proxies:
                self.add_proxy(p_url)
        elif self.settings.PROXY_SERVER:
            self.add_proxy(self.settings.PROXY_SERVER)

    def add_proxy(self, proxy_url: str) -> None:
        """Add a new proxy endpoint to the orchestrator pool."""
        try:
            proxy_config = ProxyConfig(url=proxy_url)
            self._pool.append(proxy_config)
            logger.info("Proxy registered to orchestrator pool: %s", proxy_url)
        except Exception as exc:
            logger.error("Failed to register proxy '%s': %s", proxy_url, exc)

    async def get_next_proxy(self) -> ProxyConfig | None:
        """Fetch the next healthy proxy from the pool using Round-Robin routing."""
        active_proxies = [p for p in self._pool if p.is_active and p.fail_count < p.max_fails]
        if not active_proxies:
            logger.warning("No healthy active proxies available in orchestrator pool.")
            return None

        # Sort by lowest fail count first, then latency
        active_proxies.sort(key=lambda x: (x.fail_count, x.latency_ms))
        selected = active_proxies[0]
        return selected

    async def report_status(self, proxy_url: str, success: bool, latency_ms: float = 0.0) -> None:
        """Report execution status of a proxy to update pool health metrics."""
        for proxy in self._pool:
            if proxy.url == proxy_url:
                if success:
                    proxy.fail_count = 0
                    proxy.latency_ms = latency_ms
                    logger.debug("Proxy %s health updated (Latency: %.2fms)", proxy_url, latency_ms)
                else:
                    proxy.fail_count += 1
                    logger.warning(
                        "Proxy %s reported failure (%d/%d)",
                        proxy_url,
                        proxy.fail_count,
                        proxy.max_fails,
                    )
                    if proxy.fail_count >= proxy.max_fails:
                        proxy.is_active = False
                        logger.error("Proxy %s marked as inactive/unhealthy.", proxy_url)
                break


proxy_orchestrator = DynamicProxyOrchestrator()
