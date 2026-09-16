- dashboard: payer_provider_analysis
  title: Payer-Provider Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_gender
    title: 'Gender'
    type: field_filter
    model: dashboards
    explore: facttable
    field: patient_lookup.patientgender
    default_value: ''

  - name: f_blood_group
    title: 'Blood Group'
    type: field_filter
    model: dashboards
    explore: facttable
    field: patient_lookup.bloodgroup
    default_value: ''

  - name: f_region_code
    title: 'Region Code'
    type: field_filter
    model: dashboards
    explore: facttable
    field: patient_lookup.regioncode
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Payer-Provider Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Payer-Provider Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: ppayer_provider_analysis_66_card
    title: 'City'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [patient_lookup.city]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 4
    col: 16
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Patient_Lookup.City mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add 

  - name: ppayer_provider_analysis_67_card
    title: 'Patient_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.patient_payment]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 7
    col: 12
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add

  - name: ppayer_provider_analysis_68_card
    title: 'Insurance_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.insurance_payment]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 10
    col: 8
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: ppayer_provider_analysis_69_textbox
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

  - name: ppayer_provider_analysis_70_card
    title: 'ProviderName'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [physcian_lookup.providername]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 16
    col: 2
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 

  - name: ppayer_provider_analysis_71_card
    title: 'ProviderFTE'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [physcian_lookup.providerfte]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 19
    col: 7
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderFTE mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2

  - name: ppayer_provider_analysis_72_card
    title: 'ProviderSpecialty'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [speciality_lookup.providerspecialty]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 22
    col: 11
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Speciality_Lookup.ProviderSpecialty mapped to field ref; confirm a measure exists on speciality_looku

  - name: ppayer_provider_analysis_75_columnchart
    title: 'Regional Breakdown of Provider Specialties'
    type: looker_column
    model: dashboards
    explore: facttable
    dimensions: [speciality_lookup.specialitytype, facttable.regioncode]
    measures: [physcian_lookup.providername]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 25
    col: 2
    width: 8
    height: 6
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 

  - name: ppayer_provider_analysis_76_columnchart
    title: 'Regional Physician Count Analysis'
    type: looker_column
    model: dashboards
    explore: facttable
    dimensions: [facttable.regioncode]
    measures: [physcian_lookup.dimphysicianpk]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 31
    col: 2
    width: 8
    height: 5
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on Physcian_Lookup.dimPhysicianPK mapped to field ref; confirm a measure exists on physcian_lookup (Phas

  - name: ppayer_provider_analysis_77_linestackedcolumncombochart
    title: 'Monthly Provider Activity Overview and CPT Units'
    type: looker_column
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.cptunits, physcian_lookup.providername]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 36
    col: 11
    width: 10
    height: 5
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 

  - name: ppayer_provider_analysis_78_pivottable
    title: 'Holistic Provider Performance Matrix'
    type: looker_grid
    model: dashboards
    explore: facttable
    dimensions: [speciality_lookup.specialitytype, speciality_lookup.providerspecialty]
    measures: [physcian_lookup.providername, facttable.cptunits, physcian_lookup.providerfte]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
    row: 41
    col: 11
    width: 10
    height: 6
    # status=mapped | Matrix/pivot → looker_grid
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderName mapped to field ref; confirm a measure exists on physcian_lookup (Phase 
    # deficiency: PBI aggregation on FactTable.CPTUnits mapped to field ref; confirm a measure exists on facttable (Phase 2) or add type -
    # deficiency: PBI aggregation on Physcian_Lookup.ProviderFTE mapped to field ref; confirm a measure exists on physcian_lookup (Phase 2

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>shape_0</b> (shape → skip) — skip</li><li><b>shape_1</b> (shape → skip) — skip</li><li><b>textbox_5</b> (textbox → text) — partial</li><li><b>Monthly Provider Activity Overview and CPT Units</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li><li><b>image_15</b> (image → manual) — gap</li></ul>'
    row: 48
    col: 0
    width: 24
    height: 4

