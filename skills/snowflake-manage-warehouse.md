---
name: snowflake-manage-warehouse
description: Create, resume, suspend, abort queries on and retire a Snowflake virtual warehouse — the compute lever that decides the bill.
api: Snowflake REST API v2
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-warehouse-api-openapi.yml
operations:
  - createWarehouse
  - fetchWarehouse
  - listWarehouses
  - resumeWarehouse
  - suspendWarehouse
  - abortAllQueriesOnWarehouse
  - deleteWarehouse
generated: '2026-09-03'
method: generated
---

# Manage a virtual warehouse

A warehouse is Snowflake compute. It is also the meter. Every credit an agent spends on
this platform is spent by a running warehouse, so this is the flow to get right before any
automation is allowed near a production account.

## Step 1 — Create

`createWarehouse` — `POST /api/v2/warehouses?createMode=ifNotExists`

Body is a `Warehouse`. The fields that matter for cost control:

- `warehouse_size` — the multiplier on credit burn.
- `auto_suspend` — seconds of idle before Snowflake suspends it automatically. **Set this.**
  A warehouse with no auto-suspend runs, and bills, until something stops it.
- `auto_resume` — whether a query wakes it. Convenient, and it means a stray query can
  start the meter.
- `min_cluster_count` / `max_cluster_count` — multi-cluster scaling (Enterprise Edition and
  above).
- `initially_suspended` — create it stopped. Prefer this when provisioning ahead of use.

## Step 2 — Verify

`fetchWarehouse` — `GET /api/v2/warehouses/{name}` returns `state`, `size`, `auto_suspend`,
`auto_resume` and the cluster counts. Read `state` before assuming anything is running.

`listWarehouses` — `GET /api/v2/warehouses` supports `like`, `startsWith`, `showLimit` and
`fromName`. Page from the `Link` header.

## Step 3 — Resume and suspend

`resumeWarehouse` — `POST /api/v2/warehouses/{name}:resume`
`suspendWarehouse` — `POST /api/v2/warehouses/{name}:suspend`

These are exact inverses and unbounded in time — suspend always undoes resume, whenever you
call it. That makes them the safest pair in the whole API, and the pattern to reach for
when you want a reversible action.

Both accept `ifExists=true` so a call against an already-suspended or missing warehouse
returns 200 rather than erroring.

## Step 4 — Stop runaway work

`abortAllQueriesOnWarehouse` — `POST /api/v2/warehouses/{name}:abort`

Kills every query currently running on the warehouse. This is the emergency brake for an
agent that has submitted something expensive. Pair it with `suspendWarehouse` — aborting
queries does not stop the warehouse, and a warehouse with `auto_resume` on will simply pick
up the next query.

The order that actually stops spend:

1. `abortAllQueriesOnWarehouse`
2. `suspendWarehouse`

## Step 5 — Retire

`deleteWarehouse` — `DELETE /api/v2/warehouses/{name}?ifExists=true`

**There is no `undropWarehouse`.** Warehouses are not covered by Time Travel and there is
no `:undrop` operation for them in the contract. Deleting one is permanent from the API's
point of view. Recreate is cheap — the configuration is a handful of fields — but any
resource monitor, grant or default-warehouse reference pointing at it breaks, because
Snowflake objects are referenced by name, not by a stable ID.

## Deprecated

`useWarehouse` is marked `deprecated: true` in the spec. Bind the warehouse in the request
context of the SQL API call (`warehouse` in the `submitStatement` body) instead of setting
a session default through this operation.

## Failure handling

| Status | Cause | Do |
|---|---|---|
| 409 | Warehouse exists, `createMode=errorIfExists` | Re-send with `ifNotExists` |
| 403 | Role lacks OPERATE/MODIFY on the warehouse | Check the grant |
| 404 | Wrong name, or identifier case-folding | Fetch by list, compare the exact stored name |
| 429 | Rate limited | Jittered backoff from ~2s. No `Retry-After` is sent |

## Cost note

Suspending returns compute to Snowflake but does not release storage, and Time Travel
retention on dropped objects keeps accruing storage charges until the window closes.
Stopping the warehouse stops the largest line, not the whole bill.
