- dashboard: executive_summary
  title: Executive Summary
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Executive Summary'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Executive Summary</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pexecutive_summary_3_card
    title: 'CountPatient'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.countpatient]
    row: 4
    col: 16
    width: 4
    height: 3

  - name: pexecutive_summary_4_card
    title: 'Insurance_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.insurance_payment]
    row: 7
    col: 8
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: pexecutive_summary_5_textbox
    title: 'textbox_4'
    type: text
    model: dashboards
    explore: facttable
    body_text: 'textbox_4'
    row: 10
    col: 5
    width: 19
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pexecutive_summary_6_areachart
    title: 'Monthly Expenses Trends'
    type: looker_area
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.gross_expenses, facttable.insurance_payment]
    row: 13
    col: 2
    width: 7
    height: 6
    # status=mapped | Area chart → looker_area
    # deficiency: PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add 
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: pexecutive_summary_7_areachart
    title: 'Patient Growth Over Time'
    type: looker_area
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.distinctpatient]
    row: 19
    col: 2
    width: 7
    height: 6

  - name: pexecutive_summary_8_columnchart
    title: 'CPT Units Monthly Distribution'
    type: looker_column
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.cptunits]
    row: 25
    col: 10
    width: 7
    height: 6
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -

  - name: pexecutive_summary_9_clusteredbarchart
    title: 'Payer-wise CPT Units'
    type: looker_bar
    model: dashboards
    explore: facttable
    dimensions: [payer_lookup.payername]
    measures: [facttable.cptunits]
    row: 31
    col: 10
    width: 7
    height: 6
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -

  - name: pexecutive_summary_10_card
    title: 'Gross Expenses'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.gross_expenses]
    row: 37
    col: 2
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add 

  - name: pexecutive_summary_11_card
    title: 'Insurance_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.insurance_payment]
    row: 40
    col: 7
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: pexecutive_summary_12_card
    title: 'Patient_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.patient_payment]
    row: 43
    col: 11
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add

  - name: pexecutive_summary_13_kpi
    title: 'Monthly Net Revenue'
    type: single_value
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.totalpayment, facttable.previous_monthpay]
    row: 46
    col: 21
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)

  - name: pexecutive_summary_14_kpi
    title: 'Monthly Insurance Revenue'
    type: single_value
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.insurance_payment, facttable.previous_monthpay]
    row: 49
    col: 21
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: pexecutive_summary_15_kpi
    title: 'Monthly Patient Revenue'
    type: single_value
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.patient_payment, facttable.previous_monthpay]
    row: 52
    col: 17
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add

  - name: pexecutive_summary_16_kpi
    title: 'Monthly Procedure Volume'
    type: single_value
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.cptunits, facttable.previous_monthpay]
    row: 55
    col: 17
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -

  - name: pexecutive_summary_17_actionbutton
    title: 'actionButton_16'
    type: button
    model: dashboards
    explore: facttable
    # DEFICIENCY: no fields — using explore count as placeholder
    measures: [facttable.count]
    row: 58
    col: 0
    width: 2
    height: 3
    # status=gap | Action button — Looker button needs explicit URL; stub as note
    # deficiency: no fields bound from prototypeQuery — tile will be incomplete

  - name: pexecutive_summary_19_card
    title: 'TotalPayment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.totalpayment]
    row: 61
    col: 20
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.TotalPayment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add ty

  - name: pexecutive_summary_20_kpi
    title: 'Yearly Avg. Patient Payment Trend'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.previous_monthpay, facttable.averagepatientpay]
    row: 64
    col: 17
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: unbound field Date Year

  - name: pexecutive_summary_21_kpi
    title: 'Monthly Payment Performance'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.previous_monthpay, facttable.ytdpayment]
    row: 67
    col: 21
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: unbound field Date Month

  - name: pexecutive_summary_22_kpi
    title: 'Optimized Quarterly Expenditure'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.previous_monthpay, facttable.totalgrossexpense]
    row: 70
    col: 17
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: unbound field Date Quarter

  - name: pexecutive_summary_23_kpi
    title: 'Deficit Reduction Efficiency - Monthly'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.previous_monthpay, facttable.totaldeficit]
    row: 73
    col: 21
    width: 3
    height: 3
    # status=partial | KPI with goal/trend → single_value (goal/trend not fully mirrored)
    # deficiency: unbound field Date Month

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>shape_0</b> (shape → skip) — skip</li><li><b>shape_1</b> (shape → skip) — skip</li><li><b>textbox_4</b> (textbox → text) — partial</li><li><b>Monthly Net Revenue</b> (kpi → single_value) — partial</li><li><b>Monthly Insurance Revenue</b> (kpi → single_value) — partial</li><li><b>Monthly Patient Revenue</b> (kpi → single_value) — partial</li><li><b>Monthly Procedure Volume</b> (kpi → single_value) — partial</li><li><b>actionButton_16</b> (actionButton → button/gap) — gap</li><li><b>image_17</b> (image → manual) — gap</li><li><b>Yearly Avg. Patient Payment Trend</b> (kpi → single_value) — partial</li><li><b>Monthly Payment Performance</b> (kpi → single_value) — partial</li><li><b>Optimized Quarterly Expenditure</b> (kpi → single_value) — partial</li><li><b>Deficit Reduction Efficiency - Monthly</b> (kpi → single_value) — partial</li></ul>'
    row: 77
    col: 0
    width: 24
    height: 4

