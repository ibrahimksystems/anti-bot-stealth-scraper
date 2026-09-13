from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ScraperSettings(BaseSettings):
    """
    Scraper configuration and environment variable management.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Uygulama Ayarları
    APP_NAME: str = "AntiBotStealthScraper"
    DEBUG: bool = False

    # Stealth Tarayıcı Ayarları
    HEADLESS: bool = True
    HUMANIZE: bool = True  # İnsan benzeri imleç ve klavye hareketleri
    TARGET_OS: str = "windows"  # windows, macos, linux
    LOCALE: str = "en-US"

    # Ağ ve Proxy Ayarları
    PROXY_SERVER: Optional[str] = Field(default=None, description="e.g.: http://user:pass@proxy.example.com:8080")
    TIMEOUT_SECONDS: int = 30000  # 30 Saniye (Milisaniye cinsinden)

    # Retry ve Rate Limit Ayarları
    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: float = 2.0  # Hata aldığında bekleme süresini katlama katsayısı


settings = ScraperSettings()