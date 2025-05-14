import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "xavigate"),
    "user": os.getenv("POSTGRES_USER", "xavigate_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "changeme"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


def get_connection():
    """Get a new Postgres connection, retrying if necessary."""
    import time
    # Retry connection in case Postgres is not ready yet
    retries = int(os.getenv("DB_CONNECT_MAX_RETRIES", "10"))
    delay = float(os.getenv("DB_CONNECT_RETRY_INTERVAL", "2"))
    last_error = None
    # If a DATABASE_URL is provided, use it directly
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"❌ Postgres connection attempt {attempt}/{retries} failed: {e}", flush=True)
            if attempt < retries:
                time.sleep(delay)
    # All retries exhausted
    print(f"⚠️ Could not connect to Postgres after {retries} attempts", flush=True)
    raise last_error


def insert_chunks(chunks, source="AD Framework"):
    with get_connection() as conn:
        with conn.cursor() as cur:
            for chunk in chunks:
                cur.execute(
                    """
                    INSERT INTO documents (source, chunk_index, content, tokens, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        source,
                        chunk["chunk_index"],
                        chunk["content"],
                        chunk["tokens"],
                        Json({"version": "v1", "origin": "AD"}),
                    ),
                )
        conn.commit()
    print(f"✅ Inserted {len(chunks)} chunks into Postgres")