- dashboard: q9
  title: Q9
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q9'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q9</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq9_107_piechart
    title: 'Average of rental_duration by staff member'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [staff.staff_id]
    measures: [film.rental_duration]
    row: 5
    col: 1
    width: 12
    height: 7
    # status=mapped | Pie → looker_pie
    # deficiency: PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type -sum

  - name: pq9_108_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 12
    col: 1
    width: 13
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq9_109_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 15
    col: 13
    width: 10
    height: 9
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li></ul>'
    row: 25
    col: 0
    width: 24
    height: 4

