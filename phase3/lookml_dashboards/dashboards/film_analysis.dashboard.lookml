- dashboard: film_analysis
  title: Film Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_film_ratings
    title: 'Film Ratings'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: film.rating
    default_value: ''

  - name: f_title
    title: 'title'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: film.title
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Film Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Film Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pfilm_analysis_57_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 10
    width: 14
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pfilm_analysis_58_card
    title: 'Film Distribution by Language'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_rate]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 5
    col: 0
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_59_clusteredbarchart
    title: 'Film-Category breakdown in Inventory'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [inventory.inventory_id]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 12
    col: 0
    width: 9
    height: 6
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add ty

  - name: pfilm_analysis_60_donutchart
    title: 'Inventory Variation by Film-Ratings'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [inventory.inventory_id]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 18
    col: 17
    width: 7
    height: 4
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add ty

  - name: pfilm_analysis_62_donutchart
    title: 'rating'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [film.film_id]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 22
    col: 10
    width: 7
    height: 4
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_63_linestackedcolumncombochart
    title: 'Revenue and Rental Rate by Film Category'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [payment.revenue, film.rental_rate]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 26
    col: 10
    width: 14
    height: 6
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_64_tableex
    title: 'film_id'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [film.film_id, film.title, film.special_features]
    measures: [film.length]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 32
    col: 0
    width: 9
    height: 5
    # status=mapped | Table → looker_grid
    # deficiency: PBI aggregation on film.length mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_65_card
    title: 'Average of Rental Duration'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_duration]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 37
    col: 4
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_67_card
    title: 'actor_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [actor.actor_id]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 40
    col: 7
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on actor.actor_id mapped to field ref; confirm a measure exists on actor (Phase 2) or add type -sum

  - name: pfilm_analysis_68_card
    title: 'film_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.film_id]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 43
    col: 7
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pfilm_analysis_70_card
    title: 'Description'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.description]
    listen:
      f_film_ratings: film.rating
      f_title: film.title
    row: 46
    col: 4
    width: 5
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.description mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>Inventory Variation by Film-Ratings</b> (donutChart → looker_pie) — partial</li><li><b>Rentals Distribution by Films</b> (lineClusteredColumnComboChart → gap) — gap</li><li><b>rating</b> (donutChart → looker_pie) — partial</li><li><b>Revenue and Rental Rate by Film Category</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li></ul>'
    row: 50
    col: 0
    width: 24
    height: 4

