- dashboard: q13
  title: Q13
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q13'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q13</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq13_119_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 4
    col: 1
    width: 8
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq13_120_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 10
    col: 1
    width: 22
    height: 7
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq13_121_donutchart
    title: 'Distribution of Films by languages'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [language.name]
    measures: [film.film_id]
    row: 17
    col: 11
    width: 8
    height: 4
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Distribution of Films by languages</b> (donutChart → looker_pie) — partial</li></ul>'
    row: 22
    col: 0
    width: 24
    height: 4

