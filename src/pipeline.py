import json
import csv
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field, HttpUrl, field_validator
from src.config import settings

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(settings.APP_NAME)


class ExtractedItemSchema(BaseModel):
    """
    Strict Pydantic v2 schema for validating extracted B2B raw payloads.
    """
    raw_url: HttpUrl
    title: str = Field(..., min_length=1, description="Page or item title cannot be empty.")
    status_code: int = Field(..., ge=200, le=599, description="Valid HTTP status code.")
    content_length: int = Field(default=0, ge=0)
    success: bool = True
    extracted_at: Optional[str] = None

    @field_validator("title")
    @classmethod
    def clean_title_whitespace(cls, value: str) -> str:
        """
        Strips leading/trailing whitespace and normalizes title strings.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title collapsed to empty string after stripping whitespace.")
        return cleaned


class ETLPipeline:
    """
    Asynchronous ETL Pipeline that transforms, validates, and dumps processed scraping data.
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_raw_payload(self, raw_data: Dict[str, Any]) -> Optional[ExtractedItemSchema]:
        """
        Transforms raw HTTP response payloads into validated Pydantic models.
        Separates bad or malformed records.
        """
        try:
            html_content = raw_data.get("html", "")
            payload = {
                "raw_url": raw_data.get("url"),
                "title": raw_data.get("title", ""),
                "status_code": raw_data.get("status_code", 0),
                "content_length": len(html_content) if html_content else 0,
                "success": raw_data.get("success", False)
            }
            
            validated_item = ExtractedItemSchema(**payload)
            logger.info(f"Pipeline Validation Passed: {validated_item.raw_url}")
            return validated_item

        except Exception as e:
            logger.error(f"Pipeline Validation Failed for payload ({raw_data.get('url')}): {str(e)}")
            return None

    async def export_to_json(self, items: List[ExtractedItemSchema], filename: str = "extracted_data.json") -> Path:
        """
        Exports validated records into a structured JSON file.
        """
        file_path = self.output_dir / filename
        data_to_dump = [item.model_dump(mode="json") for item in items]
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_dump, f, indent=4, ensure_ascii=False)
            
        logger.info(f"Successfully exported {len(items)} records to JSON: {file_path}")
        return file_path

    async def export_to_csv(self, items: List[ExtractedItemSchema], filename: str = "extracted_data.csv") -> Path:
        """
        Exports validated records into a CSV format.
        """
        file_path = self.output_dir / filename
        if not items:
            logger.warning("No items to export to CSV.")
            return file_path

        fieldnames = list(items[0].model_dump(mode="json").keys())
        
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.model_dump(mode="json"))

        logger.info(f"Successfully exported {len(items)} records to CSV: {file_path}")
        return file_path


# Global instance
pipeline = ETLPipeline()