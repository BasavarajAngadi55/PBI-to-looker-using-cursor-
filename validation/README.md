# Validation — conversion score + LookML user-input report

Deterministic evidence report across Phase 1 / 2 / 3:

1. **% conversion done** and **% left** (overall + per phase)
2. **Confidence** on those numbers (evidence-based — not KPI parity)
3. **Where you must edit LookML** (connection, project/dataset, TODOs, gap tiles)

## Quick start

```bash
# After Phase 1–3 have been run for your PBIX:
cd validation
../.venv312/bin/python run_validation.py
```

## Deliverables

| File | Purpose |
|------|---------|
| `VALIDATION_REPORT.pdf` | Printable scorecard + user-input checklist |
| `VALIDATION_REPORT.md` | Same content in Markdown |
| `VALIDATION_REPORT.json` | Machine-readable full detail |
| `VALIDATION_SUMMARY.json` | Short summary for UI |

## How scores are calculated

| Phase | Source of truth | Method |
|-------|-----------------|--------|
| 1 | `phase1/inventory/OBJECT_COUNTS.json` + inventory files | Inventory completeness checks |
| 2 | `phase2/OBJECT_MAPPING.json` statuses | mapped=100%, partial=50%, todo=0% |
| 3 | `phase3/inventory/COVERAGE.json` | Weighted visual coverage (skips excluded) |

**Overall** ≈ `0.15×P1 + 0.45×P2 + 0.40×P3` (renormalized if a phase is missing).

These percentages measure **migration generation coverage**, not live Looker number parity.

## User-input scan

Scans `phase2/lookml/` and Phase 3 dashboard/view LookML for:

- `connection: "YOUR_LOOKER_CONNECTION"`
- `` `YOUR_PROJECT.YOUR_DATASET` `` in `sql_table_name`
- `# TODO` / `complex_todo` measure stubs
- Dashboard `# deficiency:` markers
- Description / KPI-parity reminders
