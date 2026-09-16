- dashboard: q6
  title: Q6
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q6'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q6</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq6_97_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 1
    width: 9
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq6_98_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 6
    col: 1
    width: 9
    height: 12
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq6_99_clusteredbarchart
    title: 'Film-Category breakdown in Inventory'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [inventory.inventory_id]
    row: 18
    col: 11
    width: 13
    height: 15
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add ty

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 34
    col: 0
    width: 24
    height: 4

