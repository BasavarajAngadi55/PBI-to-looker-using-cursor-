# Agentic Architecture — 3 Phases (Updated)

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png**.

## Overview

```text
PBIX
  └─ PHASE 1 Inventory Orchestrator
        ├─ Agent 1 Schema
        ├─ Agent 2 Relationships
        ├─ Agent 3 DAX
        ├─ Agent 4 Power Query M
        ├─ Agent 5 TM Extras
        └─ Agent 6 Merger + COMPLETENESS_GATE (must PASS)
              │
              ▼
         PHASE 2 Mapping Orchestrator
        ├─ Agent A Tables/Columns
        ├─ Agent B DAX Measures/Calc
        ├─ Agent C Rel / M / TM
        └─ Agent D Merger -> LOOKML_MAPPING_ASSESSMENT (+ PDF)
              │
              ▼
         PHASE 3 Implementation Orchestrator
        ├─ Agent W Warehouse gaps (base tables assumed)
        ├─ Agent L LookML accountability
        └─ Outputs in phase3/ (views, model, gap SQL templates, docs)
              │
              ▼
         KPI Parity Validation (not automatic)
```

## Folders

| Phase | Path |
|-------|------|
| 1 | `inventory/` |
| 2 | `phase2_agents/` + `LOOKML_MAPPING_ASSESSMENT.*` |
| 3 | `phase3/` + `phase3_agents/` |

## Principle

**100% object accountability**, not 100% forced conversion.

Base warehouse tables are assumed present. Capture **M/DAX gaps** (seeds, transforms, calculated columns) and build LookML on top.
