- dashboard: rental_analysis
  title: Rental Analysis
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Rental Analysis'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Rental Analysis</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: prental_analysis_45_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 9
    width: 15
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: prental_analysis_46_clusteredcolumnchart
    title: 'Films Distribution by Rental Duration (In Months)'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rental_duration]
    measures: [film.film_id]
    row: 5
    col: 17
    width: 7
    height: 7
    # status=mapped | Clustered columns → looker_column
    # deficiency: PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prental_analysis_47_clusteredbarchart
    title: 'Average of rental_duration by Film-category'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [film.rental_duration]
    row: 12
    col: 9
    width: 7
    height: 7
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prental_analysis_48_treemap
    title: 'Rental Rates of Films'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [film.rental_rate]
    row: 19
    col: 0
    width: 8
    height: 7
    # status=partial | Treemap has no direct Looker twin → pie/column substitute
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prental_analysis_49_card
    title: 'Total Rentals'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [rentat.rental_id]
    row: 26
    col: 4
    width: 2
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: prental_analysis_50_card
    title: 'rental_duration'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_duration]
    row: 29
    col: 0
    width: 5
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prental_analysis_51_card
    title: 'rental_rate'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [film.rental_rate]
    row: 32
    col: 0
    width: 3
    height: 3
    # status=mapped | KPI card → single_value tile
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: prental_analysis_52_piechart
    title: 'Rental Distribution  by Year'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    measures: [rentat.rental_id]
    row: 35
    col: 0
    width: 8
    height: 5
    # status=mapped | Pie → looker_pie
    # deficiency: unbound field rental_date Year
    # deficiency: unbound field rental_date Month
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: prental_analysis_53_pivottable
    title: 'Rentals by Customer'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [customer.first_name]
    measures: [rentat.rental_id]
    row: 40
    col: 17
    width: 6
    height: 7
    # status=mapped | Matrix/pivot → looker_grid
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: prental_analysis_54_pivottable
    title: 'Rentals by Film Title'
    type: looker_grid
    model: movie_rental_analysis
    explore: film
    dimensions: [film.title]
    measures: [rentat.rental_id]
    row: 47
    col: 9
    width: 8
    height: 7
    # status=mapped | Matrix/pivot → looker_grid
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: prental_analysis_55_card
    title: 'Revenue'
    type: single_value
    model: movie_rental_analysis
    explore: film
    measures: [payment.revenue]
    row: 54
    col: 5
    width: 3
    height: 3

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>Rental Rates of Films</b> (treemap → looker_pie (substitute)) — partial</li><li><b>slicer_11</b> (slicer → dashboard filter) — gap</li></ul>'
    row: 58
    col: 0
    width: 24
    height: 4

