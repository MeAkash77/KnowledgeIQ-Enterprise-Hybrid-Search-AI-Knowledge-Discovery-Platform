"""
Configuration management for the AI Knowledge Search Platform.
Handles environment variables and application settings.
"""

from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env/config.env
load_dotenv("config.env")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file="config.env",
        case_sensitive=False,
        extra="ignore"
    )

    # ======================================================
    # LLM Configuration
    # ======================================================

    llm_provider: Literal["ollama", "openai"] = Field(
        default="ollama",
        validation_alias="LLM_PROVIDER",
    )

    openai_api_key: str = Field(
        default="",
        validation_alias="OPENAI_API_KEY",
    )

    ollama_model: str = Field(
        default="llama2",
        validation_alias="OLLAMA_MODEL",
    )

    # ======================================================
    # Embedding Configuration
    # ======================================================

    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )

    embedding_dimension: int = Field(
        default=384,
        validation_alias="EMBEDDING_DIMENSION",
    )

    # ======================================================
    # Vector Database
    # ======================================================

    chroma_persist_directory: str = Field(
        default="./data/chroma_index",
        validation_alias="CHROMA_PERSIST_DIRECTORY",
    )

    sqlite_db_path: str = Field(
        default="./data/knowledge_search.db",
        validation_alias="SQLITE_DB_PATH",
    )

    # Optional Qdrant Support
    qdrant_url: str = Field(
        default="",
        validation_alias="QDRANT_URL",
    )

    qdrant_api_key: str = Field(
        default="",
        validation_alias="QDRANT_API_KEY",
    )

    # ======================================================
    # Document Processing
    # ======================================================

    chunk_size: int = Field(
        default=1000,
        validation_alias="CHUNK_SIZE",
    )

    chunk_overlap: int = Field(
        default=200,
        validation_alias="CHUNK_OVERLAP",
    )

    max_chunks_per_query: int = Field(
        default=10,
        validation_alias="MAX_CHUNKS_PER_QUERY",
    )

    # ======================================================
    # Retrieval
    # ======================================================

    bm25_k1: float = Field(
        default=1.2,
        validation_alias="BM25_K1",
    )

    bm25_b: float = Field(
        default=0.75,
        validation_alias="BM25_B",
    )

    hybrid_alpha: float = Field(
        default=0.7,
        validation_alias="HYBRID_ALPHA",
    )

    # ======================================================
    # Context Optimization
    # ======================================================

    similarity_threshold: float = Field(
        default=0.9,
        validation_alias="SIMILARITY_THRESHOLD",
    )

    max_context_tokens: int = Field(
        default=4000,
        validation_alias="MAX_CONTEXT_TOKENS",
    )

    # ======================================================
    # Redis
    # ======================================================

    redis_host: str = Field(
        default="localhost",
        validation_alias="REDIS_HOST",
    )

    redis_port: int = Field(
        default=6379,
        validation_alias="REDIS_PORT",
    )

    redis_db: int = Field(
        default=0,
        validation_alias="REDIS_DB",
    )

    redis_password: str = Field(
        default="",
        validation_alias="REDIS_PASSWORD",
    )

    cache_enabled: bool = Field(
        default=False,
        validation_alias="CACHE_ENABLED",
    )

    cache_ttl: int = Field(
        default=3600,
        validation_alias="CACHE_TTL",
    )

    # ======================================================
    # Server
    # ======================================================

    workers: int = Field(
        default=1,
        validation_alias="WORKERS",
    )

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()

    def _ensure_directories(self):
        """Create directories automatically."""

        directories = [
            Path(self.chroma_persist_directory),
            Path(self.sqlite_db_path).parent,
            Path("./data/raw"),
            Path("./data/processed"),
            Path("./logs"),
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    # ======================================================
    # Helpers
    # ======================================================

    @property
    def is_openai_enabled(self) -> bool:
        return (
            self.llm_provider == "openai"
            and bool(self.openai_api_key)
            and self.openai_api_key != "your_openai_api_key_here"
        )

    @property
    def is_ollama_enabled(self) -> bool:
        return self.llm_provider == "ollama"

    @property
    def is_qdrant_enabled(self) -> bool:
        return bool(self.qdrant_url)


settings = Settings()
