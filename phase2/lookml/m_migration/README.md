# Power Query M → Looker migration stubs

Generated deterministically from Phase 1 `04_power_query_m.json`.

- `M_QUERY_RECOMMENDATIONS.md` — decision + steps per query
- `sql/` — recommended warehouse SQL stubs
- `lookml_stubs/` — recommended LookML (straight view and/or temporary SDT)

Best practice: implement SQL in the warehouse, then use the generated `views/*.view.lkml` with updated `sql_table_name`.
