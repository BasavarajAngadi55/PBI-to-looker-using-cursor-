# Deterministic LookML Mapping Architecture — Phase 2

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf** (filenames kept consistent with Phase 1 links).

## Important

Phase 2 is a **deterministic** Python pipeline — **not** an LLM / agentic system.  
It reads Phase 1 inventory and emits LookML + a Looker developer guide with fixed rules. Same inventory → same LookML.

## Mapping stages

| Stage | Role | Does |
|-------|------|------|
| 1 Ingest | Load inventory | Read 01..05 JSON + counts; detect fact; skip internals |
| 2 Equivalence | Object map | PBI → Looker rules; OBJECT_MAPPING; gap flags |
| 3 Views | Dimensions | One view per table; primary_key; dimension_group dates |
| 4 Model/Joins | Explore graph | Model file; explore; joins with explicit relationship |
| 5 Measures | DAX patterns | SUM/AVG/COUNT/ratios; complex DAX → TODO |
| 6 Packager | Guide + ZIP | LOOKER_DEVELOPER_GUIDE.pdf + LOOKML_PROJECT.zip + GAPS |

Flow: **Phase 1 inventory → Orchestrator → Stages 1–5 → Packager → LookML ZIP + Guide PDF**

## After Phase 2 (developer work)

- Set `connection` and real `sql_table_name` values
- Rebuild Power Query M in warehouse / dbt
- Materialize calculated columns; implement complex DAX TODOs
- Close HIGH gaps; validate LookML; side-by-side KPI checks vs Power BI

## Standards

- [LookML terms and concepts](https://cloud.google.com/looker/docs/lookml-terms-and-concepts)
- [looker-open-source/looker-skills](https://github.com/looker-open-source/looker-skills)
