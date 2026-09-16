# Phase 1 — Power BI semantic inventory

Extract **every** object from a PBIX into an inventory and a **data model** diagram.

**Approach:** **Deterministic** Python + `pbixray` extract (not LLM / not agentic).  
Six specialist **stages** write inventory files; the Streamlit UI only runs that pipeline.

**In scope:** tables, columns, measures, calc columns/tables, relationships, Power Query M, TM extras, data model, simple UI.  
**Out of scope today:** data loading, sample row data, warehouse SQL, LookML, Phase 2/3, LLM Q&A.

**Optional later:** enable **natural-language conversation on top** of the inventory to make the system **agentic** — users can ask any question about the **current** uploaded PBIX (inventory is replaced each extract). Extract itself stays deterministic.

## Quick links

| Doc | Purpose |
|-----|---------|
| [AGENTIC_ARCHITECTURE.pdf](AGENTIC_ARCHITECTURE.pdf) | Deterministic extract architecture (diagram) |
| [AGENTIC_ARCHITECTURE.png](AGENTIC_ARCHITECTURE.png) | Architecture diagram (PNG) |
| [AGENT_VALIDATION_PROOF.pdf](AGENT_VALIDATION_PROOF.pdf) | Proof extract matches live pbixray |
| [AGENT_VALIDATION_PROOF.md](AGENT_VALIDATION_PROOF.md) | Validation checks + evidence |
| [DATA_MODEL.pdf](DATA_MODEL.pdf) | Data model / ER diagram |
| [PROMPT.md](PROMPT.md) | Phase 1 extract prompt |
| [inventory/OBJECT_INVENTORY.md](inventory/OBJECT_INVENTORY.md) | Full object inventory |

## Dynamic workspace rule

`phase1/` is the **only** working folder. Each extract:

1. Clears previous inventory / M files / summary / data-model outputs  
2. Keeps a single PBIX in `phase1/uploads/`  
3. Writes fresh outputs for that PBIX  

No per-PBIX backup folders.

## Simple UI

```bash
../.venv312/bin/streamlit run app.py
```

1. Upload a `.pbix` (or paste a local path)  
2. Click **Extract summary**  
3. Download summary txt/pdf, data model pdf, or full inventory  

## CLI

```bash
cd phase1
../.venv312/bin/python inventory/run_phase1_six_agents.py "/path/to/file.pbix"
../.venv312/bin/python generate_data_model_diagram.py
../.venv312/bin/python generate_summary_pdf.py
../.venv312/bin/python generate_architecture_assets.py
../.venv312/bin/python generate_agent_validation_proof.py
```

## Layout

```text
phase1/
  app.py
  PROMPT.md
  DATA_MODEL.*
  AGENTIC_ARCHITECTURE.*   # deterministic architecture docs (filename legacy)
  AGENT_VALIDATION_PROOF.*
  generate_*.py
  requirements.txt
  inventory/
```

Repo: [BasavarajAngadi55/PBI-to-looker-using-cursor-](https://github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-)
