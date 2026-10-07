import pytest

from src.proxy_manager import DynamicProxyOrchestrator


@pytest.mark.asyncio
async def test_proxy_addition_and_retrieval():
    orchestrator = DynamicProxyOrchestrator(["http://127.0.0.1:8080"])
    proxy = await orchestrator.get_next_proxy()

    assert proxy is not None
    assert proxy.url == "http://127.0.0.1:8080"
    assert proxy.is_active is True


@pytest.mark.asyncio
async def test_proxy_health_degradation_and_failover():
    orchestrator = DynamicProxyOrchestrator(["http://127.0.0.1:8081"])
    proxy_url = "http://127.0.0.1:8081"

    # Report 3 consecutive failures to trigger deactivate
    await orchestrator.report_status(proxy_url, success=False)
    await orchestrator.report_status(proxy_url, success=False)
    await orchestrator.report_status(proxy_url, success=False)

    next_proxy = await orchestrator.get_next_proxy()
    assert next_proxy is None  # No active proxy left
