# Power BI → Looker — Migration Prompts (Index)

Use these **three full prompt files** (paste into a Cursor chat / orchestrator run). Each file includes **all details** for that phase.

| Phase | File | Agents | Purpose |
|-------|------|--------|---------|
| **1 — Inventory** | [PROMPT_PHASE1.md](PROMPT_PHASE1.md) | 6 agents (1–5 parallel, then Merger) | Extract every semantic-model object; completeness gate |
| **2 — Mapping** | [PROMPT_PHASE2.md](PROMPT_PHASE2.md) | Mapping assessment (16 sections); specialists A–C + Merger D optional | Power BI → LookML mapping only — **no LookML / SQL** |
| **3 — Implementation** | [PROMPT_PHASE3.md](PROMPT_PHASE3.md) | Docs + warehouse gaps + LookML build | Build LookML + docs; account for every mapped object |

## Hard rules (all phases)

- Semantic model only — **no** report pages, visuals, dashboards, bookmarks, themes, Q&A UI
- Never invent objects; preserve full DAX/M
- Empty categories as `[]` / `NONE_IN_SOURCE`
- Do not claim KPI parity until validated
- Phase N starts only after Phase N−1 gate / assessment is ready

## PBIX input

`/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`

## Typical flow

```text
PROMPT_PHASE1.md  →  inventory/ + COMPLETENESS_GATE PASS
PROMPT_PHASE2.md  →  LOOKML_MAPPING_ASSESSMENT.md (+ PDF)
PROMPT_PHASE3.md  →  phase3/ views · model · warehouse gaps · coverage docs
```

Architecture diagram: [AGENTIC_ARCHITECTURE.pdf](AGENTIC_ARCHITECTURE.pdf)
