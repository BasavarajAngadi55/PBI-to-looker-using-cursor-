- dashboard: q5
  title: Q5
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q5'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q5</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq5_94_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 3
    col: 2
    width: 10
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq5_95_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 11
    col: 1
    width: 23
    height: 6
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq5_96_donutchart
    title: 'Inventory Variation by Film-Ratings'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [inventory.inventory_id]
    row: 17
    col: 12
    width: 11
    height: 8
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add ty

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Inventory Variation by Film-Ratings</b> (donutChart → looker_pie) — partial</li></ul>'
    row: 26
    col: 0
    width: 24
    height: 4

