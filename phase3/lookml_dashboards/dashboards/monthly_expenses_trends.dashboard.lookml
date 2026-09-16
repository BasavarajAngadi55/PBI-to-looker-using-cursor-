- dashboard: monthly_expenses_trends
  title: Monthly Expenses Trends
  layout: newspaper
  preferred_viewer: dashboards-next
  description: 'Deterministic Phase 3 migration from Power BI (best-effort; see coverage report)'

  filters:
  - name: f_adjustment_factor_pct
    title: 'Adjustment factor (%)'
    type: field_filter
    model: dashboards
    explore: facttable
    field: adjustment_factor_pct.adjustment_factor_pct
    default_value: ''

  elements:
  - name: migration_notes
    title: 'Migration notes — Monthly Expenses Trends'
    type: text
    body_text_as_html: true
    body_text: 'Migrated from Power BI page <b>Monthly Expenses Trends</b>. Tiles below are best-effort LookML. Gaps/partials are listed in PHASE3 coverage. Model: <code>dashboards</code> / Explore: <code>facttable</code>.'
    row: 0
    col: 0
    width: 24
    height: 2

  - name: pmonthly_expenses_trends_81_stackedareachart
    title: 'Monthly Aggregate Expenses - Gross and Adjusted'
    type: looker_area
    model: dashboards
    explore: facttable
    dimensions: [dimdate.start_of_month]
    measures: [facttable.gross_expenses, adjustment_factor_pct.adjustedgrossexpense]
    listen:
      f_adjustment_factor_pct: adjustment_factor_pct.adjustment_factor_pct
    row: 2
    col: 2
    width: 18
    height: 9
    # status=partial | Stacked area → looker_area (stacking may differ)
    # deficiency: PBI aggregation on FactTable.Gross Expenses mapped to field ref; confirm a measure exists on facttable (Phase 2) or add 

  - name: remaining_gaps
    title: 'Gaps / partials (not fully migrated)'
    type: text
    body_text_as_html: true
    body_text: '<ul><li><b>Monthly Aggregate Expenses - Gross and Adjusted</b> (stackedAreaChart → looker_area) — partial</li></ul>'
    row: 12
    col: 0
    width: 24
    height: 4

