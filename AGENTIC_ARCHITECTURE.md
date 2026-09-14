# Agentic Architecture - PBIX -> Looker (6 Agents)

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png** for the diagram + full explanation.

## Flow

```text
PBIX
  -> Orchestrator
      -> Agent 1 Schema      -> 01_tables_columns.json
      -> Agent 2 Relations   -> 03_relationships.json
      -> Agent 3 DAX         -> 02_dax_objects.json
      -> Agent 4 Power Query -> 04_power_query_m.json + 04_m_raw/*.m
      -> Agent 5 TM Extras   -> 05_tmschema_extras.json
  -> Merger (only if files exist)
      -> OBJECT_INVENTORY.md
      -> ACTION_MATRIX.csv
      -> COMPLETENESS_GATE.json  (PASS | FAIL)
  -> if PASS -> warehouse -> LookML -> KPI parity
```

## Thesis

Capture everything. Tag everything. Block with names. Then build LookML.

## Run

```bash
.venv312/bin/python inventory/run_phase1_six_agents.py
.venv312/bin/python generate_architecture_assets.py
```
