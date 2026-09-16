- dashboard: q1
  title: Q1
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q1'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q1</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq1_81_linechart
    title: 'Revenue by Month'
    type: looker_line
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    row: 4
    col: 10
    width: 13
    height: 9
    # status=mapped | Line chart → looker_line
    # deficiency: unbound field payment_date Year
    # deficiency: unbound field payment_date Month

  - name: pq1_82_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 13
    col: 10
    width: 13
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq1_83_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 16
    col: 1
    width: 9
    height: 14
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 31
    col: 0
    width: 24
    height: 4

