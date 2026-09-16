- dashboard: q16
  title: Q16
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q16'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q16</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq16_128_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 2
    width: 6
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq16_129_linechart
    title: 'Rental Rate & Rental Duration By Country'
    type: looker_line
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [film.rental_rate, film.rental_duration]
    row: 5
    col: 8
    width: 15
    height: 7
    # status=mapped | Line chart → looker_line
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pq16_130_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 12
    col: 2
    width: 21
    height: 7
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 20
    col: 0
    width: 24
    height: 4

