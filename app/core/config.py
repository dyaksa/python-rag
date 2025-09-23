from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    """Application settings loaded from environment variables or a .env file."""
    APP_NAME: str
    APP_VERSION: str
    APP_PORT: int

    DEBUG: bool

    GOOGLE_API_KEY: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    MAX_CHUNK_TOKENS: int
    OVERLAP_TOKENS: int
    TOP_K: int

    LANGSMITH_API_KEY: str
    LANGSMITH_TRACING: bool = False

    GOOGLE_LLM_MODEL: str
    GOOGLE_EMBEDDING_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance so environment variables only parsed once."""
    return Settings()


settings = get_settings()