- dashboard: q11
  title: Q11
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q11'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q11</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq11_113_map
    title: 'Rental Revenue by Country'
    type: looker_map
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [payment.amount]
    row: 2
    col: 11
    width: 13
    height: 9
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum
    # deficiency: map may lack location dimension — verify geo fields

  - name: pq11_114_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 11
    col: 0
    width: 10
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq11_115_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 14
    col: 1
    width: 22
    height: 5
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>Rental Revenue by Country</b> (map → looker_map) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 20
    col: 0
    width: 24
    height: 4

