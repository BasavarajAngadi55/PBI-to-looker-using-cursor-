- dashboard: revenue_analysis
  title: Revenue Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Revenue Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Revenue Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: prevenue_analysis_20_clusteredbarchart
    title: 'Rental Revenue by Country'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [payment.amount]
    row: 4
    col: 0
    width: 7
    height: 9
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum

  - name: prevenue_analysis_21_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 13
    col: 0
    width: 15
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: prevenue_analysis_22_linechart
    title: 'Revenue by Month'
    type: looker_line
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    row: 16
    col: 16
    width: 8
    height: 7
    # status=mapped | Line chart → looker_line
    # deficiency: unbound field payment_date Year
    # deficiency: unbound field payment_date Month

  - name: prevenue_analysis_23_treemap
    title: 'name'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.revenue]
    row: 23
    col: 8
    width: 8
    height: 7
    # status=partial | Treemap has no direct Looker twin → pie/column substitute

  - name: prevenue_analysis_24_linestackedcolumncombochart
    title: 'Revenue & Inventory Distribution by Category'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.revenue, rentat.inventory_id]
    row: 30
    col: 14
    width: 10
    height: 5
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)
    # deficiency: PBI aggregation on rentat.inventory_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -su

  - name: prevenue_analysis_25_card
    title: 'Revenue'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    row: 35
    col: 10
    width: 3
    height: 3

  - name: prevenue_analysis_26_donutchart
    title: 'Revenue by Rating'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [payment.revenue]
    row: 38
    col: 8
    width: 6
    height: 5
    # status=partial | Donut → looker_pie (donut style limited)

  - name: prevenue_analysis_27_linestackedcolumncombochart
    title: 'Revenue'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rental_duration]
    measures: [payment.revenue]
    row: 43
    col: 0
    width: 7
    height: 5
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)

  - name: prevenue_analysis_28_card
    title: 'Rental Frequency'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.payment_id]
    row: 48
    col: 17
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -su

  - name: prevenue_analysis_29_card
    title: 'rental_rate'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_rate]
    row: 51
    col: 14
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prevenue_analysis_30_card
    title: 'rental_duration'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_duration]
    row: 54
    col: 16
    width: 8
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prevenue_analysis_31_card
    title: 'rental_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [rentat.rental_id]
    row: 57
    col: 20
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>name</b> (treemap → looker_pie (substitute)) — partial</li><li><b>Revenue & Inventory Distribution by Category</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li><li><b>Revenue by Rating</b> (donutChart → looker_pie) — partial</li><li><b>Revenue</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li><li><b>slicer_12</b> (slicer → dashboard filter) — gap</li></ul>'
    row: 61
    col: 0
    width: 24
    height: 4

