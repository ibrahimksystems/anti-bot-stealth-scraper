import csv
import json
import logging
from pathlib import Path
<<<<<<< HEAD
from typing import Any
=======
from typing import Any, Dict, List, Optional
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97

from pydantic import BaseModel, Field, HttpUrl, field_validator

from src.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(settings.APP_NAME)


class ExtractedItemSchema(BaseModel):
    """Validated representation of one extracted page record."""

    raw_url: HttpUrl
    title: str = Field(..., min_length=1)
    status_code: int = Field(..., ge=200, le=599)
    content_length: int = Field(default=0, ge=0)
    success: bool = True
<<<<<<< HEAD
    extracted_at: str | None = None
=======
    extracted_at: Optional[str] = None
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97

    @field_validator("title")
    @classmethod
    def clean_title_whitespace(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title collapsed to an empty string.")
        return cleaned


class ETLPipeline:
    """Transform, validate, and export extracted records."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

<<<<<<< HEAD
    def process_raw_payload(self, raw_data: dict[str, Any]) -> ExtractedItemSchema | None:
=======
    def process_raw_payload(
        self, raw_data: Dict[str, Any]
    ) -> Optional[ExtractedItemSchema]:
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
        try:
            html_content = raw_data.get("html", "")
            payload = {
                "raw_url": raw_data.get("url"),
                "title": raw_data.get("title", ""),
                "status_code": raw_data.get("status_code", 0),
                "content_length": len(html_content) if html_content else 0,
                "success": raw_data.get("success", False),
            }
            validated_item = ExtractedItemSchema(**payload)
            logger.info("Pipeline validation passed: %s", validated_item.raw_url)
            return validated_item
        except Exception as exc:
            logger.error(
                "Pipeline validation failed for payload (%s): %s",
                raw_data.get("url"),
                exc,
            )
            return None

    async def export_to_json(
        self,
<<<<<<< HEAD
        items: list[ExtractedItemSchema],
=======
        items: List[ExtractedItemSchema],
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
        filename: str = "extracted_data.json",
    ) -> Path:
        file_path = self.output_dir / filename
        data = [item.model_dump(mode="json") for item in items]
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4, ensure_ascii=False)
        logger.info("Exported %s records to JSON: %s", len(items), file_path)
        return file_path

    async def export_to_csv(
        self,
<<<<<<< HEAD
        items: list[ExtractedItemSchema],
=======
        items: List[ExtractedItemSchema],
>>>>>>> ed9713b75295699be7d51fa65d7a3eb581dece97
        filename: str = "extracted_data.csv",
    ) -> Path:
        file_path = self.output_dir / filename
        if not items:
            file_path.write_text("", encoding="utf-8")
            return file_path

        fieldnames = list(items[0].model_dump(mode="json").keys())
        with file_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.model_dump(mode="json"))
        logger.info("Exported %s records to CSV: %s", len(items), file_path)
        return file_path


pipeline = ETLPipeline()
