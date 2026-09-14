# MIGRATION NOTE:
# Source: Power BI Employee fact + calculated columns + 28 Employee measures (+ Count of BU/Date on dims)
# Decision: sql_table_name points at warehouse employee (calc cols materialized in warehouse_sql/09_fact_employee.sql)
# Reason: Phase 2 WAREHOUSE_REQUIRED for M; LookML implements measures per mapping
# Suggestion: Prefer warehouse columns for isNewHire/AgeGroupID/Tenure*/BadHires; LookML CASE kept as fallback comments only where needed
#
# TODO: KPI parity validation required after warehouse load.
view: employee {
  label: "Employee"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;

  dimension: empl_id {
    label: "Employee ID"
    type: number
    sql: ${TABLE}.EmplID ;;
  }

  dimension_group: snapshot {
    label: "Snapshot"
    description: "Employee[date] month-grain snapshot key."
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.date ;;
    datatype: date
  }

  dimension: gender_id {
    label: "Gender ID"
    type: string
    sql: ${TABLE}.Gender ;;
  }

  dimension: age {
    label: "Age"
    type: number
    sql: ${TABLE}.Age ;;
  }

  dimension: ethnic_group {
    label: "Ethnic Group Code"
    type: string
    sql: ${TABLE}.EthnicGroup ;;
  }

  dimension: fp {
    label: "Full/Part Time Code"
    type: string
    sql: ${TABLE}.FP ;;
  }

  dimension_group: term {
    label: "Termination"
    type: time
    timeframes: [raw, date, month, quarter, year]
    sql: ${TABLE}.TermDate ;;
    datatype: date
  }

  dimension: is_terminated {
    label: "Is Terminated"
    type: yesno
    sql: ${TABLE}.TermDate IS NOT NULL ;;
  }

  dimension: bu {
    label: "Business Unit"
    type: string
    sql: ${TABLE}.BU ;;
  }

  dimension_group: hire {
    label: "Hire"
    type: time
    timeframes: [raw, date, month, quarter, year]
    sql: ${TABLE}.HireDate ;;
    datatype: date
  }

  dimension: pay_type_id {
    label: "Pay Type ID"
    type: string
    sql: ${TABLE}.PayTypeID ;;
  }

  dimension: term_reason {
    label: "Term Reason Code"
    type: string
    sql: ${TABLE}.TermReason ;;
  }

  # --- Calculated columns (prefer warehouse physical columns) ---
  dimension: is_new_hire {
    label: "Is New Hire Flag"
    description: "Power BI isNewHire. Prefer ${TABLE}.isNewHire from warehouse."
    type: number
    sql: ${TABLE}.isNewHire ;;
  }

  dimension: age_group_id {
    label: "Age Group ID"
    type: number
    sql: ${TABLE}.AgeGroupID ;;
  }

  dimension: tenure_days {
    label: "Tenure Days"
    type: number
    sql: ${TABLE}.TenureDays ;;
  }

  dimension: tenure_months {
    label: "Tenure Months"
    type: number
    sql: ${TABLE}.TenureMonths ;;
  }

  dimension: bad_hires_flag {
    label: "Bad Hire Flag"
    type: number
    sql: ${TABLE}.BadHires ;;
  }

  # --- Measures ---
  measure: count {
    label: "Row Count"
    type: count
    hidden: yes
  }

  # TODO:
  # Source Power BI object: EmpCount
  # Dependency: Date[PeriodNumber] MAX over ALL PeriodNumber
  # Reason blocked: latest-period FILTER(ALL(...)) not equivalent to plain count_distinct
  # Suggested resolution: always_filter / liquid / SQL filter to MAX(PeriodNumber); parity test
  # Source Power BI DAX: CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
  measure: emp_count {
    group_label: "Blocked — TODO"
    label: "Emp Count"
    description: "PARTIAL/COMPLEX — not full EmpCount period logic yet."
    type: count_distinct
    sql: ${empl_id} ;;
  }

  # DAX: CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
  measure: seps {
    label: "Separations"
    type: count_distinct
    sql: ${empl_id} ;;
    filters: [is_terminated: "yes"]
  }

  # DAX: CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
  # MIGRATION NOTE: PBIX nests EmpCount; LookML uses TermDate-blank distinct count — PARTIAL until EmpCount parity
  measure: actives {
    label: "Actives"
    type: count_distinct
    sql: ${empl_id} ;;
    filters: [is_terminated: "no"]
  }

  measure: new_hires {
    label: "New Hires"
    type: sum
    sql: ${is_new_hire} ;;
  }

  measure: avg_tenure_days {
    label: "AVG Tenure Days"
    type: average
    sql: ${tenure_days} ;;
    value_format_name: decimal_1
  }

  measure: avg_tenure_months {
    label: "AVG Tenure Months"
    type: number
    sql: ROUND(${avg_tenure_days} / 30.0, 1) - 1 ;;
    value_format_name: decimal_1
  }

  measure: avg_age {
    label: "AVG Age"
    type: average
    sql: ${age} ;;
    value_format_name: decimal_0
  }

  measure: sum_of_bad_hires {
    label: "Sum of Bad Hires"
    type: sum
    sql: ${bad_hires_flag} ;;
  }

  # TODO: SAMEPERIODLASTYEAR — KPI parity validation required
  measure: new_hires_sply {
    group_label: "Blocked — TODO"
    label: "New Hires SPLY"
    # Source Power BI DAX: CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date]))
    # Reason: no 1:1 LookML SAMEPERIODLASTYEAR
    # Suggested resolution: Looker PoP / prior-year join + parity test
    type: number
    sql: NULL ;;
  }

  measure: actives_sply {
    group_label: "Blocked — TODO"
    label: "Actives SPLY"
    # Source Power BI DAX: CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: seps_sply {
    group_label: "Blocked — TODO"
    label: "Seps SPLY"
    # Source Power BI DAX: CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: emp_count_sply {
    group_label: "Blocked — TODO"
    label: "Emp Count SPLY"
    # Source Power BI DAX: EmpCount + SAMEPERIODLASTYEAR
    type: number
    sql: NULL ;;
  }

  measure: seps_yoy_var {
    label: "Seps YoY Var"
    type: number
    sql: ${seps} - ${seps_sply} ;;
  }

  measure: actives_yoy_var {
    label: "Actives YoY Var"
    type: number
    sql: ${actives} - ${actives_sply} ;;
  }

  measure: new_hires_yoy_var {
    label: "New Hires YoY Var"
    type: number
    sql: ${new_hires} - ${new_hires_sply} ;;
  }

  measure: seps_yoy_pct_change {
    label: "Seps YoY % Change"
    type: number
    sql: SAFE_DIVIDE(${seps_yoy_var}, ${seps_sply}) ;;
    value_format_name: percent_1
  }

  measure: actives_yoy_pct_change {
    label: "Actives YoY % Change"
    type: number
    sql: SAFE_DIVIDE(${actives_yoy_var}, ${actives_sply}) ;;
    value_format_name: percent_1
  }

  measure: new_hires_yoy_pct_change {
    label: "New Hires YoY % Change"
    type: number
    sql: SAFE_DIVIDE(${new_hires_yoy_var}, ${new_hires_sply}) ;;
    value_format_name: percent_1
  }

  measure: bad_hires_sply {
    group_label: "Blocked — TODO"
    label: "Bad Hires SPLY"
    # Source Power BI DAX: CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: bad_hires_yoy_var {
    label: "Bad Hires YoY Var"
    type: number
    sql: ${sum_of_bad_hires} - ${bad_hires_sply} ;;
  }

  measure: bad_hires_yoy_pct_change {
    label: "Bad Hires YoY % Change"
    type: number
    sql: SAFE_DIVIDE(${bad_hires_yoy_var}, ${bad_hires_sply}) ;;
    value_format_name: percent_1
  }

  measure: to_pct {
    label: "TO %"
    type: number
    sql: SAFE_DIVIDE(${seps}, ${actives}) ;;
    value_format_name: percent_1
  }

  # TODO: ALL(Gender), ALL(Ethnicity)
  measure: to_pct_norm {
    group_label: "Blocked — TODO"
    label: "TO % Norm"
    # Source Power BI DAX: CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
    # Suggested resolution: filtered measure / PDT ignoring Gender & Ethnicity; parity test
    type: number
    sql: NULL ;;
    value_format_name: percent_1
  }

  measure: to_pct_var {
    label: "TO % Var"
    type: number
    sql: ${to_pct} - ${to_pct_norm} ;;
    value_format_name: percent_1
  }

  measure: sep_pct_of_active {
    label: "Sep % of Active"
    type: number
    sql: SAFE_DIVIDE(${seps}, ${actives}) ;;
    value_format_name: percent_1
  }

  measure: sep_pct_of_smly_actives {
    label: "Sep % of SMLY Actives"
    type: number
    sql: SAFE_DIVIDE(${seps_sply}, ${actives_sply}) ;;
    value_format_name: percent_1
  }

  measure: bad_hire_pct_of_actives {
    label: "Bad Hire % of Actives"
    type: number
    sql: SAFE_DIVIDE(${sum_of_bad_hires}, ${actives}) ;;
    value_format_name: percent_1
  }

  measure: bad_hire_pct_of_active_sply {
    label: "Bad Hire % of Active SPLY"
    type: number
    sql: SAFE_DIVIDE(${bad_hires_sply}, ${actives_sply}) ;;
    value_format_name: percent_1
  }
}
