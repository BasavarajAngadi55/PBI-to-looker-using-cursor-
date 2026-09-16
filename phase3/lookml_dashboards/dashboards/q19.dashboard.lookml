- dashboard: q19
  title: Q19
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q19'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q19</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq19_137_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 0
    width: 23
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq19_138_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 5
    col: 0
    width: 12
    height: 13
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq19_139_linestackedcolumncombochart
    title: 'Revenue & Inventory Distribution by Category'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.revenue, rentat.inventory_id]
    row: 18
    col: 13
    width: 10
    height: 9
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)
    # deficiency: PBI aggregation on rentat.inventory_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -su

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Revenue & Inventory Distribution by Category</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li></ul>'
    row: 28
    col: 0
    width: 24
    height: 4

