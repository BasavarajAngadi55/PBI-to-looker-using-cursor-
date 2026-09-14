# Power BI to Looker Semantic Inventory Showcase

## Executive summary

This showcase documents a complete, inventory-first methodology for migrating a Power BI semantic model (PBIX) to Google Looker (LookML), using the Microsoft / obviEnce **Human Resources Sample PBIX** as the working example.

**What we proved:** Every semantic-model object can be extracted, catalogued, action-tagged, and linked to blockers (especially Power Query M dependencies) before any LookML is treated as "done."

**Out of scope (by design):** Report pages, visuals, dashboards, bookmarks, themes.

**Not using dbt:** Warehouse SQL / Looker PDTs / LookML dimension SQL instead.

---

## Why an agentic architecture is needed

A PBIX is not one artifact - it is several tightly coupled layers:

1. Tabular schema (tables, columns, types)
2. Relationships (cardinality, cross-filter)
3. DAX (measures, calculated columns, calculated tables)
4. Power Query M (source SQL, unions, seeds, transforms)
5. TM extras (partitions, hierarchies, RLS, annotations, auto date tables)

A single "convert to LookML" pass misses M dependencies, stubs complex DAX silently, and cannot prove completeness.

### Agentic design (specialist roles + merger)

```
PBIX
 +- Agent Schema        -> 01_tables_columns.json
 +- Agent DAX           -> 02_dax_objects.json
 +- Agent Relationships -> 03_relationships.json
 +- Agent M / Power Query -> 04_power_query_m.json + 04_m_raw/*.m
 +- Agent TM Extras     -> 05_tmschema_extras.json
 +- Merger + Gate       -> OBJECT_INVENTORY.md + ACTION_MATRIX.csv + COMPLETENESS_GATE.json
```

**Why specialists:**
- Parallelism and focus (each role has one contract)
- Less hallucination / skipped categories
- Empty categories must be listed as empty (NONE_IN_SOURCE), not omitted
- Merger enforces a hard completeness gate before LookML is trusted

**Implementation note for this engagement:** Roles ran as one orchestrated extractor (`inventory/capture_pbix_inventory.py`) with the same contracts - logical multi-agent architecture, single process for consistency.

---

## Source and workspace

| Item | Value |
|------|-------|
| PBIX | Human Resources Sample PBIX.pbix |
| Path | /Users/.../Downloads/Human Resources Sample PBIX.pbix |
| Engine | pbixray (XPress9 DataModel decompress) |
| Workspace | Desktop/data eng / |
| Reports/dashboards | Excluded |
| dbt | Not used |

---

## What we captured (completeness gate PASSED)

| Object class | Count | Artifact |
|--------------|------:|----------|
| Tables (all) | 15 | 01_tables_columns.json |
| Columns | 87 | 01_tables_columns.json |
| DAX measures (full text) | 30 | 02_dax_objects.json |
| Calculated columns (full text) | 43 | 02_dax_objects.json |
| Calculated tables (full text) | 6 | 02_dax_objects.json |
| Relationships | 8 | 03_relationships.json |
| Power Query queries + .m files | 9 | 04_m_raw/*.m |
| Empty TM categories listed | 29 | 05_tmschema_extras.json |
| Action matrix rows | 237 | ACTION_MATRIX.csv |

Gate rules: table count match, every column listed, full DAX text, all relationships, all M files on disk, empty TM categories explicit.

---

## Tables in the PBIX

### Business tables (9) - Power Query M

Employee (fact), Date, BU, AgeGroup, Ethnicity, FP, Gender, PayType, SeparationReason

### Internal auto date tables (6) - ALSO CAPTURED

DateTableTemplate_*, LocalDateTable_* (x5)

These were fully inventoried (columns + Calendar DAX + 36 calc columns). Tagged SKIP_PBI_INTERNAL for default Looker migration - **capture ≠ skip extraction**.

---

## Action tagging (what to do next)

| Tag | Meaning |
|-----|---------|
| LOOKML_VIEW_DIM / FACT | Build LookML views |
| LOOKML_MEASURE | Straight measure mapping |
| LOOKML_JOIN | Explore joins from relationships |
| LOOKML_TODO_COMPLEX | SPLY, EmpCount max period, TO % Norm |
| WAREHOUSE_SQL / (was DBT_SQL) | Rebuild M/SQL in warehouse or PDT |
| WAREHOUSE_SEED | Embedded M seed tables |
| SKIP_PBI_INTERNAL | Auto date tables - captured, optional LookML |
| NONE_IN_SOURCE | Confirmed empty (e.g. RLS) |

---

## Blocked items - clear M -> KPI chains

Example:

```
BLOCKED: New Hires YoY % Change
  +-- needs New Hires SPLY     (SAMEPERIODLASTYEAR - LookML complex)
        +-- needs New Hires    (SUM isNewHire)
              +-- needs isNewHire (DAX calc column)
                    +-- needs hr.employee from Employee.m  <- M DEPENDENCY
```

Primary blockers:
1. Employee.m not loaded to warehouse -> almost all KPIs blocked
2. Dim M/SQL (Date, BU, FP, ...) missing -> slices blocked
3. Seed M (AgeGroup, Gender, Ethnicity) missing -> diversity KPIs blocked
4. Calc columns (isNewHire, BadHires, tenure, ...) -> named KPI dependencies
5. SPLY / EmpCount / TO % Norm -> LookML complex
6. KPI parity tests not yet run

Full detail: BLOCKERS_AND_DEPENDENCIES.md

---

## LookML produced (draft)

views/*.view.lkml (9 business views), models/human_resources.model.lkml (star explore + 8 joins).

Honest conversion estimate:
- Inventory/mapping: ~95-100%
- Runnable Looker without warehouse: ~40-50%
- After warehouse + simple measures: ~70%
- True 80%+ parity needs SPLY/EmpCount/TO% Norm + KPI checks

---

## Audience takeaways

1. Inventory before LookML - never skip M and calc columns
2. Agentic roles + completeness gate prevent silent gaps
3. Internal auto date tables must be captured even if not migrated
4. Blockers must name the .m file and KPIs above it
5. No dbt required - warehouse SQL / PDT / LookML SQL
6. KPI parity is a separate phase - files ≠ correct numbers

---

## Artifact index

inventory/01-05 JSON, 04_m_raw/*.m, OBJECT_INVENTORY.md, ACTION_MATRIX.csv, COMPLETENESS_GATE.json, views/, models/, BLOCKERS_AND_DEPENDENCIES.md, MIGRATION_SUMMARY.md, capture_pbix_inventory.py
