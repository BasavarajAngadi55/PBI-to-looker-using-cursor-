# PHASE 2 — POWER BI → LOOKML MAPPING ASSESSMENT

You are an expert in Power BI Tabular models and Google Looker/LookML.

Phase 1 has already extracted the complete Power BI semantic model.

Your ONLY task in this phase is to create a **Power BI → LookML mapping assessment document**.

## IMPORTANT — DO NOT IMPLEMENT ANYTHING

Do NOT:

* generate LookML files
* generate `.view.lkml`
* generate `.model.lkml`
* generate warehouse SQL
* generate PDTs
* modify the Power BI model
* migrate dashboards
* migrate visuals
* migrate report pages

This phase is **analysis and mapping only**.

The next phase will use this mapping document to generate the actual LookML.

---

# INPUT

Read the Phase 1 outputs:

```text
inventory/01_tables_columns.json
inventory/02_dax_objects.json
inventory/03_relationships.json
inventory/04_power_query_m.json
inventory/05_tmschema_extras.json
inventory/04_m_raw/*.m

OBJECT_INVENTORY.md
ACTION_MATRIX.csv
COMPLETENESS_GATE.json
```

Do not invent any missing information.

If something is not available in the extracted inventory, explicitly say:

`Not available in source extraction`

---

# PRIMARY OUTPUT

Create ONE document:

```text
LOOKML_MAPPING_ASSESSMENT.md
```

The document must contain **section-wise tabular mappings**.

Every section must use a table.

Do NOT create LookML files.

---

# SECTION 1 — TABLES → LOOKML VIEWS

Create a table containing every Power BI table.

Columns:

| Power BI Table | Table Type | Business/Internal | Recommended LookML Object | Suggested View Type | Mapping Status | Comments | Suggestion |
| -------------- | ---------- | ----------------- | ------------------------- | ------------------- | -------------- | -------- | ---------- |

Recommended LookML object will normally be:

`view`

Suggested View Type:

* Dimension
* Fact
* Bridge
* Aggregate
* Date
* Internal/Skip

Mapping Status:

* DIRECT
* PARTIAL
* COMPLEX
* SKIP_INTERNAL
* BLOCKED

Comments should explain why the table maps to that LookML object.

Suggestions should explain anything the next implementation phase needs to consider.

Include Power BI internal tables such as:

```text
LocalDateTable_*
DateTableTemplate_*
```

Do not omit them.

---

# SECTION 2 — COLUMNS → LOOKML DIMENSIONS

Create a table containing every source/business column.

Columns:

| Power BI Table | Power BI Column | Data Type | Calculated? | Recommended LookML Object | LookML Type | Mapping Status | Comments | Suggestion |
| -------------- | --------------- | --------- | ----------- | ------------------------- | ----------- | -------------- | -------- | ---------- |

Recommended LookML object will normally be:

`dimension`

LookML Type examples:

* string
* number
* yesno
* date
* time
* date_time

Consider:

* data type
* nullable behavior if available
* formatting
* hidden status
* sort-by column
* descriptions
* keys
* business meaning

Do not generate actual LookML code.

---

# SECTION 3 — MEASURES → LOOKML MEASURES

Create a table containing **every Power BI measure**.

Columns:

| Table | Measure | Original DAX | Recommended LookML Object | Suggested Measure Type | Mapping Status | Complexity | Comments | Suggestion | KPI Impact |
| ----- | ------- | ------------ | ------------------------- | ---------------------- | -------------- | ---------- | -------- | ---------- | ---------- |

Suggested Measure Type examples:

* sum
* count
* count_distinct
* average
* min
* max
* number
* yesno

Analyze the DAX before deciding the suggested LookML measure type.

Identify measures using complex DAX such as:

```text
CALCULATE
FILTER
ALL
ALLEXCEPT
REMOVEFILTERS
SAMEPERIODLASTYEAR
DATEADD
TOTALYTD
RANKX
SUMX
AVERAGEX
USERELATIONSHIP
SELECTEDVALUE
VALUES
```

For complex measures:

* do NOT force a DIRECT mapping
* mark them PARTIAL or COMPLEX
* explain why
* suggest the likely implementation approach for the next phase

Example comment:

`Uses SAMEPERIODLASTYEAR and requires date-filter context validation.`

Example suggestion:

`Review LookML time-based implementation and validate against Power BI KPI results.`

---

# SECTION 4 — CALCULATED COLUMNS → LOOKML DIMENSIONS / OTHER

Create a table containing **every calculated column**.

Columns:

| Table | Calculated Column | Original DAX | Recommended LookML Object | Mapping Status | Complexity | Comments | Suggestion | Dependency |
| ----- | ----------------- | ------------ | ------------------------- | -------------- | ---------- | -------- | ---------- | ---------- |

Possible recommended object:

* dimension
* dimension_group
* measure
* warehouse calculation
* PDT
* no direct equivalent

Determine whether the calculation is:

* simple row-level logic
* dependent on another table
* dependent on aggregation
* dependent on filter context
* dependent on time intelligence
* complex DAX

Do not implement the calculation.

Only document the recommended destination.

---

# SECTION 5 — CALCULATED TABLES

Create a table containing every calculated table.

Columns:

| Power BI Table | Original DAX | Recommended LookML Representation | Mapping Status | Comments | Suggestion | Dependency |
| -------------- | ------------ | --------------------------------- | -------------- | -------- | ---------- | ---------- |

Possible recommendations:

* LookML view
* warehouse table
* warehouse SQL
* PDT
* seed
* no direct equivalent

Explain why.

---

# SECTION 6 — RELATIONSHIPS → LOOKML JOINS

Create a table containing **every Power BI relationship**.

Columns:

| From Table | From Column | To Table | To Column | Power BI Cardinality | Cross Filter | Active | Recommended LookML Join | LookML Relationship | Mapping Status | Comments | Suggestion |
| ---------- | ----------- | -------- | --------- | -------------------- | ------------ | ------ | ----------------------- | ------------------- | -------------- | -------- | ---------- |

Suggested LookML relationship values:

* many_to_one
* one_to_many
* one_to_one
* many_to_many

Do not blindly copy Power BI terminology.

Analyze how the relationship should behave in Looker.

Flag:

* many-to-many relationships
* bidirectional relationships
* inactive relationships
* ambiguous joins
* bridge tables

---

# SECTION 7 — POWER QUERY / M → LOOKER DATA LAYER

Create a table containing **every Power Query query**.

Columns:

| Power Query | Source | Transformation Type | Referenced Queries | Recommended Destination | Mapping Status | Comments | Suggestion | Impacted Tables/KPIs |
| ----------- | ------ | ------------------- | ------------------ | ----------------------- | -------------- | -------- | ---------- | -------------------- |

Recommended destination can be:

* Warehouse SQL
* Warehouse Seed
* PDT
* Existing warehouse table
* Review Required

Look specifically for:

* SQL queries
* joins
* merges
* appends/unions
* filters
* calculated columns
* custom transformations
* static/embedded data
* query dependencies
* parameters

Do not generate SQL.

Do not generate PDTs.

Only provide the recommendation.

---

# SECTION 8 — HIERARCHIES

Create a table for every Power BI hierarchy.

Columns:

| Table | Hierarchy | Levels | Recommended LookML Approach | Mapping Status | Comments | Suggestion |
| ----- | --------- | ------ | --------------------------- | -------------- | -------- | ---------- |

Possible recommendations:

* drill_fields
* related dimensions
* dimension group
* no direct equivalent
* review required

Do not generate LookML.

---

# SECTION 9 — RLS / SECURITY

Create this section even when there is no RLS.

If RLS exists:

| Role | Table | Power BI Filter | Recommended Looker Security Object | Mapping Status | Comments | Suggestion |
| ---- | ----- | --------------- | ---------------------------------- | -------------- | -------- | ---------- |

Consider:

* user_attribute
* access_grant
* sql_always_where
* sql_always_having

Do not implement security.

If no RLS exists, write:

| RLS  | Status         | Comments                               |
| ---- | -------------- | -------------------------------------- |
| None | NONE_IN_SOURCE | No Power BI RLS roles were identified. |

---

# SECTION 10 — PARTITIONS

Create a table for every partition.

Columns:

| Table | Partition | Source | Mode | Recommended LookML / Warehouse Treatment | Mapping Status | Comments | Suggestion |
| ----- | --------- | ------ | ---- | ---------------------------------------- | -------------- | -------- | ---------- |

Explain whether the partition is:

* relevant to warehouse design
* irrelevant to LookML
* requires warehouse consideration

Do not implement anything.

---

# SECTION 11 — SORT-BY COLUMNS

Create a table for all Power BI Sort By Column configurations.

Columns:

| Table | Column | Sort By Column | Recommended LookML Approach | Mapping Status | Comments | Suggestion |
| ----- | ------ | -------------- | --------------------------- | -------------- | -------- | ---------- |

---

# SECTION 12 — FORMATTING / DISPLAY METADATA

Create a table for important formatting metadata.

Columns:

| Table | Object | Power BI Format | Recommended LookML Formatting | Mapping Status | Comments | Suggestion |
| ----- | ------ | --------------- | ----------------------------- | -------------- | -------- | ---------- |

Consider:

* currency
* percentage
* decimal
* date
* datetime
* custom format strings
* labels
* display folders
* hidden objects

Do not generate LookML.

---

# SECTION 13 — AUTO DATE TABLES

Create a table for every Power BI internal date table.

Columns:

| Internal Table | Columns | Hierarchy | Recommended LookML Treatment | Mapping Status | Comments | Suggestion |
| -------------- | ------- | --------- | ---------------------------- | -------------- | -------- | ---------- |

Recommended treatment will normally be:

`SKIP_INTERNAL`

But explain that a proper Looker date model may need to replace the Power BI auto-date behavior.

---

# SECTION 14 — ANNOTATIONS / OTHER TABULAR METADATA

Create a table for any remaining important metadata.

Columns:

| Object | Metadata Type | Power BI Value | LookML Equivalent | Mapping Status | Comments | Suggestion |
| ------ | ------------- | -------------- | ----------------- | -------------- | -------- | ---------- |

Include:

* annotations
* perspectives
* display folders
* hidden objects
* other model metadata

If a category is empty, explicitly show:

`NONE_IN_SOURCE`

---

# SECTION 15 — COMPLEX / UNMAPPED OBJECTS

This is a very important section.

Create a consolidated table containing anything that cannot be directly mapped.

Columns:

| Object Type | Table | Object | Mapping Status | Why Direct Mapping Is Difficult | Dependency | Recommended Approach | KPI Impact | Priority |
| ----------- | ----- | ------ | -------------- | ------------------------------- | ---------- | -------------------- | ---------- | -------- |

Priority:

* HIGH
* MEDIUM
* LOW

Examples:

```text
SAMEPERIODLASTYEAR
FILTER(ALL(...))
USERELATIONSHIP
complex calculated tables
many-to-many relationships
Power Query transformations
RLS
```

Do not solve them.

Only provide the recommendation for the next implementation phase.

---

# SECTION 16 — OVERALL OBJECT MAPPING SUMMARY

Create one final summary table.

| Power BI Object Type | Total | Direct Mapping | Partial | Complex | Warehouse Required | Skip Internal | Blocked |
| -------------------- | ----: | -------------: | ------: | ------: | -----------------: | ------------: | ------: |
| Tables               |       |                |         |         |                    |               |         |
| Columns              |       |                |         |         |                    |               |         |
| Measures             |       |                |         |         |                    |               |         |
| Calculated Columns   |       |                |         |         |                    |               |         |
| Calculated Tables    |       |                |         |         |                    |               |         |
| Relationships        |       |                |         |         |                    |               |         |
| Power Query          |       |                |         |         |                    |               |         |
| Hierarchies          |       |                |         |         |                    |               |         |
| RLS                  |       |                |         |         |                    |               |         |

Calculate the numbers from the actual inventory.

Do not invent totals.

---

# MAPPING STATUS DEFINITIONS

Use only these statuses:

### DIRECT

Clear one-to-one conceptual mapping exists.

### PARTIAL

Can be represented in LookML but requires additional design or validation.

### COMPLEX

Power BI logic cannot safely be represented as a simple LookML object.

### WAREHOUSE_REQUIRED

Logic should preferably be implemented in the warehouse before LookML.

### SKIP_INTERNAL

Power BI-generated/internal object captured for completeness but normally not migrated directly.

### BLOCKED

Required information is missing.

### NO_DIRECT_EQUIVALENT

LookML does not have a direct equivalent.

---

# IMPORTANT RULES

1. **Every object must be accounted for.**

2. Never silently omit an object.

3. Preserve original DAX in the document.

4. Preserve original M query names and reference them; do not rewrite the M code.

5. Do not generate any LookML code.

6. Do not generate warehouse SQL.

7. Do not claim KPI parity.

8. Do not claim that a complex DAX calculation is equivalent unless the mapping is genuinely clear.

9. For uncertain mappings, use:
   `PARTIAL`, `COMPLEX`, or `BLOCKED`.

10. Every non-direct mapping must contain a useful **Comment** and **Suggestion**.

11. Keep the document focused on what the **next LookML implementation phase** needs to know.

12. Use actual extracted objects from the PBIX. Never use assumptions based on the HR Sample example.

---

# FINAL VALIDATION

Before finishing, verify that every object from the Phase 1 inventory appears in the appropriate section.

Check:

```text
Tables
Columns
Measures
Calculated Columns
Calculated Tables
Relationships
Power Query
Hierarchies
RLS
Partitions
Sort By
Formatting
Auto Date Tables
Annotations
Other TM metadata
```

If something has no LookML equivalent, it must still appear in the assessment.

---

# FINAL OUTPUT

Create ONLY:

```text
LOOKML_MAPPING_ASSESSMENT.md
```

Do not create:

```text
views/
models/
*.view.lkml
*.model.lkml
warehouse_sql/
PDTs
```

At the end of the document include:

# Next Phase

State that this document is the **design/mapping layer only**.

The next phase will use this assessment to generate:

1. Warehouse SQL where required
2. LookML views
3. LookML measures
4. LookML joins
5. LookML model/explore
6. Security implementation
7. KPI parity testing

Do not perform those tasks now.
