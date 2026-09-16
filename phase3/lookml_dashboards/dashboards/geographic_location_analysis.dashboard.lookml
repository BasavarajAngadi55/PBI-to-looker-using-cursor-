- dashboard: geographic_location_analysis
  title: Geographic / Location Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_city
    title: 'city'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: city.city
    default_value: ''

  - name: f_country
    title: 'country'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: country.country
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Geographic / Location Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Geographic / Location Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pgeographic_location_analysis_8_map
    title: 'country'
    type: looker_map
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [payment.revenue]
    listen:
      f_city: city.city
      f_country: country.country
    row: 11
    col: 0
    width: 9
    height: 7
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: map may lack location dimension — verify geo fields

  - name: pgeographic_location_analysis_9_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 18
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pgeographic_location_analysis_10_columnchart
    title: 'Location wise Customer Ratings'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [city.city]
    measures: [film.rental_rate]
    listen:
      f_city: city.city
      f_country: country.country
    row: 21
    col: 15
    width: 9
    height: 7
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pgeographic_location_analysis_11_clusteredbarchart
    title: 'Distribution of Customers across Countries'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [customer.customer_id]
    listen:
      f_city: city.city
      f_country: country.country
    row: 28
    col: 9
    width: 5
    height: 7
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type 

  - name: pgeographic_location_analysis_12_card
    title: 'Revenue'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    listen:
      f_city: city.city
      f_country: country.country
    row: 35
    col: 0
    width: 3
    height: 3

  - name: pgeographic_location_analysis_13_card
    title: 'rental_rate'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_rate]
    listen:
      f_city: city.city
      f_country: country.country
    row: 38
    col: 4
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pgeographic_location_analysis_14_card
    title: 'rental_duration'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_duration]
    listen:
      f_city: city.city
      f_country: country.country
    row: 41
    col: 0
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pgeographic_location_analysis_17_card
    title: 'Rental Frequency'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.payment_id]
    listen:
      f_city: city.city
      f_country: country.country
    row: 44
    col: 4
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -su

  - name: pgeographic_location_analysis_18_tableex
    title: 'Rental Rate & Rental Duration By Country'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [film.rental_rate, film.rental_duration]
    listen:
      f_city: city.city
      f_country: country.country
    row: 47
    col: 7
    width: 7
    height: 7
    # status=mapped | Table → looker_grid
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pgeographic_location_analysis_19_clusteredbarchart
    title: 'Rental Revenue by Country'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [payment.amount]
    listen:
      f_city: city.city
      f_country: country.country
    row: 54
    col: 15
    width: 9
    height: 7
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>country</b> (map → looker_map) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 62
    col: 0
    width: 24
    height: 4

