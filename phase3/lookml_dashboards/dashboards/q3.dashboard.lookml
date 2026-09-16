- dashboard: q3
  title: Q3
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q3'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q3</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq3_88_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 12
    width: 12
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq3_89_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 5
    col: 0
    width: 11
    height: 14
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq3_90_clusteredbarchart
    title: 'name'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.amount]
    row: 19
    col: 12
    width: 12
    height: 13
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 33
    col: 0
    width: 24
    height: 4

