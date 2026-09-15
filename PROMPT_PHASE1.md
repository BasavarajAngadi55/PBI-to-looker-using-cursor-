# Power BI → Looker Migration — 6-Agent Architecture

You are the **Orchestrator** for a Power BI → Google Looker semantic-model migration.

Your job is to coordinate **5 specialist agents + 1 merger agent**.

We are migrating **only the semantic model and business logic** required for Looker.

Do NOT migrate:

* Power BI report pages
* Visuals
* Dashboards
* Bookmarks
* Themes
* Q&A UI

## INPUT

PBIX file:

`/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`

If the path does not exist, locate the PBIX in the workspace or ask for the correct path.

Workspace:

Use the **currently opened Cursor workspace**.

Create all outputs inside the workspace.

---

# ARCHITECTURE

Run these 5 specialist agents:

1. **Tabular Schema Agent**
2. **Relationships Agent**
3. **DAX Agent**
4. **Power Query M Agent**
5. **TM Extras Agent**

Then run:

6. **Merger Agent**

The Merger Agent combines the outputs from all 5 agents.

The Orchestrator must validate that every agent completed successfully before allowing the merger to run.

---

# COMMON RULES FOR ALL AGENTS

Every agent must:

1. Read the PBIX directly using `pbixray` or an equivalent Power BI extraction method.
2. Never invent objects, columns, relationships, expressions, or metadata.
3. Preserve the **exact original object names**.
4. Preserve the **full original DAX/M expression** where applicable.
5. Capture empty categories as `[]` rather than omitting them.
6. Clearly distinguish:

   * Power BI internal objects
   * Business objects
   * Derived/calculated objects
7. Write its output to the specified `inventory/` location.
8. Return a short completion summary to the Orchestrator.
9. If extraction fails, write the failure to the output and report:
   `BLOCKER → reason → required action`
10. Do not modify another agent's files.

Use Python 3.12 virtual environment if required.

---

# AGENT 1 — TABULAR SCHEMA

## Objective

Extract the complete Tabular model schema.

Capture:

### Tables

For every table:

* table name
* table type
* hidden/visible status
* description if available

### Columns

For every column:

* table name
* column name
* data type
* source column name if available
* hidden/visible
* calculated column indicator
* expression if available
* format string if available
* description if available

### Calculated tables

List calculated tables separately.

Capture:

* table name
* complete DAX expression
* hidden/visible

### Internal tables

Do NOT exclude:

* LocalDateTable_*
* DateTableTemplate_*
* other Power BI-generated tables

Capture them completely.

## Output

Write:

`inventory/01_tables_columns.json`

Suggested structure:

```json
{
  "tables": [],
  "columns": [],
  "calculated_tables": [],
  "internal_tables": []
}
```

## Validation

Report:

* total tables
* total columns
* total calculated columns
* total calculated tables
* internal table count

Do not claim completeness unless extraction was successful.

---

# AGENT 2 — RELATIONSHIPS

## Objective

Extract every relationship in the Tabular model.

For each relationship capture:

* relationship ID if available
* from table
* from column
* to table
* to column
* cardinality
* cross-filter direction
* active/inactive
* relationship type
* any available security/filtering metadata

Examples of cardinality:

* one_to_many
* many_to_one
* one_to_one
* many_to_many

Examples of cross-filter:

* single
* both

## Output

Write:

`inventory/03_relationships.json`

Suggested structure:

```json
{
  "relationships": [
    {
      "from_table": "",
      "from_column": "",
      "to_table": "",
      "to_column": "",
      "cardinality": "",
      "cross_filter": "",
      "active": true
    }
  ]
}
```

## Validation

Report:

* total relationships
* active relationships
* inactive relationships
* cross-filter directions
* cardinality distribution

Do not invent missing metadata.

---

# AGENT 3 — DAX

## Objective

Extract **ALL DAX business logic**.

Capture:

### Measures

For every measure:

* table
* measure name
* complete DAX expression
* format string
* description if available
* hidden/visible
* display folder if available

### Calculated columns

For every calculated column:

* table
* column name
* complete DAX expression
* data type if available
* format string if available

### Calculated tables

For every calculated table:

* table name
* complete DAX expression

Do not simplify or rewrite DAX.

The original DAX must be preserved exactly wherever possible.

## Complexity detection

Flag expressions containing patterns such as:

* CALCULATE
* FILTER
* ALL
* ALLEXCEPT
* REMOVEFILTERS
* SAMEPERIODLASTYEAR
* DATEADD
* TOTALYTD
* MAX
* MIN
* VALUES
* SELECTEDVALUE
* SUMX
* AVERAGEX
* RANKX
* SWITCH
* USERELATIONSHIP
* RELATED
* LOOKUPVALUE

Add a simple classification:

* SIMPLE
* MODERATE
* COMPLEX

This classification is only a migration aid. It does not change the original DAX.

## Output

Write:

`inventory/02_dax_objects.json`

Suggested structure:

```json
{
  "measures": [],
  "calculated_columns": [],
  "calculated_tables": [],
  "complexity_summary": {}
}
```

## Validation

Report:

* measure count
* calculated-column count
* calculated-table count
* simple/moderate/complex counts

---

# AGENT 4 — POWER QUERY M

## Objective

Extract **ALL Power Query / M logic**.

For every Power Query query/table capture:

* query name
* complete M code
* source
* source type
* SQL statements if present
* referenced queries
* joins
* merges
* appends/unions
* filters
* column transformations
* custom columns
* data type transformations
* parameters
* embedded/static tables
* seed data
* dependencies

Do not rewrite M.

Store the raw M code exactly as extracted.

## Important

Identify whether the query contains:

* SQL source
* BigQuery source
* Excel/CSV source
* static/embedded table
* append
* merge
* reference to another query
* custom transformation
* filtering
* calculated column logic

## Outputs

Create:

`inventory/04_power_query_m.json`

And:

`inventory/04_m_raw/`

Create one file per query:

`inventory/04_m_raw/<TableName>.m`

Example:

```text
inventory/
  04_power_query_m.json
  04_m_raw/
    Employee.m
    Department.m
    AgeGroup.m
    Gender.m
```

## Validation

Report:

* total Power Query queries
* queries with SQL
* queries with dependencies
* append/union queries
* merge/join queries
* embedded/static tables
* transformation-heavy queries

---

# AGENT 5 — TABULAR MODEL EXTRAS

## Objective

Extract everything important that is **not already covered by schema, relationships, DAX, or M**.

Capture:

### Partitions

For every table:

* partition name
* source/query
* mode if available
* storage mode
* refresh information if available

### Hierarchies

Capture:

* hierarchy name
* table
* levels
* level order

### RLS

Capture:

* role name
* table
* filter expression
* members if available

If there are no RLS roles, explicitly write:

```json
"rls": []
```

### Perspectives

Capture all perspectives.

If none:

```json
"perspectives": []
```

### Annotations

Capture annotations/custom metadata where available.

### Display folders

Capture if available.

### Sort-by-column metadata

Capture:

* table
* column
* sort-by column

### Format strings

Capture where not already available from Agent 1/3.

### Auto date tables

Capture:

* LocalDateTable_*
* DateTableTemplate_*

Include:

* columns
* hierarchy
* relationships
* metadata

These can later be marked as `SKIP_PBI_INTERNAL`, but they must first be captured.

### Other Tabular metadata

Capture any additional model metadata that may affect Looker migration.

## Output

Write:

`inventory/05_tmschema_extras.json`

Suggested structure:

```json
{
  "partitions": [],
  "hierarchies": [],
  "rls": [],
  "perspectives": [],
  "annotations": [],
  "display_folders": [],
  "sort_by_columns": [],
  "format_strings": [],
  "auto_date_tables": [],
  "other": []
}
```

## Validation

Report counts for every category.

Empty categories must remain present.

---

# AGENT 6 — MERGER

## Objective

Merge the outputs from Agents 1–5 into a single authoritative inventory.

Read:

```text
inventory/01_tables_columns.json
inventory/02_dax_objects.json
inventory/03_relationships.json
inventory/04_power_query_m.json
inventory/05_tmschema_extras.json
inventory/04_m_raw/*.m
```

Do not modify the original specialist files.

---

# MERGER OUTPUT 1 — OBJECT_INVENTORY.md

Create:

`OBJECT_INVENTORY.md`

Organize it into:

## 1. Summary

Show:

* table count
* business table count
* internal table count
* column count
* measure count
* calculated-column count
* calculated-table count
* relationship count
* Power Query query count

## 2. Tables

List every table.

For each:

* type
* columns
* calculated columns
* source/query
* internal/business classification

## 3. Measures

List every measure with:

* table
* measure name
* DAX
* complexity

## 4. Calculated Columns

List every calculated column with:

* table
* column
* DAX
* complexity

## 5. Calculated Tables

List every calculated table.

## 6. Relationships

List every relationship.

## 7. Power Query

List every M query and dependency.

## 8. TM Extras

List:

* partitions
* hierarchies
* RLS
* perspectives
* annotations
* sort-by
* display folders
* auto date tables

## 9. Migration Notes

Explain why direct Power BI → LookML conversion is not enough.

Specifically identify dependencies between:

`M → warehouse layer → calculated columns → measures → LookML`

and:

`relationships → LookML joins`

and:

`date tables → time-based measures`

---

# MERGER OUTPUT 2 — ACTION_MATRIX.csv

Create:

`ACTION_MATRIX.csv`

One row per migration object.

Columns:

```text
object_type
table
object_name
source
action
complexity
dependency
notes
```

Use exactly one primary action per object.

Allowed actions:

```text
LOOKML_VIEW_DIM
LOOKML_VIEW_FACT
LOOKML_MEASURE
LOOKML_JOIN
LOOKML_TODO_COMPLEX
WAREHOUSE_SQL
WAREHOUSE_SEED
SKIP_PBI_INTERNAL
NONE_IN_SOURCE
```

Examples:

```text
measure,Employee,Employee Count,DAX,LOOKML_MEASURE,SIMPLE,,Direct COUNT mapping
```

```text
calculated_column,Employee,TenureDays,DAX,WAREHOUSE_SQL,MODERATE,Employee M query,Implement in warehouse SQL
```

```text
table,LocalDateTable_abc,LocalDateTable_abc,Power BI,SKIP_PBI_INTERNAL,SIMPLE,,Captured but not required as business LookML view
```

```text
measure,Employee,Previous Year Sales,DAX,LOOKML_TODO_COMPLEX,COMPLEX,Date table,SAMEPERIODLASTYEAR requires parity testing
```

Do not create multiple primary actions for one object.

---

# MERGER OUTPUT 3 — COMPLETENESS_GATE.json

Create:

`COMPLETENESS_GATE.json`

The merger must compare extracted counts and objects.

Structure:

```json
{
  "status": "PASS",
  "checks": [
    {
      "name": "table_count",
      "status": "PASS",
      "expected": 15,
      "actual": 15
    },
    {
      "name": "columns",
      "status": "PASS"
    },
    {
      "name": "measures",
      "status": "PASS",
      "expected": 30,
      "actual": 30
    },
    {
      "name": "calculated_columns",
      "status": "PASS",
      "expected": 43,
      "actual": 43
    },
    {
      "name": "calculated_tables",
      "status": "PASS",
      "expected": 6,
      "actual": 6
    },
    {
      "name": "relationships",
      "status": "PASS",
      "expected": 8,
      "actual": 8
    },
    {
      "name": "power_query",
      "status": "PASS",
      "expected": 9,
      "actual": 9
    },
    {
      "name": "tm_empty_categories",
      "status": "PASS"
    }
  ]
}
```

Important:

Do NOT blindly use the HR Sample expected numbers.

Use the PBIX extraction as the source of truth.

The numbers above are only known reference values for the sample PBIX.

---

# COMPLETENESS RULE

The merger status can be:

```text
PASS
```

only when all extraction checks pass.

Otherwise:

```text
FAIL
```

Do not hide missing objects.

Do not assume missing objects are unnecessary.

Do not continue to LookML generation if:

`COMPLETENESS_GATE.json = FAIL`

---

# BLOCKER FORMAT

Whenever something cannot be extracted or understood, use:

```text
BLOCKER
Depends on: <M / DAX / Tabular metadata>
Impact: <what is affected>
Unlocks: <KPI/object>
Resolution: <warehouse SQL / LookML / manual input>
```

Example:

```text
BLOCKER
Depends on: SAMEPERIODLASTYEAR DAX
Impact: Previous Year Revenue
Unlocks: YoY Revenue KPI
Resolution: LookML time comparison + KPI parity test
```

---

# ORCHESTRATOR WORKFLOW

Execute in this order:

### Step 1

Check PBIX path.

### Step 2

Create:

```text
inventory/
inventory/04_m_raw/
```

### Step 3

Run Agents 1–5.

They may run in parallel if the environment supports it.

### Step 4

Validate that all expected output files exist.

### Step 5

Run Merger Agent.

### Step 6

Generate:

```text
OBJECT_INVENTORY.md
ACTION_MATRIX.csv
COMPLETENESS_GATE.json
```

### Step 7

Print a short final report:

```text
PHASE 1 COMPLETE

Tables:
Columns:
Measures:
Calculated Columns:
Calculated Tables:
Relationships:
Power Query Queries:
Internal Date Tables:

Completeness Gate:
PASS / FAIL

Files created:
- ...
- ...
- ...

Blockers:
- ...
```

Do not generate warehouse SQL or LookML in this phase.

The purpose of this 6-agent workflow is to produce a **complete and trustworthy semantic-model inventory first**.

Only after `COMPLETENESS_GATE.json` passes should the next migration phase generate:

`warehouse_sql/`

and then:

`views/`

and:

`models/`.
