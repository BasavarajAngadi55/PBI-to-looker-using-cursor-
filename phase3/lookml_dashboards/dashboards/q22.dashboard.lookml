- dashboard: q22
  title: Q22
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q22'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q22</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq22_146_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 1
    width: 9
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq22_147_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 5
    col: 1
    width: 9
    height: 12
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq22_148_barchart
    title: 'DIstribution of Films by Actors'
    type: looker_bar
    model: movie_rental_analysis
    explore: film
    dimensions: [actor.first_name]
    measures: [film_actor.film_id]
    row: 17
    col: 11
    width: 12
    height: 15
    # status=mapped | Bar chart → looker_bar
    # deficiency: PBI aggregation on film_actor.film_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type 

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li></ul>'
    row: 33
    col: 0
    width: 24
    height: 4

