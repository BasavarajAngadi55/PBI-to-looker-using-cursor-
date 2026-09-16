- dashboard: q29
  title: Q29
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q29'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q29</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq29_167_textbox
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

  - name: pq29_168_textbox
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

  - name: pq29_169_treemap
    title: 'Revenue Distribution by Film Category - Identifying Top Contributors'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.revenue]
    row: 17
    col: 10
    width: 13
    height: 8
    # status=partial | Treemap has no direct Looker twin → pie/column substitute

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Revenue Distribution by Film Category - Identifying Top Contributors</b> (treemap → looker_pie (substitute)) — partial</li></ul>'
    row: 26
    col: 0
    width: 24
    height: 4

