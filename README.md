# Power BI → Looker using Cursor

Inventory-first migration of a **Power BI semantic model (PBIX)** to **Google Looker (LookML)**, demonstrated on the Microsoft / obviEnce **Human Resources Sample PBIX**.

This repo shows how Cursor agents can:

1. Extract **every** semantic-model object from a PBIX  
2. Enforce a **completeness gate**  
3. Tag each object with a clear next action  
4. Document **blockers** as `M code → table → KPI` chains  
5. Draft LookML (without claiming KPI parity until warehouse tables exist)

**Out of scope:** report pages, visuals, dashboards, bookmarks, themes.  
**Not using dbt:** use warehouse SQL, Looker PDTs, or LookML dimension SQL instead.

Repo: [BasavarajAngadi55/PBI-to-looker-using-cursor-](https://github.com/BasavarajAngadi55/PBI-to-looker-using-cursor-)

---

## Quick links

| Doc | Purpose |
|-----|---------|
| [PBIX_to_Looker_Inventory_Showcase.pdf](PBIX_to_Looker_Inventory_Showcase.pdf) | Audience-ready PDF walkthrough |
| [PBIX_to_Looker_Inventory_Showcase.md](PBIX_to_Looker_Inventory_Showcase.md) | Same content in Markdown |
| [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) | Clear M → KPI blocker chains |
| [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md) | Early LookML migration notes |
| [inventory/OBJECT_INVENTORY.md](inventory/OBJECT_INVENTORY.md) | Full object inventory |
| [inventory/ACTION_MATRIX.csv](inventory/ACTION_MATRIX.csv) | Object → action backlog (237 rows) |
| [inventory/COMPLETENESS_GATE.json](inventory/COMPLETENESS_GATE.json) | Gate pass/fail evidence |

---

## Why an agentic architecture?

A PBIX is not one file of LookML waiting to happen. It packs:

- Tabular schema (tables, columns, types)
- Relationships (cardinality, cross-filter)
- DAX (measures, calculated columns, calculated tables)
- Power Query **M** (SQL, unions, seeds)
- TM extras (partitions, hierarchies, RLS, auto date tables)

A single “convert to LookML” pass typically:

- Skips or under-documents **M dependencies**
- Stubs complex DAX (`SAMEPERIODLASTYEAR`) as `NULL` without disclosure
- Drops hidden **LocalDateTable_*** objects (incomplete inventory)
- Omits empty categories instead of confirming `NONE_IN_SOURCE`

### Specialist roles + merger

```text
PBIX
  ├─ Agent Schema           → inventory/01_tables_columns.json
  ├─ Agent DAX              → inventory/02_dax_objects.json
  ├─ Agent Relationships    → inventory/03_relationships.json
  ├─ Agent M / Power Query  → inventory/04_power_query_m.json + 04_m_raw/*.m
  ├─ Agent TM Extras        → inventory/05_tmschema_extras.json
  └─ Merger + Gate          → OBJECT_INVENTORY.md
                              ACTION_MATRIX.csv
                              COMPLETENESS_GATE.json
```

In this project the roles ran inside one orchestrator  
[`inventory/capture_pbix_inventory.py`](inventory/capture_pbix_inventory.py)  
(same contracts, single process for consistency).

**Thesis:** *Capture everything. Tag everything. Block with names. Then build LookML.*

---

## What was captured (gate PASSED)

| Object class | Count |
|--------------|------:|
| Tables (business + internal auto date) | 15 |
| Columns | 87 |
| DAX measures (full expression text) | 30 |
| Calculated columns (full text) | 43 |
| Calculated tables (full text) | 6 |
| Relationships | 8 |
| Power Query queries + `.m` files | 9 |
| Empty TM categories listed (not omitted) | 29 |
| Action matrix rows | 237 |

**Internal auto date tables were captured** (`LocalDateTable_*`, `DateTableTemplate_*`) including columns and `Calendar(...)` DAX. They are tagged `SKIP_PBI_INTERNAL` for default Looker migration — **capture ≠ skip extraction**.

---

## Repo layout

```text
├── README.md                          ← you are here
├── PROMPT.md                          ← reusable master prompt
├── BLOCKERS_AND_DEPENDENCIES.md
├── MIGRATION_SUMMARY.md
├── PBIX_to_Looker_Inventory_Showcase.md / .pdf
├── generate_showcase_pdf.py
├── inventory/
│   ├── capture_pbix_inventory.py
│   ├── 01_tables_columns.json
│   ├── 02_dax_objects.json
│   ├── 03_relationships.json
│   ├── 04_power_query_m.json
│   ├── 04_m_raw/*.m                   ← verbatim Power Query
│   ├── 05_tmschema_extras.json
│   ├── OBJECT_INVENTORY.md
│   ├── ACTION_MATRIX.csv
│   └── COMPLETENESS_GATE.json
├── views/                             ← draft LookML views
├── models/human_resources.model.lkml
└── pbix_analysis/                     ← earlier CSV extracts
```

---

## Conversion honesty

| Layer | Progress |
|-------|----------|
| Object capture / inventory | ~95–100% |
| Dim/fact + join design | ~80% |
| Simple measures (draft LookML) | ~70% (need warehouse tables) |
| Complex measures (SPLY, EmpCount, TO % Norm) | ~15–25% |
| Warehouse tables (no dbt) | ~0–10% |
| KPI parity vs Power BI | ~0% (not validated yet) |

**~70–80%** of *understanding/mapping* is done.  
*Runnable* Looker KPI replacement needs warehouse tables + complex DAX + parity checks.

---

## Blocker example (how we document gaps)

```text
BLOCKED: New Hires YoY % Change
  └── needs: New Hires YoY Var
        └── needs: New Hires SPLY     ← LookML (SAMEPERIODLASTYEAR)
              └── needs: New Hires    ← SUM(isNewHire)
                    └── needs: isNewHire  ← DAX calculated column
                          └── needs: hr.employee from Employee.m
                                ← M CODE DEPENDENCY (warehouse / PDT)
```

See [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) for the full map.

---

## How to re-run inventory (optional)

```bash
# Python 3.12 recommended for pbixray
python3.12 -m venv .venv312
source .venv312/bin/activate
pip install pbixray fpdf2

# Point PBIX path inside the script if needed, then:
python inventory/capture_pbix_inventory.py
```

Sample PBIX (external):  
[microsoft/powerbi-desktop-samples — Human Resources Sample PBIX](https://github.com/microsoft/powerbi-desktop-samples/blob/main/Sample%20Reports/Human%20Resources%20Sample%20PBIX.pbix)

---

## Master prompt (copy into a new Cursor chat)

Use the full prompt in **[PROMPT.md](PROMPT.md)**. That file is the detailed, reusable instruction set to accomplish this workflow again on this or another PBIX.

---

## License / attribution

- Methodology & LookML drafts in this repo: project work product for showcase.  
- Sample PBIX content: Microsoft / obviEnce Human Resources sample (see Microsoft Learn / powerbi-desktop-samples).  
- Extraction engine used in development: [pbixray](https://pypi.org/project/pbixray/).
