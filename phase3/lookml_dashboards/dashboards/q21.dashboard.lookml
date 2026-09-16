- dashboard: q21
  title: Q21
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q21'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q21</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq21_143_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 3
    col: 1
    width: 8
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq21_144_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 11
    col: 1
    width: 23
    height: 7
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq21_145_columnchart
    title: 'rental_id'
    type: looker_column
    model: movie_rental_analysis
    explore: film
    dimensions: [film.title]
    measures: [rentat.rental_id]
    row: 18
    col: 10
    width: 14
    height: 7
    # status=mapped | Column chart → looker_column
    # deficiency: PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type -sum

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 26
    col: 0
    width: 24
    height: 4

