import pytest
from src.pipeline import ETLPipeline, ExtractedItemSchema
from src.stealth import stealth_engine


@pytest.fixture
def pipeline_instance():
    """
    Provides an ETLPipeline instance initialized with a temporary test output directory.
    """
    return ETLPipeline(output_dir="tests/test_output")


@pytest.mark.asyncio
async def test_pydantic_schema_validation_success(pipeline_instance):
    """
    Tests Pydantic v2 schema validation with valid payload inputs.
    """
    mock_raw_data = {
        "url": "https://example.com",
        "title": "  Example Domain  ",
        "status_code": 200,
        "html": "<html><body><h1>Example Domain</h1></body></html>",
        "success": True
    }

    validated_item = pipeline_instance.process_raw_payload(mock_raw_data)

    assert validated_item is not None
    assert isinstance(validated_item, ExtractedItemSchema)
    assert validated_item.title == "Example Domain"  # Validates whitespace stripping
    assert validated_item.status_code == 200
    assert validated_item.content_length > 0


@pytest.mark.asyncio
async def test_pydantic_schema_validation_failure(pipeline_instance):
    """
    Tests Pydantic v2 schema failure handling with invalid payloads.
    """
    invalid_raw_data = {
        "url": "not-a-valid-url",
        "title": "",  # Empty title triggers validator error
        "status_code": 999,  # Invalid status code range
        "html": "",
        "success": False
    }

    validated_item = pipeline_instance.process_raw_payload(invalid_raw_data)
    assert validated_item is None  # Pipeline gracefully filters out bad payloads


@pytest.mark.asyncio
async def test_stealth_bypass_live_target():
    """
    Live anti-bot bypass validation test against a standard detection/sec target.
    """
    target_url = "https://nowsecure.nl"
    result = await stealth_engine.fetch_page_content(target_url)

    assert result["success"] is True
    assert result["status_code"] == 200
    assert len(result["html"]) > 0
    assert result["title"] != ""