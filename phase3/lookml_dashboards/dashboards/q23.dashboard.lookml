- dashboard: q23
  title: Q23
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q23'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q23</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq23_149_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 3
    col: 5
    width: 15
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq23_150_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 6
    col: 10
    width: 13
    height: 12
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq23_151_linestackedcolumncombochart
    title: 'Actor wise Rental Rate Variation'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.first_name]
    measures: [film.rental_rate]
    row: 18
    col: 0
    width: 9
    height: 12
    # status=partial | Combo chart → looker_column or looker_line (combo not 1:1)
    # deficiency: PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Actor wise Rental Rate Variation</b> (lineStackedColumnComboChart → looker_column (partial)) — partial</li></ul>'
    row: 31
    col: 0
    width: 24
    height: 4

