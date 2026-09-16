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

See [phase1/README.md](phase1/README.md) and [phase2/README.md](phase2/README.md).
