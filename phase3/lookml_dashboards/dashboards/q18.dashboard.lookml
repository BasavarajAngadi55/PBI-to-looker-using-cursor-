- dashboard: q18
  title: Q18
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q18'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q18</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq18_134_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 0
    width: 11
    height: 4
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq18_135_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 8
    col: 0
    width: 23
    height: 9
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq18_136_donutchart
    title: 'Revenue by Rating'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [payment.revenue]
    row: 17
    col: 13
    width: 11
    height: 6
    # status=partial | Donut → looker_pie (donut style limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Revenue by Rating</b> (donutChart → looker_pie) — partial</li></ul>'
    row: 24
    col: 0
    width: 24
    height: 4

