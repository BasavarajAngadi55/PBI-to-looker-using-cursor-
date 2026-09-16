- dashboard: overview
  title: Overview
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Overview'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Overview</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>movie_rental_analysis</code> / Explore: <code>film</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: poverview_1_textbox
    title: 'textbox_1'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_1'
    row: 3
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_2_textbox
    title: 'textbox_2'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_2'
    row: 6
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_3_textbox
    title: 'textbox_3'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_3'
    row: 9
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_4_textbox
    title: 'textbox_4'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_4'
    row: 12
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_5_textbox
    title: 'textbox_5'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_5'
    row: 15
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_6_textbox
    title: 'textbox_6'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_6'
    row: 18
    col: 7
    width: 17
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: poverview_7_textbox
    title: 'textbox_7'
    type: text
    model: movie_rental_analysis
    explore: film
    body_text: 'textbox_7'
    row: 21
    col: 0
    width: 24
    height: 3
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>pageNavigator_0</b> (pageNavigator → gap) — gap</li><li><b>textbox_1</b> (textbox → text) — partial</li><li><b>textbox_2</b> (textbox → text) — partial</li><li><b>textbox_3</b> (textbox → text) — partial</li><li><b>textbox_4</b> (textbox → text) — partial</li><li><b>textbox_5</b> (textbox → text) — partial</li><li><b>textbox_6</b> (textbox → text) — partial</li><li><b>textbox_7</b> (textbox → text) — partial</li></ul>'
    row: 25
    col: 0
    width: 24
    height: 4

