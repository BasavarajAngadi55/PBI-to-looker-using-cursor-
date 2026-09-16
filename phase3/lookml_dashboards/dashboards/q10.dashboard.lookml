- dashboard: q10
  title: Q10
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q10'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q10</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq10_110_columnchart
    title: 'Distribution of Customers across Cities'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [city.city]
    measures: [customer.customer_id]
    row: 3
    col: 11
    width: 12
    height: 7
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type 

  - name: pq10_111_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 10
    col: 1
    width: 10
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq10_112_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 13
    col: 1
    width: 23
    height: 5
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 19
    col: 0
    width: 24
    height: 4

