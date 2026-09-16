# Migration Validation Report

_Generated 2026-09-16 10:12:19 UTC_

## Accuracy / confidence

Percentages are computed from inventory JSON / OBJECT_MAPPING / COVERAGE only. They measure migration generation coverage — NOT live Looker KPI parity or warehouse deploy success. Confidence reflects evidence completeness, not business acceptance.

**Overall conversion done:** **73.4%**  
**Left:** **26.6%**  
**Confidence:** **MEDIUM**  
Formula: `0.15*P1 + 0.45*P2 + 0.40*P3 (renormalized if a phase is missing)`  
Weights: `{'phase1': 0.15, 'phase2': 0.45, 'phase3': 0.4}`

### Warning

Phase source PBIX names differ — overall % mixes different reports. Sources seen: ['Human Resources Sample PBIX.pbix', 'dashboards.pbix']

## Phase breakdown

### Phase 1 — Extract / inventory

- Done: **100.0%** | Left: **0.0%**
- Confidence: **HIGH** — File presence + OBJECT_COUNTS evidence; extract is deterministic (pbixray).
- Source PBIX: `Human Resources Sample PBIX.pbix`
- Evidence: `{"counts": {"tables": 15, "business_tables": 9, "internal_tables": 6, "columns": 87, "measures": 30, "calculated_columns": 43, "calculated_tables": 6, "relationships": 8, "power_query": 9, "m_files": 9, "rls_roles": 0, "hierarchies": 7, "partitions": 122, "auto_date_tables": 6, "annotations": 158, "`

### Phase 2 — Semantic model / LookML

- Done: **55.3%** | Left: **44.7%**
- Confidence: **HIGH** — Weighted from phase2/OBJECT_MAPPING.json statuses (mapped=1.0, partial=0.5, todo=0). Placeholder connection/dataset still require user input.
- Source PBIX: `Human Resources Sample PBIX.pbix`
- Evidence: `{"object_count": 47, "status_counts": {"todo": 21, "mapped": 26}, "kind_counts": {"measure": 30, "view": 9, "join": 8}, "views": 9, "measures": 30, "relationships": 8, "placeholder_lookml_files": 19}`

Remaining (sample):
- `{'kind': 'measure', 'lookml': 'measure:empcount', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:seps', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:actives', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:new_hires', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:avg_tenure_days', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:avg_tenure_months', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:avg_age', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:sum_of_badhires', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:new_hires_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:actives_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:seps_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:empcount_sply', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:seps_yoy_var', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:actives_yoy_var', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`
- `{'kind': 'measure', 'lookml': 'measure:new_hires_yoy_var', 'pbi': None, 'note': 'TODO in OBJECT_MAPPING'}`

### Phase 3 — Dashboards / visuals

- Done: **83.9%** | Left: **16.1%**
- Confidence: **HIGH** — Weighted visual coverage from phase3/inventory/COVERAGE.json (decorative skips excluded; mapped/partial/gap weights fixed).
- Source PBIX: `dashboards.pbix`
- Evidence: `{"visual_total": 83, "status_counts": {"partial": 22, "skip": 8, "mapped": 48, "gap": 5}, "dashboards": 6, "target_pct": 70, "meets_target": true}`

Remaining (sample):
- `{'page': 'Project Overview', 'title': 'textbox_0', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Executive Summary', 'title': 'textbox_4', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Executive Summary', 'title': 'Monthly Net Revenue', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'KPI with goal/trend → single_value (goal/trend not fully mirrored)'}`
- `{'page': 'Executive Summary', 'title': 'Monthly Insurance Revenue', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum'}`
- `{'page': 'Executive Summary', 'title': 'Monthly Patient Revenue ', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum'}`
- `{'page': 'Executive Summary', 'title': ' Monthly Procedure Volume', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum'}`
- `{'page': 'Executive Summary', 'title': 'actionButton_16', 'pbi_type': 'actionButton', 'status': 'gap', 'looker': 'button/gap', 'notes': 'no fields bound from prototypeQuery — tile will be incomplete'}`
- `{'page': 'Executive Summary', 'title': 'image_17', 'pbi_type': 'image', 'status': 'gap', 'looker': 'manual', 'notes': 'Image tile — not auto-ported; add manually or as text note'}`
- `{'page': 'Executive Summary', 'title': 'Yearly Avg. Patient Payment Trend', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'unbound field Date Year'}`
- `{'page': 'Executive Summary', 'title': 'Monthly Payment Performance', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'unbound field Date Month'}`
- `{'page': 'Executive Summary', 'title': 'Optimized Quarterly Expenditure', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'unbound field Date Quarter'}`
- `{'page': 'Executive Summary', 'title': 'Deficit Reduction Efficiency - Monthly', 'pbi_type': 'kpi', 'status': 'partial', 'looker': 'single_value', 'notes': 'unbound field Date Month'}`
- `{'page': 'Hospital Insights', 'title': 'textbox_5', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`
- `{'page': 'Hospital Insights', 'title': ' CPT Units Distribution by Hospital', 'pbi_type': 'treemap', 'status': 'partial', 'looker': 'looker_pie (substitute)', 'notes': 'PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum'}`
- `{'page': 'Hospital Insights', 'title': 'textbox_16', 'pbi_type': 'textbox', 'status': 'partial', 'looker': 'text', 'notes': 'Text box → text tile (rich formatting limited)'}`

## Where YOU must provide input in LookML

Findings: **146** across **35** files.  
By severity: `{'HIGH': 48, 'MEDIUM': 91, 'LOW': 7}`  
By category: `{'warehouse_binding': 47, 'measure_todo': 43, 'connection': 1, 'descriptions': 2, 'looker_platform': 6, 'dashboard_gap': 47}`

| Severity | File | Line | Snippet | What you must do |
|---|---|---:|---|---|
| HIGH | `phase2/lookml/m_migration/M_QUERY_RECOMMENDATIONS.md` | 50 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/agegroup_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.agegroup` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/bu_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/date_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/employee_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/ethnicity_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/fp_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/gender_recommended.lkml` | 2 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/paytype_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.paytype` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/lookml_stubs/separationreason_recommended.lkml` | 3 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separationreason` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/agegroup.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.agegroup` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/bu.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/date.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.date` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/employee.sql` | 6 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.employee` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/ethnicity.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.ethnicity` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/fp.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.fp` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/gender.sql` | 5 | `CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.gender` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/paytype.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.paytype` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/m_migration/sql/separationreason.sql` | 2 | `CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.separationreason` AS` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 5 | `connection: "YOUR_LOOKER_CONNECTION"` | Set Looker connection name (Admin > Connections) |
| HIGH | `phase2/lookml/views/agegroup.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.agegroup` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/bu.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/date.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/employee.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/ethnicity.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/fp.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/gender.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/paytype.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.paytype` ;;` | Replace BigQuery project.dataset in sql_table_name |
| HIGH | `phase2/lookml/views/separationreason.view.lkml` | 5 | `sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separationreason` ;;` | Replace BigQuery project.dataset in sql_table_name |
| MEDIUM | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 4 | `# TODO: set connection to your Looker Admin connection name` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 23 | `description: "Migrated from Power BI (Human Resources Sample PBIX.pbix). KPI par` | Explore/view notes KPI parity still required |
| MEDIUM | `phase2/lookml/views/bu.view.lkml` | 35 | `description: "From Power BI. Strategy=complex_todo. DAX: COUNTA('BU'[BU])"` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/views/bu.view.lkml` | 37 | `# TODO: complex DAX — see description; validate KPI parity before production` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase2/lookml/views/date.view.lkml` | 95 | `description: "From Power BI. Strategy=complex_todo. DAX: CALCULATE(COUNT([EmplID` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/views/date.view.lkml` | 97 | `# TODO: complex DAX — see description; validate KPI parity before production` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase2/lookml/views/employee.view.lkml` | 132 | `description: "From Power BI. Strategy=complex_todo. DAX: CALCULATE(COUNT([EmplID` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/views/employee.view.lkml` | 134 | `# TODO: complex DAX — see description; validate KPI parity before production` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase2/lookml/views/gender.view.lkml` | 30 | `description: "From Power BI. Strategy=complex_todo. DAX: CALCULATE([TO %], all(G` | Measure stubbed as complex_todo — implement SQL + KPI parity |
| MEDIUM | `phase2/lookml/views/gender.view.lkml` | 32 | `# TODO: complex DAX — see description; validate KPI parity before production` | Resolve TODO — complex DAX / parity / missing logic |
| MEDIUM | `phase3/lookml_dashboards/dashboards/executive_summary.dashboard.lookml` | 40 | `# deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref` | Dashboard tile deficiency — verify field or replace gap tile |
| MEDIUM | `phase3/lookml_dashboards/dashboards/hospital_insights.dashboard.lookml` | 49 | `# deficiency: PBI aggregation on CptCode_Lookup.CptGrouping mapped to field ref;` | Dashboard tile deficiency — verify field or replace gap tile |
| MEDIUM | `phase3/lookml_dashboards/dashboards/monthly_expenses_trends.dashboard.lookml` | 41 | `# deficiency: PBI aggregation on FactTable.Gross Expenses mapped to field ref; c` | Dashboard tile deficiency — verify field or replace gap tile |
| MEDIUM | `phase3/lookml_dashboards/dashboards/patient_analysis.dashboard.lookml` | 67 | `# deficiency: PBI aggregation on Patient_Lookup.City mapped to field ref; confir` | Dashboard tile deficiency — verify field or replace gap tile |
| MEDIUM | `phase3/lookml_dashboards/dashboards/payer_provider_analysis.dashboard.lookml` | 58 | `# deficiency: PBI aggregation on Patient_Lookup.City mapped to field ref; confir` | Dashboard tile deficiency — verify field or replace gap tile |
| LOW | `phase2/lookml/models/human_resources_sample_pbix.model.lkml` | 23 | `description: "Migrated from Power BI (Human Resources Sample PBIX.pbix). KPI par` | Optional: rewrite explore/dashboard description for end users |
| LOW | `phase3/lookml_dashboards/dashboards/executive_summary.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/hospital_insights.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/monthly_expenses_trends.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/patient_analysis.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/payer_provider_analysis.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |
| LOW | `phase3/lookml_dashboards/dashboards/project_overview.dashboard.lookml` | 4 | `preferred_viewer: dashboards-next` | Confirm dashboards-next is enabled in your Looker instance |

## Next steps

- 1. Fix HIGH items first: connection + YOUR_PROJECT.YOUR_DATASET in every view/model.
- 2. Implement Phase 2 TODO measures (complex DAX) and re-validate KPIs vs Power BI.
- 3. Open Phase 3 dashboards; replace gap/partial tiles listed in remaining work.
- 4. Re-run validation/run_validation.py after edits to refresh this report.
