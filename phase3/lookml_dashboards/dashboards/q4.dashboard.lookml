- dashboard: q4
  title: Q4
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q4'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q4</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq4_91_columnchart
    title: 'Distribution of Films by Rental-Duration.'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rental_duration]
    measures: [film.film_id]
    row: 3
    col: 10
    width: 14
    height: 9
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pq4_92_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 12
    col: 1
    width: 9
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq4_93_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 15
    col: 0
    width: 23
    height: 4
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 20
    col: 0
    width: 24
    height: 4

