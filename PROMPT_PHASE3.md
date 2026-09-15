# PHASE 3 — DOCUMENTATION UPDATE + COMPLETE LOOKML IMPLEMENTATION

You are now starting **Phase 3** of the Power BI → Looker migration.

Phase 1 = Power BI semantic model extraction.

Phase 2 = Power BI → LookML mapping assessment.

Phase 3 = **Build the actual Looker semantic model** based on the approved mapping.

Your job is to:

1. Update the migration documentation.
2. Update the Looker Developer Guide.
3. Build the LookML model step by step.
4. Make sure every mapped Power BI object is accounted for.
5. Clearly document anything that cannot be implemented directly.
6. Never silently drop or invent objects.

---

# INPUTS

Before doing anything, read:

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

LOOKML_MAPPING_ASSESSMENT.md
```

The following are the primary design sources:

```text
OBJECT_INVENTORY.md
LOOKML_MAPPING_ASSESSMENT.md
```

Do not create implementation logic that contradicts these documents without documenting why.

---

# PART 1 — UPDATE MIGRATION SUMMARY

Create or update:

```text
MIGRATION_SUMMARY.md
```

The document should explain the migration from:

```text
Power BI Tabular
        ↓
Power Query / M
        ↓
Warehouse Layer
        ↓
LookML Semantic Model
        ↓
Looker Explore
        ↓
KPI Parity Validation
```

Include:

## 1. Migration Objective

Explain:

* what is being migrated
* what is intentionally not being migrated
* target Looker architecture

## 2. Source Model Summary

Include actual counts:

* tables
* columns
* measures
* calculated columns
* calculated tables
* relationships
* Power Query queries
* hierarchies
* RLS
* partitions
* auto date tables

## 3. Mapping Summary

Summarize:

* direct mappings
* partial mappings
* complex mappings
* warehouse-required mappings
* internal objects
* blocked objects

## 4. Architecture Decisions

Explain why each object is being placed in:

* warehouse
* LookML
* PDT
* security layer
* skipped/internal layer

## 5. Implementation Progress

Maintain a live status table:

| Area               | Total | Completed | Pending | Blocked | Notes |
| ------------------ | ----: | --------: | ------: | ------: | ----- |
| Tables             |       |           |         |         |       |
| Dimensions         |       |           |         |         |       |
| Measures           |       |           |         |         |       |
| Calculated Columns |       |           |         |         |       |
| Calculated Tables  |       |           |         |         |       |
| Joins              |       |           |         |         |       |
| M Transformations  |       |           |         |         |       |
| RLS                |       |           |         |         |       |

Update this document as implementation progresses.

## 6. Known Gaps

Document all unresolved items.

For every gap include:

* object
* reason
* dependency
* impact
* recommended solution
* status

---

# PART 2 — UPDATE LOOKER DEVELOPER GUIDE

Create or update:

```text
LOOKER_DEVELOPER_GUIDE.md
```

This is the implementation guide for a Looker developer who will maintain this migrated model.

Include:

# 1. Project Structure

Document the actual project structure:

```text
inventory/
warehouse_sql/
views/
models/
documentation/
```

Only document folders that actually exist.

---

# 2. Naming Standards

Document:

* view naming
* dimension naming
* measure naming
* join naming
* model naming
* file naming

Use consistent LookML naming.

---

# 3. Power BI → LookML Mapping Rules

Document the conventions used in this migration:

```text
Power BI Table
→ LookML View

Power BI Column
→ LookML Dimension

Power BI Measure
→ LookML Measure

Power BI Relationship
→ LookML Join

Power Query Transformation
→ Warehouse SQL / Seed / PDT

Power BI RLS
→ Looker Security

Power BI Auto Date Table
→ Internal/Skip
```

---

# 4. Measure Development Standards

Explain:

* when to use `sum`
* when to use `count`
* when to use `count_distinct`
* when to use `average`
* when to use `type: number`
* how to handle ratios
* how to use `SAFE_DIVIDE`
* formatting conventions

---

# 5. Complex DAX Standards

Explain how this project handles:

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

Do not claim these are automatically equivalent to LookML.

Explain when warehouse SQL or additional testing is required.

---

# 6. Join Standards

Document:

* join type
* relationship
* SQL ON conditions
* many-to-one handling
* many-to-many handling
* fanout risks
* symmetric aggregate considerations
* bridge tables

---

# 7. Dimension Standards

Document:

* data types
* labels
* descriptions
* hidden fields
* keys
* sort fields
* drill fields
* date dimensions

---

# 8. Security Standards

Document how Power BI RLS is translated to Looker.

Include:

* user attributes
* access grants
* SQL filters
* model/explore security

Do not implement security differently from the mapping assessment without documenting the reason.

---

# 9. Testing Standards

Document:

* object-level validation
* SQL validation
* measure validation
* relationship validation
* Power BI vs Looker KPI comparison
* edge-case testing
* null testing
* duplicate/fanout testing

---

# 10. Developer Rules

Include:

* never silently remove a Power BI object
* preserve business logic
* document complex mappings
* avoid unnecessary PDTs
* prefer warehouse transformations for reusable business logic
* do not hard-code environment-specific project IDs
* use TODO comments for unresolved logic
* validate measures against Power BI

---

# PART 3 — START LOOKML IMPLEMENTATION

Now begin the actual implementation.

The implementation must be **step-by-step**.

Do NOT generate everything blindly in one pass.

Use the following order.

---

# STEP 3.1 — DATA / WAREHOUSE DEPENDENCIES

Review all Power Query M and calculated-column mappings.

Identify which objects require:

```text
WAREHOUSE_SQL
WAREHOUSE_SEED
PDT
```

Create the required warehouse layer only where the mapping assessment says it is required.

Directory:

```text
warehouse_sql/
```

Use BigQuery SQL unless another dialect is explicitly specified.

Never use dbt terminology.

For each generated SQL file include a comment explaining:

```text
Source Power BI object:
Original M/DAX dependency:
Why warehouse transformation is required:
Downstream LookML objects:
```

If a real project/dataset is unavailable, use:

```text
YOUR_PROJECT.YOUR_DATASET
```

Do not invent a real project.

---

# STEP 3.2 — BUILD TABLE VIEWS

Build LookML views for every business table.

Directory:

```text
views/
```

For each table:

1. Create the view.
2. Add all source dimensions.
3. Add keys.
4. Add descriptions.
5. Add labels where appropriate.
6. Add formatting.
7. Add hidden fields where required.
8. Add sort fields where required.
9. Add comments for complex fields.
10. Cross-check against the inventory.

Example structure:

```text
view: employee {
  dimension: employee_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.employee_id ;;
  }

  dimension: department {
    type: string
    sql: ${TABLE}.department ;;
  }
}
```

Do not use this example blindly.

Use the actual extracted schema.

---

# STEP 3.3 — CALCULATED COLUMNS

For every calculated column in:

```text
inventory/02_dax_objects.json
```

and:

```text
LOOKML_MAPPING_ASSESSMENT.md
```

implement according to its approved mapping.

Possible destinations:

```text
LookML dimension
Warehouse SQL
PDT
```

For every calculated column confirm:

```text
Power BI object exists
↓
Mapping exists
↓
Implementation exists
```

If it cannot be implemented safely:

```text
# TODO:
# Power BI DAX:
# Reason:
# Required next step:
```

Never silently omit it.

---

# STEP 3.4 — MEASURES

Implement every Power BI measure.

For each measure:

1. Locate the original DAX.
2. Read the mapping assessment.
3. Determine the recommended LookML measure.
4. Implement the equivalent logic.
5. Preserve formatting.
6. Add comments for complex logic.
7. Mark TODO where exact equivalence cannot yet be guaranteed.

For complex measures, do not fake equivalence.

Example:

```text
# TODO: KPI parity validation required.
# Source Power BI DAX: <original DAX>
# Reason: <reason>
# Recommendation: <recommendation>
```

Every measure must be accounted for.

---

# STEP 3.5 — RELATIONSHIPS / JOINS

Implement every relationship from:

```text
inventory/03_relationships.json
```

into the appropriate model Explore.

For every relationship verify:

* from table
* from column
* to table
* to column
* cardinality
* active/inactive
* cross-filter behavior
* fanout risk

Use:

```text
type: left_outer
```

unless the mapping assessment specifically recommends otherwise.

Use the appropriate:

```text
relationship:
```

based on the actual model.

Do not invent joins.

---

# STEP 3.6 — CALCULATED TABLES

Implement every calculated table according to the mapping assessment.

Possible implementation:

```text
warehouse table
warehouse SQL
seed
PDT
LookML view
```

If there is no safe implementation:

```text
# TODO:
```

and document it in:

```text
MIGRATION_SUMMARY.md
```

---

# STEP 3.7 — HIERARCHIES

Implement the approved hierarchy replacement.

Possible approaches:

```text
drill_fields
dimension groups
related dimensions
```

Do not attempt to reproduce Power BI UI behavior.

Focus only on semantic/navigation behavior required by Looker.

---

# STEP 3.8 — RLS / SECURITY

Only implement RLS if it exists in the source model.

Use the mapping assessment as the source of truth.

Possible Looker mechanisms:

```text
user_attribute
access_grant
sql_always_where
sql_always_having
```

If user attributes or production security configuration are unknown:

```text
# TODO: USER INPUT REQUIRED
```

Do not invent user attribute names.

---

# STEP 3.9 — MODEL / EXPLORE

Create:

```text
models/<model>.model.lkml
```

Add:

* connection placeholder if required
* explores
* all required joins
* labels
* descriptions
* access/security configuration where approved

Do not add joins that are not present in the source model unless explicitly justified.

---

# STEP 3.10 — FINAL OBJECT COVERAGE CHECK

After implementation, compare:

```text
OBJECT_INVENTORY.md
LOOKML_MAPPING_ASSESSMENT.md
```

against:

```text
views/
models/
warehouse_sql/
```

Create:

```text
IMPLEMENTATION_COVERAGE.md
```

with:

| Power BI Object | Expected Destination | Implemented | Status | File | Comments |
| --------------- | -------------------- | ----------- | ------ | ---- | -------- |

Every object must have a row.

Possible statuses:

```text
IMPLEMENTED
PARTIAL
TODO
BLOCKED
SKIP_INTERNAL
```

---

# STEP 3.11 — MISSING OBJECT CHECK

Perform a final automated check.

Look specifically for:

* missing tables
* missing columns
* missing measures
* missing calculated columns
* missing calculated tables
* missing joins
* missing M transformations
* missing RLS
* missing hierarchies
* missing sort-by logic
* missing formatting
* missing internal date metadata

If anything is missing, DO NOT say the implementation is complete.

Add it to:

```text
IMPLEMENTATION_COVERAGE.md
MIGRATION_SUMMARY.md
```

---

# COMMENTS AND SUGGESTIONS

Whenever implementation requires a decision, add a concise comment.

Use this format:

```text
# MIGRATION NOTE:
# Source: Power BI <object>
# Decision: <what was implemented>
# Reason: <why>
# Suggestion: <future improvement if applicable>
```

For unresolved items:

```text
# TODO:
# Source Power BI object: <object>
# Dependency: <dependency>
# Reason blocked: <reason>
# Suggested resolution: <solution>
```

Do not fill gaps with assumptions.

---

# IMPORTANT IMPLEMENTATION PRINCIPLE

The goal is:

```text
100% OBJECT ACCOUNTABILITY
```

not:

```text
100% FORCED CONVERSION
```

A Power BI object that cannot safely map to LookML must remain visible as:

```text
TODO
BLOCKED
PARTIAL
NO_DIRECT_EQUIVALENT
```

It must never disappear.

---

# FINAL VALIDATION

Before finishing Phase 3:

### 1. Schema coverage

Every business table and column is accounted for.

### 2. Measure coverage

Every measure is accounted for.

### 3. Calculated-column coverage

Every calculated column is accounted for.

### 4. Calculated-table coverage

Every calculated table is accounted for.

### 5. Relationship coverage

Every relationship is accounted for.

### 6. M coverage

Every Power Query transformation has a destination or documented blocker.

### 7. Security coverage

RLS is implemented or explicitly documented.

### 8. Internal objects

Auto date tables and other Power BI internal objects remain documented.

### 9. No invented logic

No business logic has been invented to fill gaps.

### 10. No KPI parity claim

Do not claim KPI parity until actual Power BI vs Looker/warehouse data has been compared.

---

# FINAL OUTPUT

The final workspace should contain, as applicable:

```text
MIGRATION_SUMMARY.md
LOOKER_DEVELOPER_GUIDE.md
IMPLEMENTATION_COVERAGE.md

warehouse_sql/

views/

models/
```

Do not remove the Phase 1 or Phase 2 inventory files.

---

# FINAL RESPONSE

Return a concise implementation summary:

```text
PHASE 3 IMPLEMENTATION STATUS

Documentation:
✓ MIGRATION_SUMMARY.md
✓ LOOKER_DEVELOPER_GUIDE.md

Tables:
X / Y implemented

Dimensions:
X / Y implemented

Measures:
X / Y implemented

Calculated Columns:
X / Y implemented

Calculated Tables:
X / Y implemented

Relationships:
X / Y implemented

Power Query:
X / Y implemented

RLS:
X / Y implemented / N/A

Blocked:
X

TODO:
X

Implementation Coverage:
PASS / PARTIAL / FAIL

KPI Parity:
NOT YET VALIDATED

Important Gaps:
- ...
```

Do not say "complete" if any object is missing or unresolved.
