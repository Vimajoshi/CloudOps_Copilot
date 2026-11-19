"""Embedding and LLM adapters. The local embedding model is loaded only when used."""
from functools import lru_cache

from openai import OpenAI

from app.config import get_settings


@lru_cache
def local_model(name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(name)


def client() -> OpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI services")
    return OpenAI(api_key=settings.openai_api_key, timeout=60, max_retries=2)


def embed(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    settings = get_settings()
    if settings.embedding_provider == "local":
        vectors = local_model(settings.local_embedding_model).encode(texts).tolist()
    else:
        vectors = []
        for start in range(0, len(texts), 100):
            response = client().embeddings.create(
                model=settings.openai_embedding_model,
                input=texts[start : start + 100],
                dimensions=settings.embedding_dimensions,
            )
            vectors.extend(item.embedding for item in sorted(response.data, key=lambda x: x.index))
    if len(vectors) != len(texts) or any(len(v) != settings.embedding_dimensions for v in vectors):
        raise ValueError("Embedding dimensions do not match EMBEDDING_DIMENSIONS")
    return vectors
