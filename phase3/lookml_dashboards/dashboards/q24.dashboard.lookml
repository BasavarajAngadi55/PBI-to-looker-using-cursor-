- dashboard: q24
  title: Q24
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q24'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q24</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq24_152_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 3
    col: 1
    width: 11
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq24_153_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 10
    col: 1
    width: 22
    height: 8
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq24_154_donutchart
    title: 'Genre Preference of Actors'
    type: looker_pie
    model: movie_rental_analysis
    explore: film
    dimensions: [film.rating]
    measures: [film_actor.actor_id]
    row: 18
    col: 13
    width: 10
    height: 7
    # status=partial | Donut → looker_pie (donut style limited)
    # deficiency: PBI aggregation on film_actor.actor_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>Genre Preference of Actors</b> (donutChart → looker_pie) — partial</li></ul>'
    row: 26
    col: 0
    width: 24
    height: 4

