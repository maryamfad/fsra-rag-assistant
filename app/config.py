"""All settings come from environment variables (or a .env file).

Nothing secret is ever hard-coded; API keys live in .env, which git ignores.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://rag:rag@localhost:5433/rag"
    redis_url: str = "redis://localhost:6379/0"

    # Models (used from Phase 1 on). Swap them here, not in the code.
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    reranker_model: str = "BAAI/bge-reranker-base"
    llm_primary: str = "openai/gpt-4o-mini"
    llm_fallback: str = "anthropic/claude-haiku-4-5"

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
