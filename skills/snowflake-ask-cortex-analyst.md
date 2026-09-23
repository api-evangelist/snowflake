---
name: snowflake-ask-cortex-analyst
description: Ask a natural-language question of a Snowflake semantic model and get back generated SQL plus results, then execute or verify that SQL.
api: Snowflake Cortex Analyst API
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-cortex-analyst-api-openapi.yml, openapi/snowflake-statements-api-openapi.yml
operations:
  - sendMessage
  - getScopedToken
  - generateVerifiedQuerySuggestions
  - submitStatement
  - getStatementStatus
generated: '2026-09-03'
method: generated
---

# Ask Cortex Analyst a question

Cortex Analyst turns a natural-language question into SQL against a **semantic model** —
a YAML file, staged in Snowflake, that names the tables, dimensions and metrics the model
is allowed to reason about. The semantic model is the guard rail. Without one, there is
nothing to ask.

This is also the operation behind the `CORTEX_ANALYST_MESSAGE` tool on Snowflake's managed
MCP server, so an agent reaching Snowflake through MCP is calling this same endpoint.

## Step 1 — Ask

`sendMessage` — `POST /api/v2/cortex/analyst/message`

The request carries the conversation as `messages` (a list of `MessageObject`, each with
`role` and `content`) plus a pointer to the semantic model — either
`semantic_model_file` (a stage path) or a semantic view. Multi-turn works: send prior
turns back in `messages` and Analyst resolves follow-ups against them.

The response carries `MessageContent` parts. The parts that matter:

- a **text** part — the natural-language answer
- a **sql** part — the generated SQL statement
- a **suggestions** part — alternative questions, when Analyst was not confident

**Analyst generates SQL. It does not necessarily execute it.** Treat the SQL part as a
proposal.

## Step 2 — Decide whether to run it

This is the step agents skip, and it is the important one. Before executing generated SQL:

- Read it. It is plain text in the response.
- Check it is a `SELECT`. A semantic model should not produce DDL or DML, but you are
  about to run text a model wrote against a database.
- Bind it to a role with read-only grants. Snowflake authorization is RBAC on objects,
  not API scopes — the only thing standing between generated SQL and a destructive
  statement is the privileges of the role in the session.

## Step 3 — Execute

`submitStatement` — `POST /api/v2/statements` with the generated SQL, bound to the
warehouse, database, schema and role you have chosen. Poll with `getStatementStatus`, page
the result set from the `Link` header. See `skills/snowflake-run-sql.md` for the full
lifecycle.

## Supporting operations

- `getScopedToken` — `GET /api/v2/cortex/analyst/token` issues a scoped token, for
  embedding Analyst in a front end without handing it full account credentials.
- `generateVerifiedQuerySuggestions` — `POST /api/v2/cortex/analyst/verified-query-suggestions`
  proposes verified queries to add to the semantic model. Verified queries are how you
  improve accuracy over time: they pin a known-good SQL answer to a known question.
- `sendFeedback` — `POST /api/v2/cortex/analyst/feedback` records whether a response was
  good. This feeds model improvement; send it.
- `listAgenticOptimizations` / `getAgenticOptimization` — inspect optimizations applied to
  agentic use of the model.

## Cost

Every `sendMessage` consumes credits, and so does every statement you then execute. **There
is no reversal for consumption** — no void, no refund, no test mode. An agent in a retry
loop on this endpoint spends real money on every attempt. Cap the loop.

## Failure handling

| Status | Cause | Do |
|---|---|---|
| 400 | Bad request, or the semantic model file could not be read | Check the stage path and the model YAML |
| 401 | Token missing, expired, or `X-Snowflake-Authorization-Token-Type` not set | Re-authenticate |
| 403 | Role cannot read the semantic model stage or the underlying tables | Fix the grants — Analyst inherits them |
| 429 | Rate limited | Jittered backoff from ~2s. No `Retry-After` is returned |

Error bodies are `{ message, code, error_code, request_id }` — not RFC 9457 problem+json.
