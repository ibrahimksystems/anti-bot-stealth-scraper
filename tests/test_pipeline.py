import pytest
import asyncio
from src.config import ScraperConfig
from src.stealth import AntiBotStealthEngine

@pytest.mark.asyncio
async def test_stealth_engine_execution():
    config = ScraperConfig(target_url="https://example.com")
    engine = AntiBotStealthEngine(config)
    result = await engine.execute_request()
    assert result["status"] == 200
    assert result["bypassed"] is True
