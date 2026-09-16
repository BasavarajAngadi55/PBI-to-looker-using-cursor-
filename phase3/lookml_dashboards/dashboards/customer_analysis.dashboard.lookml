- dashboard: customer_analysis
  title: Customer Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_category_id
    title: 'category_id'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: film_category.category_id
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Customer Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Customer Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pcustomer_analysis_33_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 11
    width: 13
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pcustomer_analysis_34_donutchart
    title: 'Active/Inactive Customer -'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.active]
    measures: [customer.active]
    listen:
      f_category_id: film_category.category_id
    row: 7
    col: 7
    width: 3
    height: 3
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type -sum

  - name: pcustomer_analysis_35_tableex
    title: 'Active/Inactive(1/0) Customer Details -'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.first_name, customer.customer_id, customer.last_name]
    measures: [customer.active]
    listen:
      f_category_id: film_category.category_id
    row: 10
    col: 11
    width: 7
    height: 7
    # status=mapped | Table → looker_grid
    # deficiency: PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type -sum

  - name: pcustomer_analysis_36_clusteredbarchart
    title: 'name'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.amount]
    listen:
      f_category_id: film_category.category_id
    row: 17
    col: 17
    width: 6
    height: 7
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum

  - name: pcustomer_analysis_37_map
    title: 'Customers by Country'
    type: looker_map
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [customer.customer_id]
    listen:
      f_category_id: film_category.category_id
    row: 24
    col: 0
    width: 10
    height: 7
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type 
    # deficiency: map may lack location dimension — verify geo fields

  - name: pcustomer_analysis_38_card
    title: 'customer_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [customer.customer_id]
    listen:
      f_category_id: film_category.category_id
    row: 31
    col: 0
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type 

  - name: pcustomer_analysis_39_columnchart
    title: 'Rental Rate by Customers'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.first_name]
    measures: [film.rental_rate]
    listen:
      f_category_id: film_category.category_id
    row: 34
    col: 11
    width: 13
    height: 7
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pcustomer_analysis_40_columnchart
    title: 'Distribution of Customers by Rating'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [payment.customer_id]
    listen:
      f_category_id: film_category.category_id
    row: 41
    col: 0
    width: 6
    height: 6
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on payment.customer_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -s

  - name: pcustomer_analysis_41_card
    title: 'Revenue'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    listen:
      f_category_id: film_category.category_id
    row: 47
    col: 4
    width: 3
    height: 3

  - name: pcustomer_analysis_42_card
    title: 'Rental Frequency'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.payment_id]
    listen:
      f_category_id: film_category.category_id
    row: 50
    col: 0
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -su

  - name: pcustomer_analysis_43_card
    title: 'rental_rate'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_rate]
    listen:
      f_category_id: film_category.category_id
    row: 53
    col: 4
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>Active/Inactive Customer -</b> (donutChart → looker_pie) — partial</li><li><b>Customers by Country</b> (map → looker_map) — partial</li></ul>'
    row: 57
    col: 0
    width: 24
    height: 4

