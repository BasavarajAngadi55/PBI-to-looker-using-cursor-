- dashboard: project_overview
  title: Project Overview
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  elements:
  - name: migration_notes
    title: 'Migration notes — Project Overview'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Project Overview</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pproject_overview_0_textbox
    title: 'textbox_0'
    type: text
    model: dashboards
    explore: facttable
    body_text: 'textbox_0'
    row: 2
    col: 0
    width: 24
    height: 16
    # status=partial | Text box → text tile (rich formatting limited)

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>textbox_0</b> (textbox → text) — partial</li></ul>'
    row: 19
    col: 0
    width: 24
    height: 4

