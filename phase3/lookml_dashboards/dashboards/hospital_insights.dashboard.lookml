- dashboard: hospital_insights
  title: Hospital Insights
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_hospital
    title: 'Hospital'
    type: field_filter
    model: dashboards
    explore: facttable
    field: hospital_lookup.hospitalname
    default_value: ''

  - name: f_region
    title: 'Region'
    type: field_filter
    model: dashboards
    explore: facttable
    field: patient_lookup.region
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Hospital Insights'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Hospital Insights</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: phospital_insights_26_card
    title: 'CptGrouping'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [cptcode_lookup.cptgrouping]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 4
    col: 17
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on CptCode_Lookup.CptGrouping mapped to field ref; confirm a measure exists on cptcode_lookup (Phase 2) 

  - name: phospital_insights_27_card
    title: 'Patient_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.patient_payment]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 7
    col: 12
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add

  - name: phospital_insights_28_card
    title: 'Insurance_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.insurance_payment]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 10
    col: 8
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: phospital_insights_29_textbox
    title: 'textbox_5'
    type: text
    model: dashboards
    explore: facttable
    body_text: 'textbox_5'
    row: 13
    col: 5
    width: 19
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: phospital_insights_30_linechart
    title: 'Monthly ARGE Ratio Trend'
    type: looker_line
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.arge_ratio]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 16
    col: 2
    width: 9
    height: 3

  - name: phospital_insights_31_card
    title: 'AR'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.ar]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 19
    col: 2
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.AR mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -sum

  - name: phospital_insights_32_card
    title: 'HospitalName'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [hospital_lookup.hospitalname]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 22
    col: 7
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Hospital_Lookup.HospitalName mapped to field ref; confirm a measure exists on hospital_lookup (Phase 

  - name: phospital_insights_33_card
    title: 'CPTUnits'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.cptunits]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 25
    col: 12
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -

  - name: phospital_insights_34_linechart
    title: 'Monthly IPTP Ratio Trend'
    type: looker_line
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.iptp_ratio]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 28
    col: 2
    width: 9
    height: 3

  - name: phospital_insights_35_piechart
    title: 'Gross Expenses by CptGrouping'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [cptcode_lookup.cptgrouping]
    measures: [facttable.gross_expenses]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 31
    col: 12
    width: 9
    height: 5
    # status=mapped | Pie → looker_pie
    # deficiency: PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add 

  - name: phospital_insights_36_treemap
    title: 'CPT Units Distribution by Hospital'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [hospital_lookup.hospitalname]
    measures: [facttable.cptunits]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 36
    col: 12
    width: 9
    height: 6
    # status=partial | Treemap has no direct Looker twin → pie/column substitute
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -

  - name: phospital_insights_37_pivottable
    title: 'Critical Hospital Metrics Overview'
    type: looker_grid
    model: dashboards
    explore: facttable
    dimensions: [hospital_lookup.hospitalname]
    measures: [facttable.ar, facttable.iptp_ratio, facttable.arge_ratio, facttable.baddebts]
    listen:
      f_hospital: hospital_lookup.hospitalname
      f_region: patient_lookup.region
    row: 42
    col: 2
    width: 9
    height: 6
    # status=mapped | Matrix/pivot → looker_grid
    # deficiency: PBI aggregation on FactTable.AR mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -sum

  - name: phospital_insights_40_textbox
    title: 'textbox_16'
    type: text
    model: dashboards
    explore: facttable
    body_text: 'textbox_16'
    row: 48
    col: 21
    width: 2
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>shape_0</b> (shape → skip) — skip</li><li><b>shape_1</b> (shape → skip) — skip</li><li><b>textbox_5</b> (textbox → text) — partial</li><li><b>CPT Units Distribution by Hospital</b> (treemap → looker_pie (substitute)) — partial</li><li><b>textbox_16</b> (textbox → text) — partial</li><li><b>image_17</b> (image → manual) — gap</li></ul>'
    row: 52
    col: 0
    width: 24
    height: 4

