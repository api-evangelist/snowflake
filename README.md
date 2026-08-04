# Snowflake (snowflake)

<!-- API-EVANGELIST-PROVENANCE:BEGIN -->
> ### About this repository
>
> **This is not our API.** This repository is an independent, third-party profile of a company's
> **publicly available** API surface, maintained by [API Evangelist](https://apievangelist.com).
> API Evangelist does not operate, host, resell, or support this company's APIs, and is not
> affiliated with or endorsed by the company unless stated on the profile.
>
> **Where the information came from.** Everything here is assembled from material a member of the
> public can reach with a browser and no credentials — the company's own website, developer portal
> and documentation, the specifications it publishes for public use (OpenAPI, AsyncAPI, JSON Schema,
> `apis.json`, `llms.txt` and similar), its public repositories, and its public status, pricing and
> changelog pages. **Nothing here is obtained by breaching a system, defeating an access control, or
> using credentials of any kind.**
>
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are
> independently calculated scores of a company's *public* API artifacts, produced by API Evangelist
> against a published rubric. They are not certifications, endorsements, security assessments, or
> audits, and they score published artifacts — not the quality, safety, or security of the software.
>
> **Corrections, re-scores, and removal are free.** No partnership, contract, or purchase is
> required, and you do not need to justify the request.
>
> - **Something wrong?** Open an issue on this repository, or email
>   [info@apievangelist.com](mailto:info@apievangelist.com).
> - **Published something new?** Ask for a re-score and we will re-run the rating.
> - **Want the listing taken down?** Say so and we will honor it. The profile is reduced to your
>   company name, a factual description, and a link to your own site, and the company is recorded as
>   **unrated** — never scored zero for having asked.
>
> **Response times.** Acknowledgement within **one business day**; removal or restriction within
> **two business days**; corrections and re-scores within **five business days**.
>
> **On a security or compliance team?** Email
> [info@apievangelist.com](mailto:info@apievangelist.com) with *security* in the subject line and
> you will get a person, not a form. We will tell you exactly which public URLs this profile was
> built from so your team can see the same surface we did, and we will take the listing down on
> request while you work through it.
>
> Full detail: **[Where this data comes from](https://apievangelist.com/about/where-our-data-comes-from)**
<!-- API-EVANGELIST-PROVENANCE:END -->

Snowflake is a cloud-based data platform that provides data warehousing, data lakes, data engineering, data science, and data application development capabilities.

**URL:** [Visit APIs.json URL](https://raw.githubusercontent.com/api-evangelist/snowflake/refs/heads/main/apis.yml)

**Run:** [Capabilities Using Naftiko](https://github.com/naftiko/fleet?utm_source=api-evangelist&utm_medium=readme&utm_campaign=company-api-evangelist&utm_content=repo)

## Tags:

 - Data Lakes, Data Sharing, Data Warehousing, Database, SQL

## Timestamps

- **Created:** 2025-06-05
- **Modified:** 2026-04-18

## APIs

### Snowflake Account API
The Snowflake Account API is a REST API that you can use to access, update, and perform certain actions on Account resource in Snowflake.

#### Properties

- [OpenAPI](openapi/account.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/account)

### Snowflake Database API
The Snowflake Database API is a REST API that you can use to access, update, and perform certain actions on Database resource in Snowflake.

#### Properties

- [OpenAPI](openapi/database.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/database)

### Cortex Analyst API
The Snowflake Cortex Analyst API is a REST API that allows end user to chat with their data leveraging semantic models to generate SQL queries.

#### Properties

- [OpenAPI](openapi/cortex-analyst.yaml)
- [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api)

### Cortex Inference API
OpenAPI 3.0 specification for the Cortex REST API.

#### Properties

- [OpenAPI](openapi/cortex-inference.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/cortex-inference)

### Snowflake SQL API
The Snowflake SQL API is a REST API that you can use to access and update data in a Snowflake database.

#### Properties

- [OpenAPI](openapi/sqlapi.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/sql-api/index)

### Snowflake Table API
The Snowflake Table API is a REST API that you can use to access, update, and perform certain actions on Tables resource in a Snowflake database.

#### Properties

- [OpenAPI](openapi/table.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/table)

### Snowflake Warehouse API
The Snowflake Warehouse API is a REST API that you can use to access, customize and manage virtual warehouse in a Snowflake account.

#### Properties

- [OpenAPI](openapi/warehouse.yaml)
- [Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/warehouse)

## Common Properties

- [StatusPage](https://status.snowflake.com/)
- [ChangeLog](https://docs.snowflake.com/en/release-notes/overview)
- [GettingStarted](https://docs.snowflake.com/en/user-guide-getting-started)
- [Tutorials](https://docs.snowflake.com/en/tutorials)
- [TermsOfService](https://www.snowflake.com/en/legal/snowflake-site-terms/)
- [Documentation](https://docs.snowflake.com/)
- [PrivacyPolicy](https://www.snowflake.com/en/legal/privacy/privacy-policy/)
- [Blog](https://www.snowflake.com/en/engineering-blog/)
- [Support](https://www.snowflake.com/en/support/)
- [Plans](https://www.snowflake.com/en/pricing-options/)
- [Portal](https://www.snowflake.com/en/developers/)
- [SignUp](https://signup.snowflake.com/)
- [GitHubOrganization](https://github.com/snowflakedb)
- [Quickstart](https://quickstarts.snowflake.com/)
- [Authentication](https://docs.snowflake.com/en/user-guide/admin-security.html)
- [OpenAPI](https://github.com/snowflakedb/snowflake-rest-api-specs)

## Features

| Name | Description |
|------|-------------|
| Data Warehousing | Fully managed cloud data warehouse with automatic scaling, concurrency handling, and near-zero maintenance. |
| Data Lakes | Store and query semi-structured and unstructured data alongside structured data using Iceberg tables and external volumes. |
| Cortex AI | Built-in AI and ML capabilities including LLM inference, text embeddings, semantic search, and natural language analytics. |
| Snowpark | Developer framework for building data pipelines, ML models, and applications in Python, Java, and Scala directly on Snowflake. |
| Dynamic Tables | Declarative data pipelines that automatically maintain materialized views with configurable lag targets. |
| Snowpipe Streaming | Continuous data ingestion with low-latency loading from external sources into Snowflake tables. |
| Snowflake Notebooks | Interactive development environment for data exploration, analysis, and ML model development. |
| Snowpark Container Services | Run containerized workloads and services directly within Snowflake using OCI-compatible containers. |
| Data Sharing | Securely share live data across accounts and organizations without data movement or copies. |
| Streamlit Apps | Build and deploy interactive data applications directly within Snowflake using Streamlit. |

## Use Cases

| Name | Description |
|------|-------------|
| Data Engineering | Build and orchestrate data pipelines using tasks, streams, pipes, and dynamic tables for ETL/ELT workflows. |
| Data Science and ML | Develop and deploy machine learning models using Snowpark, notebooks, and Cortex AI capabilities. |
| Data Analytics | Run complex analytical queries across massive datasets with automatic scaling and concurrency. |
| AI-Powered Analytics | Use Cortex Analyst to ask questions about data in natural language and receive SQL-backed answers. |
| Data Application Development | Build data-intensive applications using Snowflake APIs, Snowpark, and Streamlit. |
| Data Governance | Manage access control, data classification, and compliance using roles, grants, tags, and network policies. |

## Integrations

| Name | Description |
|------|-------------|
| Apache Spark | Execute Spark workloads on Snowflake infrastructure through the Spark Connect API. |
| Apache Iceberg | Create and manage Iceberg tables with support for AWS Glue, Delta, and REST catalog integrations. |
| Cloud Storage | Connect to external cloud storage on AWS S3, Azure Blob, and Google Cloud Storage via external volumes and stages. |
| Notification Services | Integrate with AWS SNS, Azure Event Grid, and GCP Pub/Sub for event-driven data pipelines. |
| Git Repositories | Connect to Git repositories for version-controlled code and configuration management. |

## Artifacts

Machine-readable API specifications organized by format.

### OpenAPI

- [Snowflake Account API](openapi/account.yaml)
- [Snowflake Alert API](openapi/alert.yaml)
- [Snowflake API Integration API](openapi/api-integration.yaml)
- [Snowflake Catalog Integration API](openapi/catalog-integration.yaml)
- [Snowflake Compute Pool API](openapi/compute-pool.yaml)
- [Cortex Analyst API](openapi/cortex-analyst.yaml)
- [Cortex Inference API](openapi/cortex-inference.yaml)
- [Cortex Search Service API](openapi/cortex-search-service.yaml)
- [Snowflake Database API](openapi/database.yaml)
- [Snowflake Database Role API](openapi/database-role.yaml)
- [Snowflake Dynamic Table API](openapi/dynamic-table.yaml)
- [Snowflake Event Table API](openapi/event-table.yaml)
- [Snowflake External Volume API](openapi/external-volume.yaml)
- [Snowflake Function API](openapi/function.yaml)
- [Snowflake Grant API](openapi/grant.yaml)
- [Snowflake Iceberg Table API](openapi/iceberg-table.yaml)
- [Snowflake Image Repository API](openapi/image-repository.yaml)
- [Snowflake Managed Account API](openapi/managed-account.yaml)
- [Snowflake Network Policy API](openapi/network-policy.yaml)
- [Snowflake Notebook API](openapi/notebook.yaml)
- [Snowflake Notification Integration API](openapi/notification-integration.yaml)
- [Snowflake Pipe API](openapi/pipe.yaml)
- [Snowflake Procedure API](openapi/procedure.yaml)
- [Snowflake Result API](openapi/result.yaml)
- [Snowflake Role API](openapi/role.yaml)
- [Snowflake Schema API](openapi/schema.yaml)
- [Snowflake Service API](openapi/service.yaml)
- [Snowflake SQL API](openapi/sqlapi.yaml)
- [Snowflake SQL REST API](openapi/snowflake-sql-rest-api.yaml)
- [Snowflake Stage API](openapi/stage.yaml)
- [Snowflake Stream API](openapi/stream.yaml)
- [Snowflake Table API](openapi/table.yaml)
- [Snowflake Task API](openapi/task.yaml)
- [Snowflake User Defined Function API](openapi/user-defined-function.yaml)
- [Snowflake User API](openapi/user.yaml)
- [Snowflake View API](openapi/view.yaml)
- [Snowflake Warehouse API](openapi/warehouse.yaml)

## Capabilities

Naftiko capabilities organized as shared per-API definitions composed into customer-facing workflows.

### Shared Per-API Definitions

- [Snowflake Account](capabilities/shared/account.yaml) — 4 operations for account management
- [Snowflake Alert](capabilities/shared/alert.yaml) — 5 operations for alert management
- [Snowflake API Integration](capabilities/shared/api-integration.yaml) — 4 operations for API integration management
- [Snowflake Catalog Integration](capabilities/shared/catalog-integration.yaml) — 4 operations for catalog integration management
- [Snowflake Compute Pool](capabilities/shared/compute-pool.yaml) — 4 operations for compute pool management
- [Snowflake Cortex Analyst](capabilities/shared/cortex-analyst.yaml) — 4 operations for natural language analytics
- [Snowflake Cortex Inference](capabilities/shared/cortex-inference.yaml) — 2 operations for LLM inference
- [Snowflake Cortex Search](capabilities/shared/cortex-search-service.yaml) — 2 operations for semantic search
- [Snowflake Database](capabilities/shared/database.yaml) — 9 operations for database management
- [Snowflake Database Role](capabilities/shared/database-role.yaml) — 4 operations for database role management
- [Snowflake Dynamic Table](capabilities/shared/dynamic-table.yaml) — 7 operations for dynamic table management
- [Snowflake Event Table](capabilities/shared/event-table.yaml) — 4 operations for event table management
- [Snowflake External Volume](capabilities/shared/external-volume.yaml) — 4 operations for external volume management
- [Snowflake Function](capabilities/shared/function.yaml) — 5 operations for function management
- [Snowflake Grant](capabilities/shared/grant.yaml) — 3 operations for grant management
- [Snowflake Iceberg Table](capabilities/shared/iceberg-table.yaml) — 5 operations for Iceberg table management
- [Snowflake Image Repository](capabilities/shared/image-repository.yaml) — 4 operations for image repository management
- [Snowflake Managed Account](capabilities/shared/managed-account.yaml) — 3 operations for managed account management
- [Snowflake Network Policy](capabilities/shared/network-policy.yaml) — 4 operations for network policy management
- [Snowflake Notebook](capabilities/shared/notebook.yaml) — 5 operations for notebook management
- [Snowflake Notification Integration](capabilities/shared/notification-integration.yaml) — 4 operations for notification integration management
- [Snowflake Pipe](capabilities/shared/pipe.yaml) — 5 operations for pipe management
- [Snowflake Procedure](capabilities/shared/procedure.yaml) — 5 operations for procedure management
- [Snowflake Result](capabilities/shared/result.yaml) — 1 operations for result retrieval
- [Snowflake Role](capabilities/shared/role.yaml) — 4 operations for role management
- [Snowflake Schema](capabilities/shared/schema.yaml) — 6 operations for schema management
- [Snowflake Service](capabilities/shared/service.yaml) — 8 operations for container service management
- [Snowflake SQL API](capabilities/shared/sqlapi.yaml) — 3 operations for SQL execution
- [Snowflake Stage](capabilities/shared/stage.yaml) — 5 operations for stage management
- [Snowflake Stream](capabilities/shared/stream.yaml) — 4 operations for stream management
- [Snowflake Table](capabilities/shared/table.yaml) — 6 operations for table management
- [Snowflake Task](capabilities/shared/task.yaml) — 7 operations for task management
- [Snowflake User](capabilities/shared/user.yaml) — 4 operations for user management
- [Snowflake User Defined Function](capabilities/shared/user-defined-function.yaml) — 4 operations for UDF management
- [Snowflake View](capabilities/shared/view.yaml) — 4 operations for view management
- [Snowflake Warehouse](capabilities/shared/warehouse.yaml) — 4 operations for warehouse management

### Workflow Capabilities

| Workflow | APIs Combined | Tools | Persona |
|----------|--------------|-------|---------|
| [Data Management](capabilities/data-management.yaml) | Database + Schema + Table + View + Dynamic Table + Iceberg Table + Event Table + External Volume | 26 | Data Engineer |
| [Data Engineering](capabilities/data-engineering.yaml) | SQL API + Task + Stream + Pipe + Stage + Function + Procedure + UDF + Result | 24 | Data Engineer |
| [Cortex AI](capabilities/cortex-ai.yaml) | Cortex Analyst + Cortex Inference + Cortex Search + Notebook | 10 | Data Scientist |
| [Security and Access](capabilities/security-and-access.yaml) | User + Role + Grant + Database Role + Network Policy + Account + Managed Account | 15 | Platform Admin |
| [Compute and Services](capabilities/compute-and-services.yaml) | Warehouse + Compute Pool + Service + Image Repository + Alert | 17 | Platform Engineer |
| [Integrations and Connectors](capabilities/integrations-and-connectors.yaml) | API Integration + Catalog Integration + Notification Integration | 12 | Platform Engineer |

## Maintainers

**FN:** Kin Lane

**Email:** kin@apievangelist.com
