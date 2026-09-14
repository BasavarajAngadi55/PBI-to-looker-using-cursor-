# Power BI → Looker Migration — 6-Agent Architecture

You are the **Orchestrator** for a Power BI → Google Looker semantic-model migration.

Your job is to coordinate **5 specialist agents + 1 merger agent**.

We are migrating **only the semantic model and business logic** required for Looker.

Do NOT migrate:

* Power BI report pages
* Visuals
* Dashboards
* Bookmarks
* Themes
* Q&A UI

## INPUT

PBIX file:

`/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`

If the path does not exist, locate the PBIX in the workspace or ask for the correct path.

Workspace:

Use the **currently opened Cursor workspace**.

Create all outputs inside the workspace.

---

# ARCHITECTURE

Run these 5 specialist agents:

1. **Tabular Schema Agent**
2. **Relationships Agent**
3. **DAX Agent**
4. **Power Query M Agent**
5. **TM Extras Agent**

Then run:

6. **Merger Agent**

The Merger Agent combines the outputs from all 5 agents.

The Orchestrator must validate that every agent completed successfully before allowing the merger to run.

---

# COMMON RULES FOR ALL AGENTS

Every agent must:

1. Read the PBIX directly using `pbixray` or an equivalent Power BI extraction method.
2. Never invent objects, columns, relationships, expressions, or metadata.
3. Preserve the **exact original object names**.
4. Preserve the **full original DAX/M expression** where applicable.
5. Capture empty categories as `[]` rather than omitting them.
6. Clearly distinguish:

   * Power BI internal objects
   * Business objects
   * Derived/calculated objects
7. Write its output to the specified `inventory/` location.
8. Return a short completion summary to the Orchestrator.
9. If extraction fails, write the failure to the output and report:
   `BLOCKER → reason → required action`
10. Do not modify another agent's files.

Use Python 3.12 virtual environment if required.

---

# AGENT 1 — TABULAR SCHEMA

## Output

`inventory/01_tables_columns.json`

---

# AGENT 2 — RELATIONSHIPS

## Output

`inventory/03_relationships.json`

---

# AGENT 3 — DAX

## Output

`inventory/02_dax_objects.json`

---

# AGENT 4 — POWER QUERY M

## Outputs

`inventory/04_power_query_m.json`  
`inventory/04_m_raw/<TableName>.m`

---

# AGENT 5 — TABULAR MODEL EXTRAS

## Output

`inventory/05_tmschema_extras.json`

Empty categories (RLS, perspectives, etc.) must remain present as `[]`.

---

# AGENT 6 — MERGER

## Outputs

`inventory/OBJECT_INVENTORY.md`  
`inventory/ACTION_MATRIX.csv`  
`inventory/COMPLETENESS_GATE.json`

Do **not** generate warehouse SQL or LookML in Phase 1.

Only after `COMPLETENESS_GATE.json = PASS` should later phases generate `warehouse_sql/`, `views/`, and `models/`.

---

## How this repo runs Phase 1

```bash
.venv312/bin/python inventory/run_phase1_six_agents.py
```

Orchestrator implements Agents 1–6 with the contracts above (pbixray extraction; no invented objects; no sample table dumps).
