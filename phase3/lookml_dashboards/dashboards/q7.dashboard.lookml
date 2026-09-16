- dashboard: q7
  title: Q7
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q7'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q7</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq7_100_columnchart
    title: 'Staff Distribution by Employment Duration'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.employment_duration, staff.staff_id]
    measures: [staff.staff_id]
    row: 6
    col: 12
    width: 11
    height: 7
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on staff.staff_id mapped to field ref; confirm a measure exists on staff (Phase 2) or add type -sum

  - name: pq7_101_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 13
    col: 3
    width: 6
    height: 6
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq7_102_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 19
    col: 11
    width: 12
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq7_103_textbox
    title: 'textbox_3'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_3'
    row: 22
    col: 0
    width: 11
    height: 9
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li><li><b>textbox_3</b> (textbox → text) — partial</li></ul>'
    row: 32
    col: 0
    width: 24
    height: 4

