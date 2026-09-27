from pathlib import Path

import pytest

from src.pipeline import ETLPipeline, ExtractedItemSchema
from src.stealth import stealth_engine


@pytest.fixture
def pipeline_instance(tmp_path: Path) -> ETLPipeline:
    return ETLPipeline(output_dir=str(tmp_path))


def test_pydantic_schema_validation_success(pipeline_instance: ETLPipeline):
    mock_raw_data = {
        "url": "https://example.com",
        "title": "  Example Domain  ",
        "status_code": 200,
        "html": "<html><body><h1>Example Domain</h1></body></html>",
        "success": True,
    }

    validated_item = pipeline_instance.process_raw_payload(mock_raw_data)

    assert isinstance(validated_item, ExtractedItemSchema)
    assert validated_item.title == "Example Domain"
    assert validated_item.status_code == 200
    assert validated_item.content_length > 0


def test_pydantic_schema_validation_failure(pipeline_instance: ETLPipeline):
    invalid_raw_data = {
        "url": "not-a-valid-url",
        "title": "",
        "status_code": 999,
        "html": "",
        "success": False,
    }

    assert pipeline_instance.process_raw_payload(invalid_raw_data) is None


def test_target_allowlist_blocks_unconfigured_host():
    with pytest.raises(PermissionError):
        stealth_engine.validate_target("https://example.com")


def test_target_allowlist_accepts_localhost():
    stealth_engine.validate_target("http://localhost:8765/")


@pytest.mark.asyncio
async def test_exports_json_and_csv(pipeline_instance: ETLPipeline):
    item = pipeline_instance.process_raw_payload(
        {
            "url": "http://localhost:8765/",
            "title": " Local Demo ",
            "status_code": 200,
            "html": "<h1>Local Demo</h1>",
            "success": True,
        }
    )
    assert item is not None

    json_path = await pipeline_instance.export_to_json([item])
    csv_path = await pipeline_instance.export_to_csv([item])

    assert json_path.exists()
    assert csv_path.exists()
    assert json_path.stat().st_size > 0
    assert csv_path.stat().st_size > 0
