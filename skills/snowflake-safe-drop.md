---
name: snowflake-safe-drop
description: Drop a Snowflake object with a recovery plan — which objects can be undropped, inside what window, and which deletions are one-way doors.
api: Snowflake REST API v2
base_url: https://<orgname>-<account_name>.snowflakecomputing.com
spec: openapi/snowflake-database-api-openapi.yml, openapi/snowflake-table-api-openapi.yml, openapi/snowflake-account-api-openapi.yml
operations:
  - deleteTable
  - undropTable
  - deleteDatabase
  - undropDatabase
  - cloneDatabase
  - fetchTable
generated: '2026-09-03'
method: generated
---

# Drop something, and be able to get it back

Read this before any automated delete against Snowflake. There is no dry-run on this API,
and the reversal window is much shorter than most people assume.

## The window

Reversal is Time Travel, governed by `DATA_RETENTION_TIME_IN_DAYS` on the object.

- **Default: 1 day (24 hours).** Automatically enabled on every account.
- **Standard Edition: 1 day maximum.** It can be set to 0, or back to 1. That is the range.
- **Enterprise Edition and above: 0 to 90 days** for permanent databases, schemas and tables.
- Transient and temporary objects: 1 day maximum regardless of edition.

Source: <https://docs.snowflake.com/en/user-guide/data-time-travel>

**Never assume 90 days.** An agent that plans a rollback on a 90-day assumption against a
Standard Edition account has one day, and will find out on day two.

Check the actual value before you drop: `fetchDatabase` and `fetchTable` return
`data_retention_time_in_days` and `retention_time` on the object.

## What can be undropped

Each of these has a first-class reversal operation in the contract:

| Object | Drop | Reversal |
|---|---|---|
| Database | `deleteDatabase` | `undropDatabase` — `POST /api/v2/databases/{name}:undrop` |
| Schema | `deleteSchema` | `undropSchema` |
| Table | `deleteTable` | `undropTable` — `POST /api/v2/.../tables/{name}:undrop` |
| Iceberg table | `dropIcebergTable` | `undropIcebergTable` |
| Dynamic table | `deleteDynamicTable` | `undropDynamicTable` |
| External volume | `deleteExternalVolume` | `undropExternalVolume` |
| Tag | `deleteTag` | `undropTag` |
| Streamlit app | `deleteStreamlit` | `undropStreamlit` |
| Account | `deleteAccount` | `UndropAccount` |

The account case is different and better: `deleteAccount` takes a **required**
`gracePeriodInDays` query parameter, and its own description in the spec states "The minimum
is 3 days and the maximum is 90 days." You choose the recovery window at delete time.

## What cannot be undropped

No `:undrop` operation exists for any of these. Deleting one is permanent as far as the API
is concerned:

`deleteWarehouse`, `deleteRole`, `deleteDatabaseRole`, `deleteUser`, `deleteAlert`,
`deleteEventTable`, `deleteSecret`, `deleteSequence`, `deletePipe`, `deleteStream`,
`deleteView`, `deleteNotebook`, `deleteTask`, `deleteStage`, `deleteFunction`,
`deleteProcedure`, `deleteUserDefinedFunction`, `deleteComputePool`, `deleteService`,
`deleteImageRepository`, `deleteNetworkPolicy`, `deleteNetworkRule`, `deletePasswordPolicy`,
`deleteAPIIntegration`, `deleteCatalogIntegration`, `deleteNotificationIntegration`,
`deleteManagedAccount`, `deleteArtifactRepository`, `deleteCortexSearchService`.

Some of these are cheap to recreate (a warehouse is a handful of fields). Some are not — a
`Role` carries a grant graph, and recreating the role does not restore the grants that were
attached to it.

## The safe sequence

1. **Read the retention value.** `fetchTable` / `fetchDatabase`; look at
   `data_retention_time_in_days`. If it is 0, there is no reversal at all.
2. **Clone first if it matters.** `cloneDatabase` — `POST /api/v2/databases/{name}:clone` —
   is a zero-copy metadata clone. It costs almost nothing until the copy diverges, and it
   gives you a recovery path that does not expire with the Time Travel window. This is the
   single most useful habit on this platform.
3. **Delete with `ifExists=true`.** `DELETE /api/v2/.../{name}?ifExists=true` returns 200
   without acting if the object is already gone, which makes the delete idempotent and
   makes retries safe.
4. **Verify.** Fetch the object; expect a 404.
5. **If you were wrong, undrop immediately.** `POST /api/v2/.../{name}:undrop`. The window
   is running from the moment of the drop.

## What UNDROP does not restore

- **Spend.** Compute consumed before the drop is billed regardless. Time Travel storage for
  the dropped object also keeps accruing until the retention window closes — dropping
  something does not immediately stop it costing money.
- **References by name.** Snowflake objects have no surrogate ID; everything points at
  everything else by name. An undropped object comes back under its name, so name-based
  references heal — but anything created in the gap that reused the name will collide.

## Failure handling

| Status | Cause | Do |
|---|---|---|
| 404 on undrop | Window has closed, or the name is wrong | The object is gone. Restore from a clone or a share |
| 409 on undrop | An object now occupies that name | Rename the occupant first |
| 403 | Role lacks OWNERSHIP on the object | Check the grant |
