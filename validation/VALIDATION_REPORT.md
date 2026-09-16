# Migration Validation Report

_Generated 2026-09-16 12:20:37 UTC_

## Accuracy / confidence

Percentages are computed from inventory JSON / OBJECT_MAPPING / COVERAGE only. They measure migration generation coverage — NOT live Looker KPI parity or warehouse deploy success. Confidence reflects evidence completeness, not business acceptance.

**Overall conversion done:** **81.9%**  
**Left:** **18.1%**  
**Confidence:** **HIGH**  
Formula: `0.15*P1 + 0.45*P2 + 0.40*P3 (renormalized if a phase is missing)`  
Weights: `{'phase1': 0.15, 'phase2': 0.45, 'phase3': 0.4}`

## Phase breakdown

### Phase 1 — Extract / inventory

- Done: **100.0%** | Left: **0.0%**
- Confidence: **HIGH** — File presence + OBJECT_COUNTS evidence; extract is deterministic (pbixray).
- Source PBIX: `Human Resources Sample PBIX.pbix`
- Evidence: `{"counts": {"tables": 15, "business_tables": 9, "internal_tables": 6, "columns": 87, "measures": 30, "calculated_columns": 43, "calculated_tables": 6, "relationships": 8, "power_query": 9, "m_files": 9, "rls_roles": 0, "hierarchies": 7, "partitions": 122, "auto_date_tables": 6, "annotations": 158, "`

### Phase 2 — Semantic model / LookML

- Done: **83.0%** | Left: **17.0%**
- Confidence: **HIGH** — Weighted from phase2/OBJECT_MAPPING.json statuses (mapped=1.0, partial=0.5, todo=0). Placeholder connection/dataset still require user input.
- Source PBIX: `Human Resources Sample PBIX.pbix`
- Evidence: `{"object_count": 47, "status_counts": {"todo": 8, "mapped": 39}, "kind_counts": {"measure": 30, "view": 9, "join": 8}, "views": 9, "measures": 30, "relationships": 8, "placeholder_lookml_files": 19}`

Remaining (sample):
- `{'kind': 'measure', 'lookml': 'measure:emp_count', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:actives', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:new_hires_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:actives_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:seps_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:emp_count_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:bad_hires_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:to_pct_norm', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`

### Phase 3 — Dashboards / visuals

- Done: **73.8%** | Left: **26.2%**
- Confidence: **HIGH** — Weighted visual coverage from phase3/inventory/COVERAGE.json (decorative skips excluded; mapped/partial/gap weights fixed).
- Source PBIX: `Human Resources Sample PBIX.pbix`
- Evidence: `{"visual_total": 36, "status_counts": {"gap": 4, "partial": 14, "mapped": 18}, "dashboards": 5, "target_pct": 70, "meets_target": true}`

Remaining (sample):
- `{'page': 'Info', 'title': 'VisualContainer', 'pbi_type': 'image', 'status': 'gap', 'looker': 'manual', 'notes': 'Image tile — not auto-ported; add manually or as text note'}`
- `{'page': 'Info', 'title': 'VisualContainer1', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'New Hires', 'title': 'VisualContainer', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'New Hires', 'title': 'VisualContainer2', 'pbi_type': 'lineClusteredColumnComboChart', 'status': 'gap', 'looker': 'gap', 'notes': 'Unknown/unsupported visual type `lineClusteredColumnComboChart` — document as GAP'}`
- `{'page': 'New Hires', 'title': 'VisualContainer5', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'New Hires', 'title': 'VisualContainer6', 'pbi_type': 'lineStackedColumnComboChart', 'status': 'partial', 'looker': 'looker_column (partial)', 'notes': 'Combo chart → looker_column or looker_line (combo not 1:1)'}`
- `{'page': 'New Hires', 'title': 'VisualContainer7', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'New Hires', 'title': 'VisualContainer8', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Actives and Separations', 'title': 'VisualContainer', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Actives and Separations', 'title': 'VisualContainer1', 'pbi_type': 'lineClusteredColumnComboChart', 'status': 'gap', 'looker': 'gap', 'notes': 'Unknown/unsupported visual type `lineClusteredColumnComboChart` — document as GAP'}`
- `{'page': 'Actives and Separations', 'title': 'VisualContainer5', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Actives and Separations', 'title': 'VisualContainer6', 'pbi_type': 'lineClusteredColumnComboChart', 'status': 'gap', 'looker': 'gap', 'notes': 'Unknown/unsupported visual type `lineClusteredColumnComboChart` — document as GAP'}`
- `{'page': 'Actives and Separations', 'title': 'VisualContainer8', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Bad Hires', 'title': 'VisualContainer', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Bad Hires', 'title': 'VisualContainer1', 'pbi_type': 'donutChart', 'status': 'partial', 'looker': 'looker_pie', 'notes': 'PBI aggregation on Employee.BadHires mapped to field ref; confirm a measure exists on employee (Phase 2) or add type:sum'}`

## Where YOU must provide input in LookML

Findings: **84** across **35** files.  
By severity: `{'HIGH': 48, 'MEDIUM': 30, 'LOW': 6}`  
By category: `{'measure_todo': 27, 'warehouse_binding': 47, 'connection': 1, 'descriptions': 2, 'looker_platform': 5, 'dashboard_gap': 2}`

| Severity | File | Line | Snippet | What you must do |
|---|---|---:|---|---|
| HIGH | `phase2/lookml/m_migration/M_QUERY_RECOMMENDATIONS.md` | 50 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/age_group_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.age_group` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/bu_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/date_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/employee_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/ethnicity_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/fp_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/gender_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/pay_type_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.pay_type` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/separation_reason_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separation_reason` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/age_group.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.age_group` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/bu.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/date.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.date` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/employee.sql` | 6 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.employee` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/ethnicity.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.ethnicity` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/fp.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.fp` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/gender.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.gender` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/pay_type.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.pay_type` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/separation_reason.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.separation_reason` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 5 | `connection: "YOUR_LOOKER_CONNECTION"` | Set Looker connection name (Admin > Connections) |
| HIGH | `phase2/lookml/views/age_group.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.age_group` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/bu.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/date.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/employee.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/ethnicity.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/fp.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/gender.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/pay_type.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.pay_type` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/separation_reason.view.lkml` | 9 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separation_reason` ;;` | Replace BigQuery project.dataset in sql_table_name |
| MEDIUM | `phase2/lookml/MEASURE_DEPENDENCIES.md` | 14 | `/ `new_hires_sply` / New Hires / complex_todo / TODO /` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 4 | `# TODO: set connection to your Looker Admin connection name` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 23 | `description: "Migrated from Power BI (Human Resources Sample PBIX.pbix). KPI par` | Explore/view notes KPI parity still required |
| MEDIUM | `phase2/lookml/views/employee.view.lkml` | 136 | `description: "From Power BI measure `EmpCount`. Strategy=complex_todo. Complex /` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/views/employee.view.lkml` | 138 | `# TODO: complex DAX — keep original expression; validate KPI parity before produ` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase3/lookml_dashboards/dashboards/bad_hires.dashboard.lookml` | 53 | `# deficiency: PBI aggregation on Employee.BadHires mapped to field ref; confirm ` | Dashboard tile deficiency — verify field or replace gap tile |
| LOW | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 23 | `description: "Migrated from Power BI (Human Resources Sample PBIX.pbix). KPI par` | Optional: rewrite explore/dashboard description for end users |
| LOW | `phase3/lookml_dashboards/dashboards/actives_and_separations.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/bad_hires.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/info.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/new_hires.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/new_hires_scorecard.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |

## Next steps

- 1. Fix HIGH items first: connection + YOUR_PROJECT.YOUR_DATASET in every view/model.
- 2. Implement Phase 2 TODO measures (complex DAX) and re-validate KPIs vs Power BI.
- 3. Open Phase 3 dashboards; replace gap/partial tiles listed in remaining work.
- 4. Re-run validation/run_validation.py after edits to refresh this report.
