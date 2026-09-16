- dashboard: patient_analysis
  title: Patient Analysis
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

  - name: f_region
    title: 'Region'
    type: field_filter
    model: dashboards
    explore: facttable
    field: patient_lookup.region
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Patient Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Patient Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: ppatient_analysis_44_card
    title: 'City'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [patient_lookup.city]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 4
    col: 16
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Patient_Lookup.City mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add 

  - name: ppatient_analysis_45_card
    title: 'Patient_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.patient_payment]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 7
    col: 12
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Patient_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or add

  - name: ppatient_analysis_46_card
    title: 'Insurance_Payment'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.insurance_payment]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 10
    col: 8
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.Insurance_Payment mapped to field ref; confirm a measure exists on facttable (Phase 2) or a

  - name: ppatient_analysis_47_textbox
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

  - name: ppatient_analysis_48_card
    title: 'DistinctPatient'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 16
    col: 2
    width: 4
    height: 3

  - name: ppatient_analysis_49_card
    title: 'dimPatientFK'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [facttable.dimpatientfk]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 19
    col: 7
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on FactTable.dimPatientFK mapped to field ref; confirm a measure exists on facttable (Phase 2) or add ty

  - name: ppatient_analysis_50_card
    title: 'State'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [patient_lookup.state]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 22
    col: 11
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Patient_Lookup.State mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) or add

  - name: ppatient_analysis_53_donutchart
    title: 'Patient by Tobacco'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.tobacco]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 25
    col: 2
    width: 4
    height: 3
    # status=partial | Donut → looker_pie (donut style limited)

  - name: ppatient_analysis_54_donutchart
    title: 'Patient By Exercise'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.exercise]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 28
    col: 7
    width: 4
    height: 3
    # status=partial | Donut → looker_pie (donut style limited)

  - name: ppatient_analysis_55_donutchart
    title: 'Patient by Alcohol'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.alcohol]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 31
    col: 7
    width: 4
    height: 3
    # status=partial | Donut → looker_pie (donut style limited)

  - name: ppatient_analysis_56_donutchart
    title: 'Patient by Diet'
    type: looker_pie
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.diet]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 34
    col: 2
    width: 4
    height: 3
    # status=partial | Donut → looker_pie (donut style limited)

  - name: ppatient_analysis_57_clusteredcolumnchart
    title: 'Distinct Patients by BloodGroup'
    type: looker_column
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.bloodgroup]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 37
    col: 2
    width: 9
    height: 5

  - name: ppatient_analysis_58_pivottable
    title: 'Patient Gender Distribution by State'
    type: looker_grid
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.state, patient_lookup.patientgender]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 42
    col: 11
    width: 9
    height: 5

  - name: ppatient_analysis_60_map
    title: 'Distribution of Patient by State'
    type: looker_map
    model: dashboards
    explore: facttable
    dimensions: [patient_lookup.state]
    measures: [facttable.distinctpatient]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 47
    col: 11
    width: 9
    height: 7
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: map may lack location dimension — verify geo fields

  - name: ppatient_analysis_62_card
    title: 'PatientAge'
    type: single_value
    model: dashboards
    explore: facttable
    measures: [patient_lookup.patientage]
    listen:
      f_gender: patient_lookup.patientgender
      f_blood_group: patient_lookup.bloodgroup
      f_region_code: patient_lookup.regioncode
      f_region: patient_lookup.region
    row: 54
    col: 20
    width: 4
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on Patient_Lookup.PatientAge mapped to field ref; confirm a measure exists on patient_lookup (Phase 2) o

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>shape_0</b> (shape → skip) — skip</li><li><b>shape_1</b> (shape → skip) — skip</li><li><b>textbox_5</b> (textbox → text) — partial</li><li><b>Patient by Tobacco</b> (donutChart → looker_pie) — partial</li><li><b>Patient By Exercise</b> (donutChart → looker_pie) — partial</li><li><b>Patient by Alcohol</b> (donutChart → looker_pie) — partial</li><li><b>Patient by Diet</b> (donutChart → looker_pie) — partial</li><li><b>Distribution of Patient by State</b> (map → looker_map) — partial</li><li><b>image_19</b> (image → manual) — gap</li></ul>'
    row: 58
    col: 0
    width: 24
    height: 4

