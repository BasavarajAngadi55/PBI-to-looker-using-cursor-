- dashboard: q8
  title: Q8
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q8'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q8</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq8_104_map
    title: 'Store Performance Variation by Location'
    type: looker_map
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [payment.amount]
    row: 5
    col: 8
    width: 16
    height: 12
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum
    # deficiency: map may lack location dimension — verify geo fields

  - name: pq8_105_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 17
    col: 8
    width: 16
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq8_106_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 20
    col: 1
    width: 7
    height: 14
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>Store Performance Variation by Location</b> (map → looker_map) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 35
    col: 0
    width: 24
    height: 4

