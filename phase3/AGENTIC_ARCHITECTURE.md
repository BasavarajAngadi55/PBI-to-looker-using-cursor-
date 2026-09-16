# Deterministic Dashboard Migration Architecture — Phase 3

See **AGENTIC_ARCHITECTURE.png** and **AGENTIC_ARCHITECTURE.pdf**.

## Important

Phase 3 is **deterministic** Python — not LLM/agentic.  
It reads PBIX `Report/Layout` + Phase 2 model/explore and emits LookML dashboards with coverage scoring.

## Stages

| Stage | Role | Does |
|-------|------|------|
| 1 Extract | Report layout | Pages, visuals, fields, positions from PBIX |
| 2 Equivalence | Visual map | Fixed PBI visual → Looker element rules |
| 3 Bind | Fields | Map to Phase 2 `view.field` / measures |
| 4 Emit | LookML | One `.dashboard.lookml` per page |
| 5 Coverage | Score | Weighted completion vs 70% target |
| 6 Packager | Deliver | Guide PDF + ZIP + comparison |

Flow: **PBIX Layout → Orchestrator → Stages 1–5 → Packager → LookML dashboards**

## Optional agentic later

NL Q&A over Phase 3 inventory/comparison — extract/mapping stays deterministic.
