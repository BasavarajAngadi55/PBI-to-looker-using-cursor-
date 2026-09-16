- dashboard: q12
  title: Q12
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q12'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q12</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq12_116_columnchart
    title: 'Location wise Customer Ratings'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [city.city]
    measures: [film.rental_rate]
    row: 5
    col: 0
    width: 8
    height: 12
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pq12_117_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 17
    col: 0
    width: 22
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq12_118_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 20
    col: 9
    width: 14
    height: 9
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 30
    col: 0
    width: 24
    height: 4

