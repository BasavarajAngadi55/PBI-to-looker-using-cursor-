- dashboard: q25
  title: Q25
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q25'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q25</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq25_155_textbox
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

  - name: pq25_156_textbox
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

  - name: pq25_157_columnchart
    title: 'Revenue Contribution by Actors'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.first_name]
    measures: [payment.revenue]
    row: 17
    col: 10
    width: 13
    height: 8

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 26
    col: 0
    width: 24
    height: 4

