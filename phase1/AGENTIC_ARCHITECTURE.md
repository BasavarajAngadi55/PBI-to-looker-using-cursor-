# Deterministic Extraction Architecture — Phase 1

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf** (filenames kept for links).

## Important

Phase 1 is a **deterministic** Python + `pbixray` pipeline — **not** an LLM / agentic system.  
The six “stages” are specialist extract modules (fixed code). Same PBIX → same inventory.

## Extract stages

| Stage | Role | Does |
|-------|------|------|
| 1 Schema | Structure | Tables, columns, types, LocalDate* internals, calc tables |
| 2 Relationships | Graph / joins | From/to, cardinality, cross-filter, active |
| 3 DAX | Business logic | Full measures + calc columns/tables DAX |
| 4 Power Query M | Data prep | Verbatim M + `04_m_raw/*.m` + SQL/seed tags |
| 5 TM Extras | Metadata | Partitions, hierarchies, RLS, auto dates |
| 6 Merger | Combine + summarize | `OBJECT_INVENTORY.md` + `OBJECT_COUNTS.json` |

Flow: **PBIX → Orchestrator → Stages 1–5 → Merger → DATA_MODEL**

## Make it agentic (optional)

**By enabling natural-language conversation on top of this extract, the system becomes agentic.**  
Users can ask any question about the **current** PBIX (the one just uploaded — inventory is replaced each run).  

- Extract = deterministic (no LLM, no invent)  
- NL layer = agentic Q&A over that PBIX’s inventory only  
