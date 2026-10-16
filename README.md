# FSRA RAG Assistant

A production-style retrieval-augmented generation (RAG) system that answers questions about
guidance from the [Financial Services Regulatory Authority of Ontario (FSRA)](https://www.fsrao.ca/guidance-financial-planners-and-financial-advisors)
for financial planners and advisors, with citations to the exact guidance document.

> Not legal or compliance advice. Always confirm against the official FSRA source.

## Architecture

- **Offline ingestion:** crawl FSRA guidance → parse HTML/PDF → structure-aware chunks with
  metadata (guidance number, status, date) → Redis queue → embedding workers → Postgres.
- **Online serving:** FastAPI → cache → query rewrite → hybrid search (pgvector + Postgres
  full-text) → reciprocal rank fusion → cross-encoder rerank → grounded prompt → LLM gateway
  with fallback → citation check → streamed answer.
- **Operations:** evaluation suite in CI, tracing, monitoring, incremental re-indexing.

## Roadmap

- [x] Phase 0 — Repo skeleton, Docker Compose, database schema, CI
- [ ] Phase 1 — Ingestion pipeline (crawl, parse, chunk, queue + embedding workers)
- [ ] Phase 2 — Hybrid retrieval + reranking
- [ ] Phase 3 — Generation with citations + LLM fallback
- [ ] Phase 4 — Evaluation suite (golden set, retrieval + faithfulness metrics) in CI
- [ ] Phase 5 — Caching, guardrails, tracing, monitoring
- [ ] Phase 6 — UI, cloud deploy, results write-up

## Run locally

```bash
cp .env.example .env        # add your API keys
make up                     # starts Postgres+pgvector, Redis, and the API
curl localhost:8000/health  # {"status":"ok", ...}
```

## Tests

```bash
pip install -e ".[dev]"
make lint test
```

## Data

FSRA documents are downloaded by the ingestion script at run time and are not stored in this
repository. All content belongs to FSRA.
