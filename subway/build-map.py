#!/usr/bin/env python3
"""Build the Snowflake API tube-style map.

~40 of Snowflake's APIs grouped onto 7 product lines including a closed
loop for the Cortex AI family.
"""

import sys
from pathlib import Path

sys.path.insert(0, "/Users/kinlane/GitHub/all/.claude/skills")
from _subway_engine import build_subway  # noqa: E402

ABBREV = {
    "Image Repository":       "Image Repo",
    "User-Defined Function":  "UDF",
    "Notification Integration":"Notification Int.",
    "API Integration":        "API Int.",
    "Catalog Integration":    "Catalog Int.",
    "External Volume":        "External Volume",
    "Network Policy":         "Net Policy",
    "Network Rule":           "Net Rule",
    "Password Policy":        "Pass Policy",
    "Spark Connect":          "Spark Connect",
    "Streamlit":              "Streamlit",
    "Database Role":          "DB Role",
    "Managed Account":        "Mgd Account",
    "Snowpipe REST API":      "Snowpipe",
    "Artifact Repository":    "Artifact Repo",
}

LINES = [
    {
        "name": "Database Objects",
        "color": "#29B5E8",  # Snowflake blue
        "stations": [
            ("Database",    (260, 200)),
            ("Schema",      (380, 175)),
            ("Table",       (500, 165)),
            ("View",        (620, 165)),
            ("Function",    (740, 175)),
            ("Procedure",   (860, 200)),
            ("Sequence",    (980, 230)),
        ],
    },
    {
        "name": "Compute & Streaming",
        "color": "#1E5BD0",
        "stations": [
            ("Warehouse",      (270, 320)),
            ("Compute Pool",   (430, 295)),
            ("Service",        (590, 320)),
            ("Stream",         (760, 295)),
            ("Pipe",           (920, 320)),
        ],
    },
    {
        "name": "Special Tables",
        "color": "#0E9D6E",
        "stations": [
            ("Iceberg Table", (300, 430)),
            ("Dynamic Table", (530, 410)),
            ("Event Table",   (770, 430)),
        ],
    },
    {
        "name": "Cortex AI",
        "color": "#7B3FE4",
        # Closed pentagon — Cortex services form a self-contained AI layer.
        "closed": True,
        "stations": [
            ("Cortex Analyst",   (820, 510)),  # 12 o'clock
            ("Cortex Search",    (886, 555)),  # 2 o'clock
            ("Cortex Inference", (861, 633)),  # 5 o'clock
            ("Cortex Agents",    (779, 633)),  # 7 o'clock
            ("Cortex Embed",     (754, 555)),  # 10 o'clock
        ],
    },
    {
        "name": "Identity & Access",
        "color": "#C5318B",
        "stations": [
            ("User",          (270, 540)),
            ("Role",          (270, 600)),
            ("Database Role", (270, 660)),
            ("Grant",         (320, 715)),
            ("Network Policy",(420, 745)),
        ],
    },
    {
        "name": "Integrations",
        "color": "#E68B1F",
        "stations": [
            ("API Integration",         (490, 545)),
            ("Catalog Integration",     (620, 525)),
            ("Notification Integration",(750, 545)),
        ],
    },
    {
        "name": "Account & Code",
        "color": "#5A6275",
        "stations": [
            ("Account",        (280, 800)),
            ("Managed Account",(420, 800)),
            ("Notebook",       (550, 800)),
            ("Streamlit",      (660, 800)),
            ("SQL API",        (770, 800)),
            ("Snowpipe REST API",(890, 800)),
            ("Stage",          (1010, 800)),
        ],
    },
]

URL_OVERRIDES = {
    "Database":                "https://apis.apis.io/apis/snowflake/snowflake-database-api/",
    "Schema":                  "https://apis.apis.io/apis/snowflake/snowflake-schema-api/",
    "Table":                   "https://apis.apis.io/apis/snowflake/snowflake-table-api/",
    "View":                    "https://apis.apis.io/apis/snowflake/snowflake-view-api/",
    "Function":                "https://apis.apis.io/apis/snowflake/snowflake-function-api/",
    "Procedure":               "https://apis.apis.io/apis/snowflake/snowflake-procedure-api/",
    "Sequence":                "https://apis.apis.io/apis/snowflake/snowflake-sequence-api/",
    "Warehouse":               "https://apis.apis.io/apis/snowflake/snowflake-warehouse-api/",
    "Compute Pool":            "https://apis.apis.io/apis/snowflake/snowflake-compute-pools-api/",
    "Service":                 "https://apis.apis.io/apis/snowflake/snowflake-services-api/",
    "Stream":                  "https://apis.apis.io/apis/snowflake/snowflake-stream-api/",
    "Pipe":                    "https://apis.apis.io/apis/snowflake/snowflake-pipe-api/",
    "Iceberg Table":           "https://apis.apis.io/apis/snowflake/snowflake-iceberg-table-api/",
    "Dynamic Table":           "https://apis.apis.io/apis/snowflake/snowflake-dynamic-table-api/",
    "Event Table":             "https://apis.apis.io/apis/snowflake/snowflake-event-table-api/",
    "Cortex Analyst":          "https://apis.apis.io/apis/snowflake/cortex-analyst-api/",
    "Cortex Search":           "https://apis.apis.io/apis/snowflake/cortex-search-rest-api/",
    "Cortex Inference":        "https://apis.apis.io/apis/snowflake/cortex-inference-api/",
    "Cortex Agents":           "https://apis.apis.io/apis/snowflake/cortex-agents-api/",
    "Cortex Embed":            "https://apis.apis.io/apis/snowflake/cortex-embed-api/",
    "User":                    "https://apis.apis.io/apis/snowflake/snowflake-user-api/",
    "Role":                    "https://apis.apis.io/apis/snowflake/snowflake-role-api/",
    "Database Role":           "https://apis.apis.io/apis/snowflake/snowflake-database-role-api/",
    "Grant":                   "https://apis.apis.io/apis/snowflake/snowflake-grant-api/",
    "Network Policy":          "https://apis.apis.io/apis/snowflake/snowflake-network-policy-api/",
    "API Integration":         "https://apis.apis.io/apis/snowflake/snowflake-api-integration-api/",
    "Catalog Integration":     "https://apis.apis.io/apis/snowflake/snowflake-catalog-integration-api/",
    "Notification Integration":"https://apis.apis.io/apis/snowflake/snowflake-notification-integration-api/",
    "Account":                 "https://apis.apis.io/apis/snowflake/snowflake-account-api/",
    "Managed Account":         "https://apis.apis.io/apis/snowflake/snowflake-managed-account-api/",
    "Notebook":                "https://apis.apis.io/apis/snowflake/snowflake-notebook-api/",
    "Streamlit":               "https://apis.apis.io/apis/snowflake/snowflake-streamlit-api/",
    "SQL API":                 "https://apis.apis.io/apis/snowflake/snowflake-sql-api/",
    "Snowpipe REST API":       "https://apis.apis.io/apis/snowflake/snowpipe-rest-api/",
    "Stage":                   "https://apis.apis.io/apis/snowflake/snowflake-stage-api/",
}


def main():
    seen = set()
    n_unique = 0
    for ln in LINES:
        for (st, _) in ln["stations"]:
            if st not in seen:
                n_unique += 1
                seen.add(st)
    build_subway(
        title="The Snowflake API · Underground Map",
        subtitle=f"{n_unique} APIs · {len(LINES)} functional lines · click any station for the apis.io page",
        lines=LINES,
        abbrev=ABBREV,
        source_label="Source: snowflake/openapi/*.yaml · github.com/api-evangelist/snowflake",
        out_dir=Path(__file__).resolve().parent,
        out_basename="snowflake-subway-map",
        provider_id="snowflake",
        station_url_overrides=URL_OVERRIDES,
    )


if __name__ == "__main__":
    main()
