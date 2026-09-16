# PBI → Looker (Cursor)

Phase 1 work lives in **[phase1/](phase1/)**.

**Phase 1 approach:** deterministic PBIX extract (Python + `pbixray`) — not an LLM agent pipeline.  
Each upload keeps only that PBIX’s inventory. Optional later: enable NL conversation on top to make it **agentic** (Q&A about the current PBIX).

```bash
cd phase1
../.venv312/bin/streamlit run app.py
```

See [phase1/README.md](phase1/README.md) for inventory, data model, architecture, and validation proof.
