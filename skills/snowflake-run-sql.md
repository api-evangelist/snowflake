---
name: snowflake-run-sql
description: Submit a SQL statement to Snowflake, poll it to completion, page the result set, and cancel it if it runs too long.
api: Snowflake SQL API v2
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-statements-api-openapi.yml
operations:
  - submitStatement
  - getStatementStatus
  - fetchResult
  - cancelStatement
generated: '2026-09-03'
method: generated
---

# Run a SQL statement on Snowflake

The one flow every other Snowflake integration falls back on. If no REST operation
covers what you need, you do it here.

## Before you start

- You need an account host: `https://<orgname>-<account_name>.snowflakecomputing.com`.
  There is no shared API host.
- You need two headers, not one:
  - `Authorization: Bearer <token>`
  - `X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT | OAUTH | PROGRAMMATIC_ACCESS_TOKEN`
  Omitting the second header is the single most common 401 on this API.
- You need a warehouse. A statement without compute attached will not run.

## Step 1 — Submit the statement

`submitStatement` — `POST /api/v2/statements`

Body carries `statement`, plus `warehouse`, `database`, `schema` and `role` to bind the
execution context. Bind variables go in `bindings`; use them rather than string-formatting
SQL.

Two outcomes, and you must handle both:

- **200** — the statement finished fast. The `ResultSet` is already in the body.
- **202** — still running. The body is `SuccessAcceptedResponse` carrying a
  `statementHandle` (and `resultHandler`), and a `Location` header. Go to step 2.

Set `async=true` in the request if you want the 202 path deliberately rather than
waiting on the socket.

## Step 2 — Poll for completion

`getStatementStatus` — `GET /api/v2/statements/{statementHandle}`

Poll until it stops returning 202. Back off with jitter — start around 2 seconds and
double. Do not poll tightly: 429 on this API carries no `Retry-After` and no
`RateLimit-*` headers, so the server will not tell you how long to wait.

## Step 3 — Page the results

The result body is a `ResultSet` with `resultSetMetaData`, `data` (an array of rows as
arrays of strings) and `code`. Large results are paged with the `page` query parameter,
and the `Link` response header carries `rel="first"`, `rel="next"`, `rel="prev"` and
`rel="last"`. **The paging state is only in the header** — there is no `next_cursor` or
`has_more` in the body. A client that reads only the body will silently truncate.

`fetchResult` — `GET /api/v2/results/{result_handler}` retrieves a result by handle when
you have one from an asynchronous execution elsewhere in the API.

## Step 4 — Cancel if you need to

`cancelStatement` — `POST /api/v2/statements/{statementHandle}/cancel`

Works while the statement is executing. This is the only reversal available on a running
query. Compute already consumed is still billed.

## Failure handling

| Status | What it means here | Do |
|---|---|---|
| 400 | Malformed request or SQL compilation error (`code` 390189) | Fix the statement. Do not retry unchanged. |
| 401 | Bad, missing or expired token — or a missing token-type header | Re-authenticate, check the type header |
| 403 | Role lacks the privilege, **or the API is not enabled on the account** | Check both, in that order |
| 408 / 503 / 504 | Server-side timeout | Retry with jittered backoff |
| 429 | Rate limited (`code` 390505) | Back off ~2s, doubling. No header tells you how long |
| 500 | Unrecoverable | Capture `request_id` and open a support case |

Every error body is `{ message, code, error_code, request_id }`. Branch on `code`, not on
`error_code` — that field is deprecated in Snowflake's own schema. Log `request_id`; it
matches the `X-Snowflake-Request-ID` response header and is what support will ask for.

## Cautions

- There is **no dry-run**. A `DROP` submitted here executes.
- Idempotency on this endpoint is your responsibility. A retried `INSERT` inserts twice —
  the SQL API has no replay key.
- Unquoted identifiers fold to uppercase. `"my_table"` and `my_table` are different objects.
