from pydantic import BaseModel, HttpUrl

class ScraperConfig(BaseModel):
    target_url: HttpUrl
    timeout_ms: int = 30000
    use_camoufox: bool = True
    max_retries: int = 3
    headless: bool = True
