# Phase 2 — Looker developer mapping + LookML

Deterministic conversion of **Phase 1 inventory** into:

1. **Looker Developer Guide** (PDF) — Power BI object → Looker object + how to create each  
2. **LookML project** (model + views) packaged as **`LOOKML_PROJECT.zip`**

**Approach:** fixed Python rules (no LLM). Standards from [Looker docs](https://cloud.google.com/looker/docs/lookml-terms-and-concepts) and [looker-open-source/looker-skills](https://github.com/looker-open-source/looker-skills).

## Quick start

```bash
# 1) Ensure Phase 1 inventory exists
cd ../phase1
../.venv312/bin/python inventory/run_phase1_six_agents.py "/path/to/file.pbix"

# 2) Generate Phase 2
cd ../phase2
../.venv312/bin/python run_phase2.py
# or architecture diagram only:
../.venv312/bin/python generate_architecture_assets.py
```

## Deliverables

| File | Purpose |
|------|---------|
| [AGENTIC_ARCHITECTURE.pdf](AGENTIC_ARCHITECTURE.pdf) | Deterministic mapping architecture (diagram) |
| [AGENTIC_ARCHITECTURE.png](AGENTIC_ARCHITECTURE.png) | Architecture diagram (PNG) |
| [LOOKER_DEVELOPER_GUIDE.pdf](LOOKER_DEVELOPER_GUIDE.pdf) | Developer how-to + mapping |
| [OBJECT_MAPPING.md](OBJECT_MAPPING.md) | Per-object ledger |
| [LOOKML_PROJECT.zip](LOOKML_PROJECT.zip) | All LookML for import |
| `lookml/models/*.model.lkml` | Explores + joins |
| `lookml/views/*.view.lkml` | Dimensions + measures |

## Before Looker validate

1. Set `connection:` in the model  
2. Replace `` `YOUR_PROJECT.YOUR_DATASET` `` in `sql_table_name`  
3. Rebuild Power Query transforms in the warehouse (M is not LookML)  
4. Resolve measure `TODO` stubs (complex DAX) and run KPI parity checks  

## Layout

```text
phase2/
  AGENTIC_ARCHITECTURE.*   # deterministic architecture (filename legacy like Phase 1)
  PROMPT.md
  run_phase2.py
  generate_architecture_assets.py
  generate_lookml.py
  generate_developer_guide.py
  lib/                 # naming, mapping rules, DAX patterns
  lookml/              # generated
  LOOKML_PROJECT.zip
  LOOKER_DEVELOPER_GUIDE.*
  OBJECT_MAPPING.*
```
