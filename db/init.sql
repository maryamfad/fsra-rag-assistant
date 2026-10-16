-- Runs once, the first time the Postgres container starts.
CREATE EXTENSION IF NOT EXISTS vector;

-- One row per source document (an FSRA guidance page or PDF).
CREATE TABLE IF NOT EXISTS documents (
    id              BIGSERIAL PRIMARY KEY,
    source_url      TEXT UNIQUE NOT NULL,
    guidance_number TEXT,              -- e.g. FP0002APP
    title           TEXT NOT NULL,
    sector          TEXT,              -- e.g. "Financial planners and advisors"
    status          TEXT,              -- Active / Inactive
    effective_date  DATE,
    content_hash    TEXT NOT NULL,     -- fingerprint: skip re-processing if unchanged
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ        -- tombstone: set when FSRA removes the page
);

-- One row per chunk of a document.
CREATE TABLE IF NOT EXISTS chunks (
    id              BIGSERIAL PRIMARY KEY,
    document_id     BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index     INT NOT NULL,
    section_path    TEXT,              -- e.g. "Approach > Supervision of CBs"
    text            TEXT NOT NULL,
    token_count     INT NOT NULL,
    embedding       vector(384),       -- bge-small-en-v1.5 produces 384 numbers
    embedding_model TEXT,              -- which model made the embedding
    tsv             tsvector GENERATED ALWAYS AS (to_tsvector('english', text)) STORED,
    UNIQUE (document_id, chunk_index)
);

-- Meaning search: approximate nearest-neighbour index over embeddings.
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- Keyword search: full-text index (Postgres's BM25-style ranking).
CREATE INDEX IF NOT EXISTS chunks_tsv_gin ON chunks USING gin (tsv);

CREATE INDEX IF NOT EXISTS documents_live ON documents (id) WHERE deleted_at IS NULL;
