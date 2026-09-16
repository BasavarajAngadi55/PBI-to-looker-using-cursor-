"""Deterministic Power BI object → Looker object mapping rules.

Grounded in:
- Google Looker docs (views, explores, joins, dimensions, measures)
- looker-open-source/looker-skills (lookml-view, lookml-explore, modeling-guidelines)

Each entry includes developer-facing build / check / suggestion text used by the guide PDF.
"""
from __future__ import annotations

OBJECT_EQUIVALENCE: list[dict] = [
    {
        "power_bi": "Table (business)",
        "looker": "view (.view.lkml)",
        "summary": "One business table becomes one LookML view file pointed at a warehouse table.",
        "how_to_create": (
            "Create views/<name>.view.lkml with view: <name> { sql_table_name: ... }. "
            "Every view needs a primary_key dimension (Looker skills / symmetric aggregates)."
        ),
        "build_steps": [
            "Create file views/<snake_case_table>.view.lkml.",
            "Declare view: <name> with label matching the Power BI table business name.",
            "Set sql_table_name to the real warehouse table (replace YOUR_PROJECT.YOUR_DATASET).",
            "Add dimensions for all columns that analysts need.",
            "Put primary_key: yes on the unique key dimension (first field).",
        ],
        "checks": [
            "View compiles in Looker Validator with 0 errors.",
            "sql_table_name resolves on the connection (table exists).",
            "Exactly one primary_key: yes in the view.",
            "Row count in Explore (count) is plausible vs Power BI table rows.",
        ],
        "suggestions": [
            "Prefer clear warehouse names (restaurants, not Sheet1) while keeping friendly labels.",
            "Do not model LocalDateTable_* / DateTableTemplate_* as views.",
            "Hide technical surrogate keys with hidden: yes if users should not see them.",
        ],
        "example": (
            "view: sheet1 {\n"
            "  sql_table_name: `proj.dataset.sheet1` ;;\n"
            "  dimension: restaurant_id {\n"
            "    primary_key: yes\n"
            "    type: number\n"
            "    sql: ${TABLE}.RestaurantID ;;\n"
            "  }\n"
            "}"
        ),
        "refs": [
            "https://cloud.google.com/looker/docs/reference/param-view-view",
            "https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md",
        ],
    },
    {
        "power_bi": "Column",
        "looker": "dimension (or dimension_group for dates)",
        "summary": "Physical columns become dimensions; dates become dimension_group timeframes.",
        "how_to_create": (
            "Add dimension: field { type: ... sql: ${TABLE}.col ;; }. "
            "Date/time columns use dimension_group with timeframes raw/date/week/month/quarter/year."
        ),
        "build_steps": [
            "Map each inventory column to a snake_case LookML field name.",
            "Choose type: string, number, yesno, or time (dimension_group).",
            "For dates, use dimension_group: <name> { type: time timeframes: [...] sql: ... ;; }.",
            "Copy business meaning into label: and description:.",
            "Preserve format intent (currency, percent) via value_format_name when useful.",
        ],
        "checks": [
            "Field appears in Explore field picker with correct label.",
            "Filtering/grouping on the field returns values matching Power BI.",
            "Date fields support month/quarter/year without extra DAX date tables.",
        ],
        "suggestions": [
            "Never expose auto-date table columns; use business dates + timeframes.",
            "Use group_label to cluster related fields (IDs, geography, flags).",
            "If column names have spaces, quote in SQL: ${TABLE}.`Country name`.",
        ],
        "example": (
            "dimension_group: order {\n"
            "  type: time\n"
            "  timeframes: [raw, date, week, month, quarter, year]\n"
            "  sql: ${TABLE}.OrderDate ;;\n"
            "  datatype: date\n"
            "}"
        ),
        "refs": [
            "https://cloud.google.com/looker/docs/reference/param-field-dimension",
            "https://cloud.google.com/looker/docs/reference/param-field-dimension-group",
        ],
    },
    {
        "power_bi": "Measure (DAX)",
        "looker": "measure",
        "summary": "DAX measures become LookML measures using sum/average/count patterns, or TODO stubs for complex DAX.",
        "how_to_create": (
            "Map SUM/AVERAGE/COUNT/DISTINCTCOUNT to type: sum|average|count|count_distinct. "
            "Ratios use type: number + SAFE_DIVIDE. CALCULATE/time-intel become filters, period patterns, or warehouse + TODO."
        ),
        "build_steps": [
            "Classify each DAX expression (simple aggregate vs CALCULATE vs time intelligence).",
            "Implement simple aggregates with type: sum / average / count / count_distinct.",
            "Implement ratios with SAFE_DIVIDE(${num}, ${den}) and value_format_name.",
            "For CALCULATE with simple equality filters, use filters: { field: \"value\" } on a base measure.",
            "For DATESYTD/DATEADD/SUMX/etc., leave TODO and implement with Looker period analysis or warehouse metrics.",
            "Keep original DAX in description: until KPI parity is signed off.",
        ],
        "checks": [
            "Measure returns non-null for a known filter set.",
            "Side-by-side vs Power BI for at least 3 filter combinations.",
            "No fan-out inflation after joins (compare count vs count_distinct on PK).",
        ],
        "suggestions": [
            "Prefer ${dimension} references inside measure sql (looker-skills).",
            "Do not claim parity for COMPLEX DAX without tests.",
            "If PBIX has 0 measures, still add explicit KPIs users expect (counts, averages).",
        ],
        "example": (
            "measure: total_sales {\n"
            "  type: sum\n"
            "  sql: ${sales_amount} ;;\n"
            "  value_format_name: usd_0\n"
            "}\n"
            "measure: avg_rating {\n"
            "  type: average\n"
            "  sql: ${rating} ;;\n"
            "}"
        ),
        "refs": [
            "https://cloud.google.com/looker/docs/reference/param-field-measure",
            "https://cloud.google.com/looker/docs/reference/field-reference",
        ],
    },
    {
        "power_bi": "Relationship (M:1 From->To)",
        "looker": "explore join (relationship: many_to_one)",
        "summary": "Power BI relationships become Explore joins with explicit relationship and sql_on.",
        "how_to_create": (
            "In the model file: explore: fact { join: dim { type: left_outer relationship: many_to_one "
            "sql_on: ${fact.fk} = ${dim.pk} ;; } }. Always set relationship explicitly."
        ),
        "build_steps": [
            "Choose the fact table as the explore base (usually the many side).",
            "For each active M:1 relationship, add a join to the one-side view.",
            "Set type: left_outer (typical) and relationship: many_to_one.",
            "Write sql_on using ${view.field} syntax on both sides.",
            "If the same dim joins twice, use from: + a unique join name (alias).",
            "For joins off an intermediate dim, add required_joins: [intermediate_view].",
        ],
        "checks": [
            "Join keys match Phase 1 inventory from/to columns exactly.",
            "Exploring fact+dim does not multiply fact rows unexpectedly.",
            "Inactive Power BI relationships are not used as the default path.",
        ],
        "suggestions": [
            "M:M is a HIGH risk gap — prefer a warehouse bridge table.",
            "Looker has no inactive join flag; keep inactive paths aliased and hidden until needed.",
            "Always declare relationship: (looker-skills requirement).",
        ],
        "example": (
            "explore: sheet1 {\n"
            "  join: sheet2 {\n"
            "    type: left_outer\n"
            "    relationship: many_to_one\n"
            "    sql_on: ${sheet1.country_code} = ${sheet2.country_id} ;;\n"
            "  }\n"
            "}"
        ),
        "refs": [
            "https://cloud.google.com/looker/docs/reference/param-explore-join",
            "https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-explore/SKILL.md",
        ],
    },
    {
        "power_bi": "Calculated column (DAX)",
        "looker": "dimension (prefer warehouse column)",
        "summary": "Row-level DAX calculated columns should be materialized in the warehouse, then exposed as dimensions.",
        "how_to_create": (
            "Prefer materializing in warehouse SQL, then expose as dimension. "
            "Simple row expressions may use LookML sql:; complex DAX stays as migration TODO."
        ),
        "build_steps": [
            "List every business calculated column from Phase 1 (02_dax_objects.json).",
            "Recreate the expression in warehouse SQL (CASE/TRIM/date logic).",
            "Add the physical column to the warehouse table.",
            "Expose it in the view as a dimension with description noting original DAX.",
            "Only use LookML-only sql: for trivial expressions you accept maintaining in Looker.",
        ],
        "checks": [
            "Warehouse column exists and is populated for sample keys.",
            "Dimension values match Power BI calculated column for sample rows.",
        ],
        "suggestions": [
            "Warehouse-first keeps LookML thin and testable.",
            "Financial month / rating buckets / TRIM fields are typical warehouse CASE statements.",
            "Do not leave DAX in production LookML descriptions without an owner.",
        ],
        "example": (
            "dimension: cuisiness {\n"
            "  description: \"PBI calc: TRIM(Sheet1[Cuisines]) — prefer warehouse\"\n"
            "  type: string\n"
            "  sql: ${TABLE}.cuisiness ;;\n"
            "}"
        ),
        "refs": ["https://cloud.google.com/looker/docs/lookml-terms-and-concepts"],
    },
    {
        "power_bi": "Calculated table",
        "looker": "view (sql_table_name or derived_table)",
        "summary": "DAX calculated tables become warehouse tables (preferred) or LookML derived tables.",
        "how_to_create": (
            "If seeded/small, warehouse seed + standard view. "
            "Otherwise SQL derived table / NDT per lookml-view guidance."
        ),
        "build_steps": [
            "Identify calculated tables in inventory (is_calculated_table).",
            "Decide: materialize in warehouse vs SQL derived table in LookML.",
            "Prefer warehouse for anything used in multiple explores or large grain.",
            "Create the view with primary_key and needed dimensions.",
        ],
        "checks": [
            "Table grain and keys documented.",
            "Joins to the calculated table match Power BI relationships.",
        ],
        "suggestions": [
            "Avoid embedding heavy DAX table logic only inside LookML.",
            "Document why the calculated table exists (seed, bridge, snapshot).",
        ],
        "example": (
            "view: adjustment_factor_pct {\n"
            "  sql_table_name: `proj.dataset.adjustment_factor_pct` ;;\n"
            "  dimension: adjustment_factor_pct {\n"
            "    primary_key: yes\n"
            "    type: number\n"
            "    sql: ${TABLE}.`Adjustment factor (%)` ;;\n"
            "  }\n"
            "}"
        ),
        "refs": [
            "https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md",
        ],
    },
    {
        "power_bi": "Power Query M",
        "looker": "Warehouse / ETL (not LookML)",
        "summary": "M queries are ETL. Rebuild them in the warehouse; LookML only points at finished tables.",
        "how_to_create": (
            "Rebuild M transforms in the warehouse (dbt/Dataform/SQL). "
            "LookML only points sql_table_name at the finished table."
        ),
        "build_steps": [
            "Open each inventory/04_m_raw/<Query>.m file.",
            "Identify source system, filters, merges, type changes, and output grain.",
            "Implement equivalent SQL/dbt model producing the same grain and keys.",
            "Validate row counts and key uniqueness vs Power BI.",
            "Point the LookML view sql_table_name at that model.",
        ],
        "checks": [
            "Every Power Query query has a warehouse owner and job.",
            "LookML does not attempt to re-implement M with Liquid/SQL gymnastics.",
        ],
        "suggestions": [
            "Treat M as the highest-priority migration gap after connection placeholders.",
            "Keep M files as the specification; do not delete Phase 1 inventory.",
        ],
        "example": (
            "# Not LookML — warehouse example\n"
            "# SELECT ... FROM source WHERE ...  -- mirrors Sheet1.m\n"
            "# Then: sql_table_name: `proj.dataset.sheet1` ;;"
        ),
        "refs": ["https://cloud.google.com/looker/docs/lookml-terms-and-concepts"],
    },
    {
        "power_bi": "Hierarchy",
        "looker": "drill_fields / sets / dimension_group timeframes",
        "summary": "Hierarchies become drill paths or timeframes — not separate LookML hierarchy objects.",
        "how_to_create": (
            "Date hierarchies use dimension_group timeframes. "
            "Attribute hierarchies use drill_fields or sets."
        ),
        "build_steps": [
            "For date hierarchies, rely on dimension_group timeframes (year > quarter > month > date).",
            "For attribute hierarchies, add drill_fields: [level1, level2, level3] on the top field.",
            "Optionally create a set: for curated field lists.",
        ],
        "checks": [
            "Users can drill year to month to date in Explores.",
            "No dependency on LocalDateTable_* hierarchies.",
        ],
        "suggestions": [
            "Skip migrating auto-date hierarchies from internal tables.",
            "Use drill_fields on measures for guided analysis paths.",
        ],
        "example": (
            "dimension: country {\n"
            "  type: string\n"
            "  sql: ${TABLE}.Country ;;\n"
            "  drill_fields: [city, locality, restaurant_name]\n"
            "}"
        ),
        "refs": ["https://cloud.google.com/looker/docs/reference/param-field-drill-fields"],
    },
    {
        "power_bi": "RLS / OLS",
        "looker": "access_grant / access_filter / required_access_grants",
        "summary": "Power BI row/object security maps to Looker access filters and grants — not automatic.",
        "how_to_create": (
            "Map roles to Looker user attributes + access_filter on explores, or access_grant on fields."
        ),
        "build_steps": [
            "Read Phase 1 RLS inventory (empty list means none found).",
            "Define Looker user attributes (e.g. country, org_id).",
            "Add access_filter on the explore or required_access_grants on sensitive fields.",
            "Test with users in and out of each role.",
        ],
        "checks": [
            "Unauthorized users cannot see restricted rows/fields.",
            "Authorized users still see full expected grain.",
        ],
        "suggestions": [
            "Even if RLS is empty, confirm with security owners before production.",
            "Prefer access_filter for row security; access_grant for field-level.",
        ],
        "example": (
            "explore: sheet1 {\n"
            "  access_filter: {\n"
            "    field: sheet2.country_name\n"
            "    user_attribute: allowed_country\n"
            "  }\n"
            "}"
        ),
        "refs": [
            "https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-access-grants/SKILL.md",
        ],
    },
    {
        "power_bi": "LocalDateTable_* / DateTableTemplate_*",
        "looker": "Skip (use business date + dimension_group)",
        "summary": "Internal auto-date tables are Power BI implementation detail — do not migrate.",
        "how_to_create": (
            "Do not migrate auto-date tables. Use the business date column with Looker timeframes."
        ),
        "build_steps": [
            "Identify internal tables in inventory and exclude them from LookML views.",
            "Find the real business date column on fact/dim tables.",
            "Model that column as dimension_group.",
        ],
        "checks": [
            "No LocalDateTable_* views in the LookML project.",
            "Time-based analysis works via business dates.",
        ],
        "suggestions": [
            "Mark this as an intentional skip in gap docs (severity LOW).",
        ],
        "example": (
            "# SKIP creating view: local_date_table_...\n"
            "# USE dimension_group on FactTable.ServiceDate instead"
        ),
        "refs": ["https://cloud.google.com/looker/docs/reference/param-field-dimension-group"],
    },
    {
        "power_bi": "Model / Dataset",
        "looker": "model (.model.lkml) + connection",
        "summary": "The Power BI dataset becomes a LookML model file with connection, includes, explores.",
        "how_to_create": (
            "One model file: connection, includes, datagroup, explore(s). "
            "Prefer granular includes over wildcards (lookml-modeling-guidelines)."
        ),
        "build_steps": [
            "Open models/<pbix_stem>.model.lkml from LOOKML_PROJECT.zip.",
            "Set connection: to the Looker Admin connection name.",
            "Keep include: lines for each view (granular includes preferred).",
            "Confirm the primary explore points at the fact view.",
            "Configure datagroup / persist_with when ETL cadence is known.",
        ],
        "checks": [
            "Model appears in Looker and Explore loads.",
            "Includes resolve; no missing view errors.",
        ],
        "suggestions": [
            "Hide dimension-only QA explores from end users (hidden: yes).",
            "One focused explore beats a mega-explore when possible.",
        ],
        "example": (
            "connection: \"warehouse_bq\"\n"
            "include: \"/views/sheet1.view.lkml\"\n"
            "include: \"/views/sheet2.view.lkml\"\n"
            "explore: sheet1 {\n"
            "  label: \"Restaurants\"\n"
            "  description: \"Migrated from Power BI Zomato model.\"\n"
            "}"
        ),
        "refs": [
            "https://cloud.google.com/looker/docs/lookml-terms-and-concepts",
            "https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-modeling-guidelines/SKILL.md",
        ],
    },
]


# Tabular DataType codes (fallback when pandas_dtype missing)
TABULAR_TYPE_CODE = {
    1: "string",
    2: "string",
    6: "number",
    8: "number",
    9: "time",
    10: "number",
    11: "yesno",
}


def lookml_field_type(data_type, pandas_dtype: str | None = None) -> str:
    pd = (pandas_dtype or "").lower()
    if "datetime" in pd or pd.startswith("date"):
        return "time"
    if pd in {"bool", "boolean"}:
        return "yesno"
    if pd in {"int64", "int32", "float64", "float32", "float", "int"}:
        return "number"
    if pd in {"string", "object", "str"}:
        return "string"

    if isinstance(data_type, str):
        dtl = data_type.lower()
        if "datetime" in dtl or dtl == "date":
            return "time"
        if dtl in {"float64", "int64", "double", "decimal"}:
            return "number"
        if dtl in {"string", "text"}:
            return "string"
        if data_type.isdigit():
            return TABULAR_TYPE_CODE.get(int(data_type), "string")
    if isinstance(data_type, int):
        return TABULAR_TYPE_CODE.get(data_type, "string")
    return "string"


def is_internal_table(name: str) -> bool:
    n = name or ""
    return n.startswith("LocalDateTable_") or n.startswith("DateTableTemplate_")


def guess_primary_key(columns: list[dict]) -> str | None:
    """Pick PK column: *PK exact, else FactTablePK-style, else first column."""
    names = [c.get("column_name") for c in columns if c.get("column_name")]
    for n in names:
        if n.endswith("PK") or n.endswith("_pk") or n.lower() == "id":
            return n
    for n in names:
        if "PK" in n or n.lower().endswith("key"):
            return n
    return names[0] if names else None


def cardinality_to_relationship(card: str) -> str:
    c = (card or "").upper().replace(" ", "")
    if c in {"M:1", "MANY:1", "MANYTOONE"}:
        return "many_to_one"
    if c in {"1:M", "1:MANY", "ONETOMANY"}:
        return "one_to_many"
    if c in {"1:1", "ONETOONE"}:
        return "one_to_one"
    if c in {"M:M", "MANY:MANY", "MANYTOMANY"}:
        return "many_to_many"
    return "many_to_one"
