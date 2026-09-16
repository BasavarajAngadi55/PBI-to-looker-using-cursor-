# PBI → Looker (Cursor)

## Phase 1 — Extract ([phase1/](phase1/))

Deterministic PBIX extract (Python + `pbixray`) → inventory + data model PDF.

```bash
cd phase1
../.venv312/bin/streamlit run app.py
```

## Phase 2 — Looker mapping ([phase2/](phase2/))

Deterministic inventory → LookML + Looker developer guide PDF + `LOOKML_PROJECT.zip`.

```bash
cd phase2
../.venv312/bin/python run_phase2.py
```

## Phase 3 — Looker dashboards ([phase3/](phase3/))

Deterministic PBIX report Layout → LookML dashboards + coverage + `LOOKML_DASHBOARDS.zip`.

```bash
cd phase3
../.venv312/bin/python run_phase3.py
```

## Validation — conversion scorecard ([validation/](validation/))

Evidence-based **% done / % left** + LookML user-input checklist PDF.

```bash
cd validation
../.venv312/bin/python run_validation.py
```

## QandA — local Gemma chat ([QandA/](QandA/))

Ask questions about the **current PBIX** via Ollama + Google Gemma (ADK: 1 root + 3 specialists).

```bash
cd QandA
./pull_model.sh          # ollama pull gemma3 (or uses gemma4 if already local)
../.venv312/bin/pip install -r requirements.txt
../.venv312/bin/python runner.py "What tables are in the current PBIX?"
```

Chat also appears in the Streamlit UI (`phase1/app.py`).

See [phase1/README.md](phase1/README.md), [phase2/README.md](phase2/README.md), [phase3/README.md](phase3/README.md), [validation/README.md](validation/README.md), and [QandA/README.md](QandA/README.md).
