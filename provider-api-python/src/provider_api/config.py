from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Server configuration
    host: str = Field(default="0.0.0.0", description="Host to bind the server")
    port: str = Field(default="8081", description="Port to run the server on")
    log_level: str = Field(default="info", description="Logging level")

    # Environment
    env: str = Field(
        default="development", description="Environment (development/production)"
    )

    # Future provider behavior settings (for Day 3)
    provider_mode: str = Field(
        default="stable", description="Provider mode: stable, flaky, broken"
    )
    failure_rate: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Failure rate (0.0-1.0)"
    )
    delay_ms: int = Field(
        default=0, ge=0, description="Artificial delay in milliseconds"
    )

    # API configuration
    api_title: str = Field(default="Provider API Service", description="API title")
    api_version: str = Field(default="1.0.0", description="API version")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
