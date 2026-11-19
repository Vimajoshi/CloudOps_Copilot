from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://cloudops:cloudops@localhost:5432/cloudops"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    embedding_provider: Literal["openai", "local"] = "openai"
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimensions: int = Field(default=1536, ge=1, le=2000)
    runbooks_dir: str = "runbooks"
    retrieval_top_k: int = Field(default=5, ge=1, le=20)
    # Cosine distance: smaller means more similar. Calibrate for your own model/data.
    retrieval_max_distance: float = Field(default=0.45, ge=0, le=2)
    app_api_key: str = ""
    prompt_cost_per_million: float = Field(default=0, ge=0)
    completion_cost_per_million: float = Field(default=0, ge=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
