"""Deterministic Power Query M → Looker / warehouse recommendation engine.

Best-practice priority (Looker docs + looker-skills):
1. Warehouse / ETL table (dbt/Dataform/SQL) + straight LookML view (sql_table_name)
2. SQL Derived Table (SDT) only as a temporary bridge for light SQL-shaped logic
3. Native Derived Table (NDT) is rarely the right M replacement (prefer warehouse)
4. Never re-implement heavy M (merge/append/complex transforms) only in LookML
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


# Looker / migration pattern IDs
PATTERN_WAREHOUSE_STRAIGHT_VIEW = "warehouse_table_plus_straight_view"
PATTERN_SQL_DERIVED_TABLE = "lookml_sql_derived_table"
PATTERN_WAREHOUSE_SEED = "warehouse_seed_plus_straight_view"
PATTERN_WAREHOUSE_TRANSFORM = "warehouse_transform_model"


@dataclass
class MRecommendation:
    query_name: str
    recommended_pattern: str
    looker_object: str
    rationale: str
    confidence: str  # high | medium | low
    build_in: str  # warehouse | lookml | either
    source_type: str | None = None
    tags: list[str] = field(default_factory=list)
    m_signals: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)
    sql_stub: str = ""
    lookml_stub: str = ""
    prefer_over_sdt: bool = True
    column_casts: list[tuple[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["column_casts"] = [{"column": c, "m_type": t} for c, t in self.column_casts]
        return d


_TYPE_MAP = {
    "int64.type": "INT64",
    "int32.type": "INT64",
    "type number": "FLOAT64",
    "type text": "STRING",
    "type datetime": "TIMESTAMP",
    "type date": "DATE",
    "type logical": "BOOL",
    "percentage.typeid": "FLOAT64",
    "currency.typeid": "FLOAT64",
}


def _m_type_to_sql(m_type: str) -> str:
    key = re.sub(r"\s+", " ", (m_type or "").strip().lower())
    return _TYPE_MAP.get(key, "STRING")


def extract_column_casts(expression: str) -> list[tuple[str, str]]:
    """Parse Table.TransformColumnTypes column list from M when present."""
    expr = expression or ""
    casts: list[tuple[str, str]] = []
    # {"col", Int64.Type} or {"col", type text}
    for col, typ in re.findall(
        r'\{\s*"([^"]+)"\s*,\s*([^}]+?)\}',
        expr,
    ):
        typ_clean = typ.strip().rstrip(",")
        if "Type" in typ_clean or typ_clean.startswith("type "):
            casts.append((col, typ_clean))
    return casts


def extract_file_hint(expression: str) -> str | None:
    m = re.search(r'File\.Contents\(\s*"([^"]+)"', expression or "")
    if m:
        return m.group(1).replace("\\", "/")
    m = re.search(r'Csv\.Document\([^,]+\s*"([^"]+\.csv)"', expression or "", re.I)
    return m.group(1) if m else None


def extract_sql_from_m(query: dict) -> str | None:
    stmts = query.get("sql_statements") or []
    if stmts:
        if isinstance(stmts[0], dict):
            return stmts[0].get("sql") or stmts[0].get("statement") or str(stmts[0])
        return str(stmts[0])
    expr = query.get("expression") or ""
    m = re.search(r'Value\.NativeQuery\([^,]+,\s*"((?:\\.|[^"\\])*)"', expr)
    if m:
        return m.group(1).replace('\\"', '"')
    return None


def classify_m_query(query: dict) -> MRecommendation:
    """Return deterministic Looker/warehouse recommendation for one M query."""
    name = query.get("query_name") or query.get("name") or "unnamed"
    expr = query.get("expression") or ""
    source_type = (query.get("source_type") or "").lower()
    tags = list(query.get("tags") or [])
    casts = extract_column_casts(expr)
    signals: list[str] = []

    has_sql = bool(query.get("has_sql")) or bool(query.get("sql_statements"))
    has_union = bool(query.get("has_append_union"))
    has_merge = bool(query.get("has_merge_join"))
    embedded = bool(query.get("is_embedded_static"))
    heavy = bool(query.get("is_transformation_heavy"))
    file_src = source_type == "file" or "file_source" in tags
    sql_src = source_type in {"sql", "database", "odbc"} or has_sql

    if file_src:
        signals.append("file_source")
    if sql_src:
        signals.append("sql_source")
    if embedded:
        signals.append("embedded_static")
    if has_union:
        signals.append("append_union")
    if has_merge:
        signals.append("merge_join")
    if heavy:
        signals.append("transformation_heavy")
    if casts:
        signals.append(f"column_casts:{len(casts)}")

    # --- Decision tree (best practice) ---
    if embedded:
        return _seed_rec(name, query, signals, casts)
    if has_union or has_merge or heavy:
        return _warehouse_transform_rec(name, query, signals, casts)
    if file_src:
        return _file_to_warehouse_rec(name, query, signals, casts)
    if sql_src:
        return _sql_source_rec(name, query, signals, casts)
    # fallback
    return _warehouse_transform_rec(name, query, signals + ["fallback"], casts)


def _view_name(query_name: str) -> str:
    from .naming import lookml_view_name

    return lookml_view_name(query_name)


def _sql_cast_list(casts: list[tuple[str, str]]) -> str:
    if not casts:
        return "  -- TODO: add columns from Phase 1 inventory / M Changed Type step\n  *\n"
    lines = []
    for col, m_type in casts:
        sql_t = _m_type_to_sql(m_type)
        safe = col.replace("`", "")
        lines.append(f"  CAST(`{safe}` AS {sql_t}) AS `{safe}`")
    return ",\n".join(lines) + "\n"


def _file_to_warehouse_rec(
    name: str, query: dict, signals: list[str], casts: list[tuple[str, str]]
) -> MRecommendation:
    v = _view_name(name)
    path = extract_file_hint(query.get("expression") or "") or "path/to/source.csv"
    sql = f"""-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `{name}` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_{v}`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.{v}` AS
SELECT
{_sql_cast_list(casts)}FROM `YOUR_PROJECT.YOUR_DATASET.stg_{v}`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- {path}
"""
    lookml = f"""# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: {v} {{
  label: "{name}"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.{v}` ;;

  # Add dimensions from Phase 1 inventory / generated views/{v}.view.lkml
  # Keep primary_key: yes on the natural key.
}}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: {v}_sdt {{
#   derived_table: {{
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_{v}`
#     ;;
#   }}
# }}
"""
    return MRecommendation(
        query_name=name,
        recommended_pattern=PATTERN_WAREHOUSE_STRAIGHT_VIEW,
        looker_object="straight view (sql_table_name) over warehouse table",
        rationale=(
            "M is a file extract with light Promote Headers / Changed Type. "
            "Looker best practice: load to warehouse, then use a normal view — not a derived table."
        ),
        confidence="high",
        build_in="warehouse",
        source_type=query.get("source_type"),
        tags=list(query.get("tags") or []),
        m_signals=signals,
        steps=[
            "Land the CSV/Excel in cloud storage or ingest to a staging table.",
            f"Create curated table `YOUR_PROJECT.YOUR_DATASET.{v}` with casts matching M Changed Type.",
            f"Point generated LookML views/{v}.view.lkml sql_table_name at that table.",
            "Do not use File.Contents paths from M in Looker.",
            "Optional SDT only as a short-term bridge off an already-loaded staging table.",
        ],
        checks=[
            "Warehouse row count ≈ Power BI query row count",
            "Key column unique where M implied a grain",
            "LookML Validator resolves sql_table_name",
        ],
        sql_stub=sql,
        lookml_stub=lookml,
        prefer_over_sdt=True,
        column_casts=casts,
    )


def _sql_source_rec(
    name: str, query: dict, signals: list[str], casts: list[tuple[str, str]]
) -> MRecommendation:
    v = _view_name(name)
    native = extract_sql_from_m(query)
    if native:
        sql_body = native.strip().rstrip(";")
        pattern = PATTERN_SQL_DERIVED_TABLE
        looker_obj = "warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only"
        build_in = "either"
        rationale = (
            "M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, "
            "then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent."
        )
        sql = f"""-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.{v}` AS
{sql_body}
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
"""
        lookml = f"""# Option A (best practice): straight view on warehouse object
view: {v} {{
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.{v}` ;;
}}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: {v}_sdt {{
  derived_table: {{
    sql:
      {sql_body}
    ;;
  }}
  # Declare dimensions for selected columns; set primary_key: yes
}}
"""
        confidence = "high"
    else:
        pattern = PATTERN_WAREHOUSE_STRAIGHT_VIEW
        looker_obj = "straight view over existing database table"
        build_in = "warehouse"
        rationale = (
            "M connects to a database/SQL source without a captured SELECT body. "
            "Point LookML at the underlying warehouse table (or recreate the query in ETL)."
        )
        sql = f"""-- M referenced a database source for `{name}` but no SQL body was captured.
-- Inspect 04_m_raw/{name}.m and recreate as:
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.{v}` AS
SELECT
{_sql_cast_list(casts)}FROM `YOUR_PROJECT.SOURCE_DATASET.{v}`  -- TODO: confirm source table
;
"""
        lookml = f"""view: {v} {{
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.{v}` ;;
}}
"""
        confidence = "medium"

    return MRecommendation(
        query_name=name,
        recommended_pattern=pattern,
        looker_object=looker_obj,
        rationale=rationale,
        confidence=confidence,
        build_in=build_in,
        source_type=query.get("source_type"),
        tags=list(query.get("tags") or []),
        m_signals=signals,
        steps=[
            "Prefer warehouse VIEW/TABLE with the M SQL (or source table).",
            "Use straight LookML view with sql_table_name.",
            "Use SDT only if warehouse object is not ready yet; migrate off SDT later.",
        ],
        checks=[
            "SQL dialect matches Looker connection",
            "Results match Power BI query for a sample filter",
        ],
        sql_stub=sql,
        lookml_stub=lookml,
        prefer_over_sdt=True,
        column_casts=casts,
    )


def _warehouse_transform_rec(
    name: str, query: dict, signals: list[str], casts: list[tuple[str, str]]
) -> MRecommendation:
    v = _view_name(name)
    sql = f"""-- Recommended pattern: WAREHOUSE TRANSFORM MODEL (dbt/Dataform/SQL)
-- Power Query `{name}` has merges/appends/heavy transforms.
-- Best practice: implement transforms in ETL. LookML stays a thin straight view.
-- Do NOT rebuild merge/append logic as LookML derived tables.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.{v}` AS
SELECT
{_sql_cast_list(casts)}-- TODO: translate M merges/appends/filters from 04_m_raw/{name}.m
FROM `YOUR_PROJECT.YOUR_DATASET.stg_{v}_sources`  -- TODO
;

-- dbt-style sketch:
-- models/{v}.sql  ->  SELECT ... FROM {{ ref('upstream') }} ...
"""
    lookml = f"""# After warehouse model exists — straight view only
view: {v} {{
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.{v}` ;;
}}

# NOT recommended: encoding M merge/append as LookML derived_table SQL.
# If you must bridge temporarily, keep SDT minimal and ticket warehouse ownership.
"""
    return MRecommendation(
        query_name=name,
        recommended_pattern=PATTERN_WAREHOUSE_TRANSFORM,
        looker_object="warehouse transform + straight view (avoid SDT for heavy M)",
        rationale=(
            "M contains merge, append/union, or heavy transforms. "
            "Looker skills: keep LookML semantic; put ETL in the warehouse."
        ),
        confidence="high",
        build_in="warehouse",
        source_type=query.get("source_type"),
        tags=list(query.get("tags") or []),
        m_signals=signals,
        steps=[
            f"Read phase1/inventory/04_m_raw/{name}.m end-to-end.",
            "Implement joins/unions/filters in dbt/Dataform/SQL.",
            f"Expose curated table to LookML views/{v}.view.lkml via sql_table_name.",
            "Mark any LookML SDT as temporary technical debt.",
        ],
        checks=[
            "Transform tests (unique key, not null) in warehouse",
            "Row grain matches Power BI",
            "No fan-out vs related facts",
        ],
        sql_stub=sql,
        lookml_stub=lookml,
        prefer_over_sdt=True,
        column_casts=casts,
    )


def _seed_rec(
    name: str, query: dict, signals: list[str], casts: list[tuple[str, str]]
) -> MRecommendation:
    v = _view_name(name)
    sql = f"""-- Recommended pattern: WAREHOUSE SEED + straight LookML view
-- Power Query `{name}` looks like an embedded/static table (#table / enter data).
-- Best practice: seed CSV in dbt/Dataform or INSERT seed rows; then straight view.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.{v}` AS
SELECT
{_sql_cast_list(casts)}-- TODO: paste literal rows from M #table / Enter Data
FROM UNNEST([])  -- replace with seed rows
;

-- Alternative small SDT (only if seed is tiny and temporary):
-- view with derived_table sql: SELECT ... UNION ALL SELECT ...
"""
    lookml = f"""view: {v} {{
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.{v}` ;;
}}

# Tiny static alternative (temporary):
# view: {v}_sdt {{
#   derived_table: {{
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }}
#   dimension: id {{ primary_key: yes type: number sql: ${{TABLE}}.id ;; }}
# }}
"""
    return MRecommendation(
        query_name=name,
        recommended_pattern=PATTERN_WAREHOUSE_SEED,
        looker_object="warehouse seed table + straight view (tiny SDT optional)",
        rationale=(
            "Embedded/static M tables should become warehouse seeds. "
            "Straight LookML view afterward; SDT only for tiny temporary seeds."
        ),
        confidence="medium",
        build_in="warehouse",
        source_type=query.get("source_type"),
        tags=list(query.get("tags") or []),
        m_signals=signals,
        steps=[
            "Extract static rows from M into a seed CSV or INSERT script.",
            "Load seed to warehouse.",
            "Use generated straight LookML view.",
        ],
        checks=["Seed row count matches Power BI", "Types match Changed Type"],
        sql_stub=sql,
        lookml_stub=lookml,
        prefer_over_sdt=True,
        column_casts=casts,
    )
