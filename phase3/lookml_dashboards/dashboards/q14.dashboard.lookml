- dashboard: q14
  title: Q14
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q14'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q14</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq14_122_treemap
    title: 'Rental Rates of Films'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [category.name]
    measures: [film.rental_rate]
    row: 2
    col: 10
    width: 13
    height: 8
    # status=partial | Treemap has no direct Looker twin → pie/column substitute
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pq14_123_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 10
    col: 1
    width: 9
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq14_124_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 13
    col: 1
    width: 22
    height: 7
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>Rental Rates of Films</b> (treemap → looker_pie (substitute)) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 21
    col: 0
    width: 24
    height: 4

