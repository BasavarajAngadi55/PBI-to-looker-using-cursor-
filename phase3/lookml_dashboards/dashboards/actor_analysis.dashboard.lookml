- dashboard: actor_analysis
  title: Actor Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_first_name
    title: 'first_name'
    type: field_filter
    model: movie_rental_analysis
    explore: film
    field: actor.first_name
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Actor Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Actor Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pactor_analysis_71_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 0
    width: 10
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pactor_analysis_72_barchart
    title: 'DIstribution of Films by Actors'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.first_name]
    measures: [film_actor.film_id]
    listen:
      f_first_name: actor.first_name
    row: 5
    col: 15
    width: 9
    height: 7
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on film_actor.film_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type 

  - name: pactor_analysis_73_linestackedcolumncombochart
    title: 'Revenue Contribution by Actors'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.first_name]
    measures: [payment.revenue]
    listen:
      f_first_name: actor.first_name
    row: 12
    col: 13
    width: 10
    height: 7
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)

  - name: pactor_analysis_74_linechart
    title: 'Actor wise Rental Rate Variation'
    type: looker_line
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.actor_id]
    measures: [film.rental_rate]
    listen:
      f_first_name: actor.first_name
    row: 19
    col: 0
    width: 13
    height: 7
    # status=mapped | Line chart → looker_line
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pactor_analysis_75_tableex
    title: 'Actor Details'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.actor_id, actor.first_name, actor.last_name]
    measures: [actor.filmpopularity]
    listen:
      f_first_name: actor.first_name
    row: 26
    col: 0
    width: 7
    height: 7

  - name: pactor_analysis_76_card
    title: 'film_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film_category.film_id]
    listen:
      f_first_name: actor.first_name
    row: 33
    col: 10
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film_category.film_id mapped to field ref; confirm a measure exists on film_category (Phase 2) or add

  - name: pactor_analysis_77_card
    title: 'actor_id'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [actor.actor_id]
    listen:
      f_first_name: actor.first_name
    row: 36
    col: 14
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on actor.actor_id mapped to field ref; confirm a measure exists on actor (Phase 2) or add type -sum

  - name: pactor_analysis_79_card
    title: 'Revenue'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    listen:
      f_first_name: actor.first_name
    row: 39
    col: 17
    width: 3
    height: 3

  - name: pactor_analysis_80_donutchart
    title: 'Genre Preferences of Actors'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [film_actor.actor_id]
    listen:
      f_first_name: actor.first_name
    row: 42
    col: 7
    width: 7
    height: 7
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on film_actor.actor_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>Revenue Contribution by Actors</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li><li><b>Genre Preferences of Actors</b> (donutChart → looker_pie) — partial</li></ul>'
    row: 50
    col: 0
    width: 24
    height: 4

