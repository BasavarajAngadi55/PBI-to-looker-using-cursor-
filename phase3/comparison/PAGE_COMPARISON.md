# Power BI page → Looker dashboard comparison

**Source:** `dashboards.pbix`  
**Looker model/explore:** `dashboards` / `facttable`  
**Weighted completion:** **83.9%** (target ≥ 70%: YES)

## Status summary

- Total visuals: 83 (decorative skips: 8)
- Status counts: {'partial': 22, 'skip': 8, 'mapped': 48, 'gap': 5}

## Visual type equivalence

| Power BI | Looker | Status | Notes |
|---|---|---|---|
| `card` | `single_value` | mapped | KPI card → single_value tile |
| `kpi` | `single_value` | partial | KPI with goal/trend → single_value (goal/trend not fully mirrored) |
| `columnChart` | `looker_column` | mapped | Column chart → looker_column |
| `clusteredColumnChart` | `looker_column` | mapped | Clustered columns → looker_column |
| `clusteredBarChart` | `looker_bar` | mapped | Bar chart → looker_bar |
| `barChart` | `looker_bar` | mapped | Bar chart → looker_bar |
| `lineChart` | `looker_line` | mapped | Line chart → looker_line |
| `areaChart` | `looker_area` | mapped | Area chart → looker_area |
| `stackedAreaChart` | `looker_area` | partial | Stacked area → looker_area (stacking may differ) |
| `pieChart` | `looker_pie` | mapped | Pie → looker_pie |
| `donutChart` | `looker_pie` | partial | Donut → looker_pie (donut style limited) |
| `pivotTable` | `looker_grid` | mapped | Matrix/pivot → looker_grid |
| `tableEx` | `looker_grid` | mapped | Table → looker_grid |
| `table` | `looker_grid` | mapped | Table → looker_grid |
| `slicer` | `dashboard filter` | mapped | Slicer → dashboard filter (not a tile) |
| `textbox` | `text` | partial | Text box → text tile (rich formatting limited) |
| `shape` | `skip` | skip | Decorative shape — no Looker equivalent (skip) |
| `image` | `manual` | gap | Image tile — not auto-ported; add manually or as text note |
| `actionButton` | `button/gap` | gap | Action button — Looker button needs explicit URL; stub as note |
| `map` | `looker_map` | partial | Map → looker_map if geo fields exist; else gap |
| `filledMap` | `looker_google_map` | partial | Filled map → google map / choropleth if supported |
| `treemap` | `looker_pie (substitute)` | partial | Treemap has no direct Looker twin → pie/column substitute |
| `lineStackedColumnComboChart` | `looker_column (partial)` | partial | Combo chart → looker_column or looker_line (combo not 1:1) |
| `waterfallChart` | `looker_waterfall` | mapped | Waterfall → looker_waterfall |
| `funnel` | `looker_funnel` | mapped | Funnel → looker_funnel |
| `scatterChart` | `looker_scatter` | mapped | Scatter → looker_scatter |

## Page: Project Overview

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |

## Page: Executive Summary

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| shape_0 | `shape` | `skip` | skip | - |
| shape_1 | `shape` | `skip` | skip | - |
| CountPatient | `card` | `single_value` | mapped | - |
| Insurance_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| textbox_4 | `textbox` | `text` | partial | - |
|  Monthly Expenses Trends | `areaChart` | `looker_area` | mapped | PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum; PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Patient Growth Over Time | `areaChart` | `looker_area` | mapped | - |
|  CPT Units Monthly Distribution | `columnChart` | `looker_column` | mapped | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
|  Payer-wise CPT Units | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Gross Expenses | `card` | `single_value` | mapped | PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Insurance_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Patient_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Monthly Net Revenue | `kpi` | `single_value` | partial | - |
| Monthly Insurance Revenue | `kpi` | `single_value` | partial | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Monthly Patient Revenue  | `kpi` | `single_value` | partial | PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
|  Monthly Procedure Volume | `kpi` | `single_value` | partial | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| actionButton_16 | `actionButton` | `button/gap` | gap | no fields bound from prototypeQuery — tile will be incomplete |
| image_17 | `image` | `manual` | gap | - |
| TotalPayment | `card` | `single_value` | mapped | PBI aggregation on FactTable.TotalPayment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Yearly Avg. Patient Payment Trend | `kpi` | `single_value` | partial | unbound field Date Year |
| Monthly Payment Performance | `kpi` | `single_value` | partial | unbound field Date Month |
| Optimized Quarterly Expenditure | `kpi` | `single_value` | partial | unbound field Date Quarter |
| Deficit Reduction Efficiency - Monthly | `kpi` | `single_value` | partial | unbound field Date Month |

## Page: Hospital Insights

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| shape_0 | `shape` | `skip` | skip | - |
| shape_1 | `shape` | `skip` | skip | - |
| CptGrouping | `card` | `single_value` | mapped | PBI aggregation on CptCode_Lookup.CptGrouping mapped to field ref; confirm a measure exists on cptcode_lookup (Phase 2) or add type:sum |
| Patient_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Insurance_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| textbox_5 | `textbox` | `text` | partial | - |
| Monthly ARGE Ratio Trend | `lineChart` | `looker_line` | mapped | - |
| AR | `card` | `single_value` | mapped | PBI aggregation on FactTable.AR mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| HospitalName | `card` | `single_value` | mapped | PBI aggregation on Hospital_Lookup.HospitalName mapped to field ref; confirm a measure exists on hospital_lookup (Phase 2) or add type:sum |
| CPTUnits | `card` | `single_value` | mapped | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Monthly IPTP Ratio Trend | `lineChart` | `looker_line` | mapped | - |
|  Gross Expenses by CptGrouping | `pieChart` | `looker_pie` | mapped | PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
|  CPT Units Distribution by Hospital | `treemap` | `looker_pie (substitute)` | partial | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Critical Hospital Metrics Overview | `pivotTable` | `looker_grid` | mapped | PBI aggregation on FactTable.AR mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Hospital  | `slicer` | `dashboard filter` | mapped | - |
| Region | `slicer` | `dashboard filter` | mapped | - |
| textbox_16 | `textbox` | `text` | partial | - |
| image_17 | `image` | `manual` | gap | - |

## Page: Patient Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| shape_0 | `shape` | `skip` | skip | - |
| shape_1 | `shape` | `skip` | skip | - |
| City | `card` | `single_value` | mapped | PBI aggregation on Patient_Lookup.City mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add type:sum |
| Patient_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Insurance_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| textbox_5 | `textbox` | `text` | partial | - |
| DistinctPatient | `card` | `single_value` | mapped | - |
| dimPatientFK | `card` | `single_value` | mapped | PBI aggregation on FactTable.dimPatientFK mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| State | `card` | `single_value` | mapped | PBI aggregation on Patient_Lookup.State mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add type:sum |
| Gender | `slicer` | `dashboard filter` | mapped | - |
| Blood Group | `slicer` | `dashboard filter` | mapped | - |
| Patient by Tobacco | `donutChart` | `looker_pie` | partial | - |
| Patient By Exercise | `donutChart` | `looker_pie` | partial | - |
| Patient by Alcohol | `donutChart` | `looker_pie` | partial | - |
| Patient by Diet | `donutChart` | `looker_pie` | partial | - |
| Distinct Patients by BloodGroup | `clusteredColumnChart` | `looker_column` | mapped | - |
| Patient Gender Distribution by State | `pivotTable` | `looker_grid` | mapped | - |
| Region Code | `slicer` | `dashboard filter` | mapped | - |
| Distribution of Patient by State | `map` | `looker_map` | partial | map may lack location dimension — verify geo fields |
| image_19 | `image` | `manual` | gap | - |
| PatientAge | `card` | `single_value` | mapped | PBI aggregation on Patient_Lookup.PatientAge mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add type:sum |
| Region | `slicer` | `dashboard filter` | mapped | - |

## Page: Payer-Provider Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| shape_0 | `shape` | `skip` | skip | - |
| shape_1 | `shape` | `skip` | skip | - |
| City | `card` | `single_value` | mapped | PBI aggregation on Patient_Lookup.City mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add type:sum |
| Patient_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Insurance_Payment | `card` | `single_value` | mapped | PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| textbox_5 | `textbox` | `text` | partial | - |
| ProviderName | `card` | `single_value` | mapped | PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum |
| ProviderFTE | `card` | `single_value` | mapped | PBI aggregation on Physcian_Lookup.ProviderFTE mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum |
| ProviderSpecialty | `card` | `single_value` | mapped | PBI aggregation on Speciality_Lookup.ProviderSpecialty mapped to field ref; confirm a measure exists on speciality_lookup (Phase 2) or add type:sum |
| Gender | `slicer` | `dashboard filter` | mapped | - |
| Blood Group | `slicer` | `dashboard filter` | mapped | - |
| Regional Breakdown of Provider Specialties | `columnChart` | `looker_column` | mapped | PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum |
| Regional Physician Count Analysis | `columnChart` | `looker_column` | mapped | PBI aggregation on Physcian_Lookup.dimPhysicianPK mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum |
| Monthly Provider Activity Overview and CPT Units | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum; PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum |
| Holistic Provider Performance Matrix | `pivotTable` | `looker_grid` | mapped | PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2) or add type:sum; PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| image_15 | `image` | `manual` | gap | - |
| Region Code | `slicer` | `dashboard filter` | mapped | - |

## Page: Monthly Expenses Trends

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Monthly Aggregate Expenses: Gross and Adjusted | `stackedAreaChart` | `looker_area` | partial | PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type:sum |
| Adjustment factor (%) | `slicer` | `dashboard filter` | mapped | - |

## Looker dashboard files

- `lookml_dashboards/dashboards/project_overview.dashboard.lookml`
- `lookml_dashboards/dashboards/executive_summary.dashboard.lookml`
- `lookml_dashboards/dashboards/hospital_insights.dashboard.lookml`
- `lookml_dashboards/dashboards/patient_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/payer_provider_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/monthly_expenses_trends.dashboard.lookml`
