"""
Configuration module for the Healthcare Form Data Extraction PoC.
Loads environment variables from .env file using Pydantic's Settings.
"""
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    
    # File Paths
    upload_dir: Path = Field(Path("./uploads"), env="UPLOAD_DIR")
    screenshot_dir: Path = Field(Path("./screenshots"), env="SCREENSHOT_DIR")
    
    # Form URLs
    target_form_url: str = Field("https://example.com/healthcare-form", env="TARGET_FORM_URL")
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8001, env="PORT")
    debug: bool = Field(True, env="DEBUG")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    def initialize_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)


# Create a global settings instance
settings = Settings()
# Initialize directories
settings.initialize_directories()
