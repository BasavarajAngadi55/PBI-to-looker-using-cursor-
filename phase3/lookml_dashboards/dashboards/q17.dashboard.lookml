- dashboard: q17
  title: Q17
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q17'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q17</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq17_131_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 3
    col: 1
    width: 9
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq17_132_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 12
    col: 1
    width: 22
    height: 6
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq17_133_columnchart
    title: 'Location wise Customer Ratings'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [city.city]
    measures: [film.rental_rate]
    row: 18
    col: 10
    width: 13
    height: 9
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 28
    col: 0
    width: 24
    height: 4

