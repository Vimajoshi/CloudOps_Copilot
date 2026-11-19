"""PostgreSQL persistence and cosine-distance search."""
import time

import psycopg
from psycopg.rows import dict_row

from app.config import get_settings
from app.metrics import retrieval_seconds


def connect():
    return psycopg.connect(get_settings().database_url, connect_timeout=5)


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(str(float(v)) for v in values) + "]"


def init_db(conn) -> None:
    dimensions = get_settings().embedding_dimensions
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.execute(f"""CREATE TABLE IF NOT EXISTS runbook_chunks (
        chunk_id text PRIMARY KEY, filename text NOT NULL, section_title text NOT NULL,
        content text NOT NULL, embedding vector({dimensions}) NOT NULL
    )""")
    actual = conn.execute("""SELECT format_type(a.atttypid, a.atttypmod)
        FROM pg_attribute a WHERE a.attrelid = 'runbook_chunks'::regclass
        AND a.attname = 'embedding'""").fetchone()[0]
    if actual != f"vector({dimensions})":
        raise RuntimeError("Database embedding dimensions differ; recreate the index before changing models")
    conn.execute("""CREATE INDEX IF NOT EXISTS runbook_embedding_hnsw
        ON runbook_chunks USING hnsw (embedding vector_cosine_ops)""")


def replace_chunks(chunks, vectors) -> None:
    if not chunks:
        raise ValueError("No runbook chunks found; existing index was left intact")
    with connect() as conn:
        init_db(conn)
        conn.execute("SELECT pg_advisory_xact_lock(287166241)")
        conn.execute("DELETE FROM runbook_chunks")
        with conn.cursor() as cur:
            cur.executemany("""INSERT INTO runbook_chunks
                (chunk_id, filename, section_title, content, embedding)
                VALUES (%s, %s, %s, %s, %s::vector)""", [
                (c.chunk_id, c.filename, c.section_title, c.content, vector_literal(v))
                for c, v in zip(chunks, vectors, strict=True)
            ])


def search(vector: list[float]) -> list[dict]:
    settings = get_settings()
    started = time.perf_counter()
    try:
        with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
            literal = vector_literal(vector)
            cur.execute("""SELECT chunk_id, filename, section_title, content,
                embedding <=> %s::vector AS distance FROM runbook_chunks
                ORDER BY embedding <=> %s::vector LIMIT %s""",
                (literal, literal, settings.retrieval_top_k))
            return [row for row in cur.fetchall() if row["distance"] <= settings.retrieval_max_distance]
    finally:
        retrieval_seconds.observe(time.perf_counter() - started)
