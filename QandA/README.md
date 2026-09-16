# QandA — PBIX chat over local Ollama Gemma (Google ADK)

Ask questions about the **current PBIX extract** (Phase 1 inventory, Phase 2 LookML, Phase 3 dashboards, validation).  
Answers are grounded in on-disk artifacts via tools — the model must not invent facts.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the root + 3 sub-agent design.

## Prerequisites

1. Ollama installed and running (`ollama serve`)
2. Pull Gemma:

```bash
cd QandA
chmod +x pull_model.sh
./pull_model.sh
# or: ollama pull gemma3:latest
```

3. Python deps (use repo venv):

```bash
../.venv312/bin/pip install -r requirements.txt
```

Optional model override:

```bash
export QANDA_OLLAMA_MODEL=gemma3:latest   # or gemma4:e2b if preferred
```

## CLI test

```bash
cd QandA
../.venv312/bin/python runner.py "What tables are in the current PBIX?"
```

## Streamlit

Same UI as Phase 1 (`phase1/app.py`) — open the **QandA chat** section after extract (or anytime if inventory exists).

## Accuracy contract

| Allowed | Not allowed |
|---------|-------------|
| Facts from Phase 1/2/3/validation JSON | Invented measures/tables/visuals |
| “Not in current extract” when missing | Mixing stale PBIX outputs without warning |
| `Recommendation:` suggestions | Claiming KPI parity without evidence |
