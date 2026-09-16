- dashboard: q26
  title: Q26
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Q26'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Q26</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pq26_158_textbox
    title: 'textbox_0'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_0'
    row: 2
    col: 1
    width: 8
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq26_159_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 12
    col: 1
    width: 23
    height: 4
    # status=partial | Text box → text tile (rich formatting limited)

  - name: pq26_160_map
    title: 'customer distribution by countries'
    type: looker_map
    model: movie_rental_analysis
    explore: film
    dimensions: [country.country]
    measures: [customer.customer_id]
    row: 16
    col: 10
    width: 14
    height: 10
    # status=partial | Map → looker_map if geo fields exist; else gap
    # deficiency: PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type 
    # deficiency: map may lack location dimension — verify geo fields

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>customer distribution by countries</b> (map → looker_map) — partial</li></ul>'
    row: 27
    col: 0
    width: 24
    height: 4

