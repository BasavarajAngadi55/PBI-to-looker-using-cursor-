# QandA PBIX — Architecture

## Goal

Chat over the **current PBIX only**, using local **Ollama + Google Gemma** via **Google ADK**.  
Answers must come from extracted Phase 1 / 2 / 3 / validation artifacts — **no invented facts**. Recommendations are allowed when clearly labeled.

## High-level flow

```text
Streamlit UI (phase1/app.py)
        │
        ▼
QandA/runner.py  (ADK Runner + session)
        │
        ▼
┌───────────────────────────────────────┐
│  ROOT AGENT  (qanda_orchestrator)     │
│  Routes the question; synthesizes     │
│  final answer; never fabricates data  │
└───────────────┬───────────────────────┘
                │ delegates
     ┌──────────┼──────────┐
     ▼          ▼          ▼
 Phase1      Phase2      Phase3+Val
 Specialist   Specialist  Specialist
 (inventory)  (LookML)    (dashboards)
     │          │          │
     └──── tools read JSON/MD from disk for CURRENT PBIX only ────┘
```

## Agents (1 root + 3 sub-agents)

| Agent | Role | Reads |
|-------|------|-------|
| **qanda_orchestrator** (root) | Route + final answer | Sub-agent results only |
| **phase1_inventory_agent** | Tables, columns, measures, relationships, M | `phase1/inventory/*`, `CURRENT_PBIX.json` |
| **phase2_lookml_agent** | Views, joins, mapping, TODOs, placeholders | `phase2/OBJECT_MAPPING*`, `PHASE2_SUMMARY`, `lookml/` |
| **phase3_dashboard_agent** | Pages, visuals, coverage, validation gaps | `phase3/inventory/*`, `validation/*` |

## Accuracy rules (hard)

1. Every turn injects a deterministic **GROUNDING_CONTEXT** pack (current PBIX, counts, phase summaries) before the LLM sees the question.
2. Specialists may call tools for deeper detail; they must not invent missing fields.
3. If tools/context say not found → reply **“Not in current PBIX extract”**.
4. Never mix answers across PBIX files; always ground on `CURRENT_PBIX.json`.
5. Recommendations must be prefixed: `Recommendation:` (not stated as extracted fact).
6. If Phase sources disagree (stale Phase 3), surface that warning.

## Model

- Runtime: **Ollama** (local)
- Default model: `gemma3:latest` (override with `QANDA_OLLAMA_MODEL`)
- ADK binding: `LiteLlm(model="ollama_chat/<model>")`

## Folder layout

```text
QandA/
  ARCHITECTURE.md
  README.md
  requirements.txt
  config.py
  tools/
    pbix_context.py      # CURRENT PBIX + safe JSON loaders
    phase1_tools.py
    phase2_tools.py
    phase3_tools.py
  agents/
    __init__.py
    root_agent.py        # exports root_agent
  runner.py              # ask(question) for Streamlit
  pull_model.sh          # ollama pull helper
```

## Why not invent data?

Deterministic extract already produced the inventory. The LLM is a **navigator + explainer** over that inventory — not a second extract engine.
