---
name: snowflake-provision-objects
description: Provision a Snowflake database, schema and table idempotently over the REST API, verifying each object landed.
api: Snowflake REST API v2
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-database-api-openapi.yml, openapi/snowflake-schema-api-openapi.yml, openapi/snowflake-table-api-openapi.yml
operations:
  - createDatabase
  - fetchDatabase
  - createSchema
  - fetchSchema
  - createTable
  - fetchTable
  - listDatabases
generated: '2026-09-03'
method: generated
---

# Provision a database, schema and table

Snowflake's REST API mirrors the SQL object hierarchy exactly: the URL path IS the
containment relationship. Provisioning is three nested creates, in order.

## The idempotency rule that makes this safe

Every create takes a `createMode` query parameter:

- `errorIfExists` — **the default**. 409 Conflict if the object is already there.
- `ifNotExists` — succeeds without acting if it already exists. **Use this.**
- `orReplace` — replaces the existing object. Idempotent in outcome, destructive in effect.
  Do not reach for this to "make it work"; it drops what was there.

There is no `Idempotency-Key` header on this API. `createMode=ifNotExists` is the whole
idempotency story for creates, and it is a statement about desired state, not a replay
guard: if your request was received and the response was lost, the retry is re-evaluated,
not replayed.

## Step 1 — Create the database

`createDatabase` — `POST /api/v2/databases?createMode=ifNotExists`

Body is a `Database`: `name` at minimum, plus optional `comment`,
`data_retention_time_in_days`, `max_data_extension_time_in_days`.

`data_retention_time_in_days` is worth setting deliberately here — it is the Time Travel
window that decides whether a later `DROP` is recoverable. The default is **1 day**.
Standard Edition cannot exceed 1; Enterprise Edition and above allow up to 90 for
permanent objects.

## Step 2 — Verify it

`fetchDatabase` — `GET /api/v2/databases/{name}`

Do not skip this. A 200 on create tells you the request was accepted; the fetch tells you
the object exists under the name you will use later. Identifier folding means the name you
sent and the name Snowflake stored are not always the same string.

`listDatabases` — `GET /api/v2/databases` supports `like`, `startsWith`, `showLimit`
(1–10000) and `fromName` as a cursor. Read the `Link` header for paging; the body is a
bare array with no paging envelope.

## Step 3 — Create the schema

`createSchema` — `POST /api/v2/databases/{database}/schemas?createMode=ifNotExists`

Verify with `fetchSchema` — `GET /api/v2/databases/{database}/schemas/{name}`.

## Step 4 — Create the table

`createTable` — `POST /api/v2/databases/{database}/schemas/{schema}/tables?createMode=ifNotExists`

Body is a `Table` with `name` and `columns` (each a `TableColumn` with `name`, `datatype`,
and optionally `nullable`, `default`, `constraints`). Optional `cluster_by`.

Verify with `fetchTable` — `GET /api/v2/databases/{database}/schemas/{schema}/tables/{name}`.

## Identifiers

`openapi/common.yaml#/components/schemas/Identifier` sets the rule:

> pattern: `^"([^"]|"")+"|[a-zA-Z_][a-zA-Z0-9_$]*$`

Unquoted names fold to uppercase. If your name contains a space, a hyphen or any special
character, the **entire** string must be double-quoted, and it is then case-sensitive.
Decide once, at provisioning time, whether you are using quoted identifiers, and be
consistent — mixing the two produces 404s that look like permissions problems.

## Failure handling

| Status | Cause | Do |
|---|---|---|
| 409 | Object exists and you sent `createMode=errorIfExists` | Re-send with `ifNotExists` |
| 403 | Role lacks CREATE privilege, or the API is not enabled | Check the grant, then check the API is on |
| 404 | Parent container does not exist, or the endpoint path is wrong | Create the parent first |
| 400 | Invalid body — usually a bad `datatype` or malformed identifier | Fix and resend |

## Clean-up and reversal

- `deleteDatabase` / `deleteTable` accept `ifExists=true`, which returns 200 without acting
  when the object is already gone. That is the idempotent delete.
- `undropDatabase` and `undropTable` exist and work **within the object's Time Travel
  window** — one day by default. See `skills/snowflake-safe-drop.md` before you drop
  anything you care about.
