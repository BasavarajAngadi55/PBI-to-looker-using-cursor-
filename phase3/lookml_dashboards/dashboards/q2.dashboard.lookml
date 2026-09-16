- dashboard: q2
  title: Q2
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q2'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q2</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: p_q2_84_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 4
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: p_q2_85_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 5
    col: 2
    width: 11
    height: 9
    # status=partial | Text box → text tile (rich formatting limited)

  - name: p_q2_86_piechart
    title: 'Active/Inactive Customer -'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.active]
    measures: [customer.active]
    row: 14
    col: 14
    width: 7
    height: 4
    # status=mapped | Pie → looker_pie
    # deficiency: PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type -sum

  - name: p_q2_87_tableex
    title: 'Active/Inactive(1/0) Customer Details -'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.first_name, customer.customer_id, customer.last_name]
    measures: [customer.active]
    row: 18
    col: 14
    width: 7
    height: 9
    # status=mapped | Table → looker_grid
    # deficiency: PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 28
    col: 0
    width: 24
    height: 4

