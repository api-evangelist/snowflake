---
name: snowflake-search-unstructured
description: Retrieve passages from a Snowflake Cortex Search service over unstructured content, for grounding an answer in governed enterprise data.
api: Snowflake Cortex Search Service API
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-cortex-search-service-api-openapi.yml
operations:
  - listCortexSearchServices
  - fetchCortexSearchService
  - queryCortexSearchService
  - suggestCortexSearchService
  - sendFeedback
  - suspendCortexSearchService
  - resumeCortexSearchService
generated: '2026-09-03'
method: generated
---

# Retrieve from a Cortex Search service

Cortex Search is Snowflake's managed retrieval service over unstructured content that
already lives in a Snowflake table. It handles chunking, embedding and hybrid
(vector + keyword) ranking, and it keeps the index fresh against a target lag. For an agent
building RAG on enterprise data, this is the retrieval half — and the reason to use it over
an external vector store is that results stay inside Snowflake's RBAC boundary.

This operation backs the `CORTEX_SEARCH_SERVICE_QUERY` tool on the managed MCP server.

## Step 1 — Find the service

`listCortexSearchServices` —
`GET /api/v2/databases/{database}/schemas/{schema}/cortex-search-services`

Supports `like`, `startsWith`, `showLimit` and `fromName`; page from the `Link` header.

`fetchCortexSearchService` — `GET /api/v2/.../cortex-search-services/{name}` returns the
service definition. The fields you need before querying:

- `search_column` — the column that was indexed. This is what your query matches against.
- `attribute_columns` — the columns you are allowed to filter on. Filtering on anything
  else will not work.
- `columns` — the columns returned with each hit.
- `target_lag` and `warehouse` — how fresh the index is and what compute refreshes it.

Read `attribute_columns` before writing a filter. Guessing a filter column is the most
common cause of an empty result set that looks like "the data isn't there".

## Step 2 — Query

`queryCortexSearchService` —
`POST /api/v2/databases/{database}/schemas/{schema}/cortex-search-services/{service_name}:query`

Body:

- `query` — the search text.
- `columns` — which columns to return per hit. Ask for what you need; every extra column is
  payload you will put in a context window.
- `filter` — a predicate over `attribute_columns` (`@eq`, `@contains`, `@gte`, `@and`,
  `@or`, `@not`). This is where multi-tenant and permission scoping goes.
- `limit` — number of results. Set it deliberately; the default will not match your context
  budget.
- `scoring_config` / ranking weights — the spec exposes `RankingWeights`, `TextBoost`,
  `VectorBoost`, `NumericBoost`, `TimeDecay` and `QuerySimilarityBoost` for tuning hybrid
  retrieval. `TimeDecay` is the one to reach for when recency matters.

The response carries the ranked hits with the columns you asked for.

## Step 3 — Refine

`suggestCortexSearchService` — `POST /api/v2/.../{service_name}:suggest` returns query
suggestions, for autocomplete or query rewriting.

`sendFeedback` — `POST /api/v2/.../{name}:feedback` records result quality. Send it; it is
how the service improves.

## Operating the service

`createCortexSearchService` — `POST /api/v2/.../cortex-search-services?createMode=ifNotExists`
defines the service over a source query, naming the search column, attribute columns,
target lag and refresh warehouse.

`suspendCortexSearchService` / `resumeCortexSearchService` are exact inverses. Suspend stops
the refresh warehouse and stops the meter; the index stays. Use them the way you would use
warehouse suspend.

`deleteCortexSearchService` — `DELETE /api/v2/.../{name}` — **has no undrop**. There is no
`:undrop` for search services and Time Travel does not cover them. Dropping one means
rebuilding and re-indexing from source. Suspend instead of delete unless you are certain.

## Cost

Query calls consume credits, and the refresh warehouse consumes credits on the `target_lag`
schedule whether or not anyone is querying. A search service left running against a tight
target lag is a standing cost. Consumption is not reversible.

## Failure handling

| Status | Cause | Do |
|---|---|---|
| 400 | Filter references a column not in `attribute_columns` | Fetch the service, read `attribute_columns` |
| 403 | Role cannot read the service or its source table | Fix the grants |
| 404 | Wrong database/schema/service name, or identifier case-folding | List the services and compare exact names |
| 429 | Rate limited | Jittered backoff from ~2s. No `Retry-After` |
