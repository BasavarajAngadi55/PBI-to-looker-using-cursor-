# Employee fact — monthly employee snapshot from Power BI Human Resources Sample.
# Source PBIX calculated columns are expressed as LookML dimensions for warehouse portability.
view: employee {
  label: "Employee"
  sql_table_name: `hr.employee` ;;

  # ---------- Keys & attributes ----------
  dimension: empl_id {
    label: "Employee ID"
    description: "Unique employee identifier (EmplID)."
    type: number
    sql: ${TABLE}.EmplID ;;
    primary_key: no
  }

  dimension_group: snapshot {
    label: "Snapshot"
    description: "Month-grain snapshot date from Employee[date]. Joins to Date dimension."
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.date ;;
    datatype: date
  }

  dimension: gender_id {
    label: "Gender ID"
    description: "Gender code joining to Gender.ID (sample maps D=Male, C=Female)."
    type: string
    sql: ${TABLE}.Gender ;;
  }

  dimension: age {
    label: "Age"
    description: "Employee age as of the snapshot period."
    type: number
    sql: ${TABLE}.Age ;;
  }

  dimension: ethnic_group {
    label: "Ethnic Group Code"
    description: "Ethnic group code joining to Ethnicity.[Ethnic Group]."
    type: string
    sql: ${TABLE}.EthnicGroup ;;
  }

  dimension: fp {
    label: "Full/Part Time Code"
    description: "F/P code joining to FP.FP."
    type: string
    sql: ${TABLE}.FP ;;
  }

  dimension_group: term {
    label: "Termination"
    description: "Termination date; blank means currently active for the snapshot."
    type: time
    timeframes: [raw, date, month, quarter, year]
    sql: ${TABLE}.TermDate ;;
    datatype: date
  }

  dimension: is_terminated {
    label: "Is Terminated"
    description: "Yes when TermDate is populated."
    type: yesno
    sql: ${TABLE}.TermDate IS NOT NULL ;;
  }

  dimension: bu {
    label: "Business Unit"
    description: "Business unit / market code joining to BU.BU."
    type: string
    sql: ${TABLE}.BU ;;
  }

  dimension_group: hire {
    label: "Hire"
    description: "Employee seniority / hire date."
    type: time
    timeframes: [raw, date, month, quarter, year]
    sql: ${TABLE}.HireDate ;;
    datatype: date
  }

  dimension: pay_type_id {
    label: "Pay Type ID"
    description: "Pay type code joining to PayType.PayTypeID (H=Hourly, S=Salaried)."
    type: string
    sql: ${TABLE}.PayTypeID ;;
  }

  dimension: term_reason {
    label: "Term Reason Code"
    description: "Separation type code joining to SeparationReason.SeparationTypeID (V/U)."
    type: string
    sql: ${TABLE}.TermReason ;;
  }

  # ---------- Calculated columns (DAX → SQL) ----------
  # DAX: IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)
  dimension: is_new_hire {
    label: "Is New Hire Flag"
    description: "1 when snapshot year/month equals hire year/month. Prefer materializing in warehouse SQL if used heavily."
    type: number
    sql: CASE
      WHEN EXTRACT(YEAR FROM ${TABLE}.date) = EXTRACT(YEAR FROM ${TABLE}.HireDate)
        AND EXTRACT(MONTH FROM ${TABLE}.date) = EXTRACT(MONTH FROM ${TABLE}.HireDate)
      THEN 1
      ELSE NULL
    END ;;
  }

  # DAX: IF([Age]<30, 1, IF([Age]<50, 2, 3))
  dimension: age_group_id {
    label: "Age Group ID"
    description: "Derived age band: 1=<30, 2=30-49, 3=50+. Joins to AgeGroup."
    type: number
    sql: CASE
      WHEN ${TABLE}.Age < 30 THEN 1
      WHEN ${TABLE}.Age < 50 THEN 2
      ELSE 3
    END ;;
  }

  # DAX: IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])
  dimension: tenure_days {
    label: "Tenure Days"
    description: "Absolute day difference between snapshot date and hire date."
    type: number
    sql: ABS(DATE_DIFF(${TABLE}.date, ${TABLE}.HireDate, DAY)) ;;
  }

  # DAX: CEILING([TenureDays]/30, 1) - 1
  dimension: tenure_months {
    label: "Tenure Months"
    description: "Approximate tenure in months from TenureDays."
    type: number
    sql: CEILING(${tenure_days} / 30.0) - 1 ;;
  }

  # DAX: IF(OR((([HireDate]-[TermDate])*-1)>=61, ISBLANK([TermDate])), 0, 1)
  # Bad hire = terminated within 60 days of hire.
  dimension: bad_hires_flag {
    label: "Bad Hire Flag"
    description: "1 if terminated within 60 days of hire; else 0. Matches Power BI BadHires column."
    type: number
    sql: CASE
      WHEN ${TABLE}.TermDate IS NULL THEN 0
      WHEN DATE_DIFF(${TABLE}.TermDate, ${TABLE}.HireDate, DAY) >= 61 THEN 0
      ELSE 1
    END ;;
  }

  # ---------- Base measures ----------
  measure: count {
    label: "Row Count"
    type: count
    description: "Count of employee snapshot rows."
  }

  measure: emp_count {
    group_label: "Blocked — TODO"
    label: "Emp Count"
    description: "COUNT(EmplID). Power BI EmpCount also filtered to MAX PeriodNumber — see TODO."
    # TODO: DAX EmpCount = CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
    # Implement latest-period filter via explore always_filter / liquid / derived table before production use.
    type: count_distinct
    sql: ${empl_id} ;;
  }

  measure: seps {
    label: "Separations"
    description: "Employees with a termination date in the current filter context."
    # DAX: CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
    type: count_distinct
    sql: ${empl_id} ;;
    filters: [is_terminated: "yes"]
  }

  measure: actives {
    label: "Actives"
    description: "Active employees (TermDate blank) in the current filter context."
    # DAX: CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
    type: count_distinct
    sql: ${empl_id} ;;
    filters: [is_terminated: "no"]
  }

  measure: new_hires {
    label: "New Hires"
    description: "Sum of isNewHire flag."
    # DAX: SUM([isNewHire])
    type: sum
    sql: ${is_new_hire} ;;
  }

  measure: avg_tenure_days {
    label: "AVG Tenure Days"
    description: "Average tenure in days."
    # DAX: AVERAGE([TenureDays])
    type: average
    sql: ${tenure_days} ;;
    value_format_name: decimal_1
  }

  measure: avg_tenure_months {
    label: "AVG Tenure Months"
    description: "Derived from AVG Tenure Days / 30, rounded."
    # DAX: ROUND([AVG Tenure Days]/30, 1)-1
    type: number
    sql: ROUND(${avg_tenure_days} / 30.0, 1) - 1 ;;
    value_format_name: decimal_1
  }

  measure: avg_age {
    label: "AVG Age"
    description: "Rounded average employee age."
    # DAX: ROUND(AVERAGE([Age]), 0)
    type: average
    sql: ${age} ;;
    value_format_name: decimal_0
  }

  measure: sum_of_bad_hires {
    label: "Sum of Bad Hires"
    description: "Sum of BadHires flag."
    # DAX: SUM([BadHires])
    type: sum
    sql: ${bad_hires_flag} ;;
  }

  # ---------- YoY / SPLY (time intelligence) ----------
  # TODO: DAX SAMEPERIODLASTYEAR('Date'[Date]) has no 1:1 LookML equivalent.
  # Prefer: Looker period_over_period, date_offset filters, or a twin explore with prior-year join.
  measure: new_hires_sply {
    group_label: "Blocked — TODO"
    label: "New Hires SPLY"
    description: "BLOCKED: SAMEPERIODLASTYEAR. See BLOCKERS_AND_DEPENDENCIES.md."
    # TODO: CALCULATE([New Hires], SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: actives_sply {
    group_label: "Blocked — TODO"
    label: "Actives SPLY"
    description: "BLOCKED: SAMEPERIODLASTYEAR. See BLOCKERS_AND_DEPENDENCIES.md."
    # TODO: CALCULATE([Actives], SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: seps_sply {
    group_label: "Blocked — TODO"
    label: "Seps SPLY"
    description: "BLOCKED: SAMEPERIODLASTYEAR. See BLOCKERS_AND_DEPENDENCIES.md."
    # TODO: CALCULATE([Seps], SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: emp_count_sply {
    group_label: "Blocked — TODO"
    label: "Emp Count SPLY"
    description: "BLOCKED: EmpCount max PeriodNumber + SAMEPERIODLASTYEAR."
    # TODO: CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), ...), SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: seps_yoy_var {
    label: "Seps YoY Var"
    description: "Separations year-over-year variance."
    # DAX: [Seps]-[Seps SPLY]
    type: number
    sql: ${seps} - ${seps_sply} ;;
  }

  measure: actives_yoy_var {
    label: "Actives YoY Var"
    description: "Actives year-over-year variance."
    # DAX: [Actives]-[Actives SPLY]
    type: number
    sql: ${actives} - ${actives_sply} ;;
  }

  measure: new_hires_yoy_var {
    label: "New Hires YoY Var"
    description: "New hires year-over-year variance."
    # DAX: [New Hires]-[New Hires SPLY]
    type: number
    sql: ${new_hires} - ${new_hires_sply} ;;
  }

  measure: seps_yoy_pct_change {
    label: "Seps YoY % Change"
    description: "Separations YoY percent change."
    # DAX: DIVIDE([Seps YoY Var], [Seps SPLY])
    type: number
    sql: SAFE_DIVIDE(${seps_yoy_var}, ${seps_sply}) ;;
    value_format_name: percent_1
  }

  measure: actives_yoy_pct_change {
    label: "Actives YoY % Change"
    description: "Actives YoY percent change."
    # DAX: DIVIDE([Actives YoY Var], [Actives SPLY])
    type: number
    sql: SAFE_DIVIDE(${actives_yoy_var}, ${actives_sply}) ;;
    value_format_name: percent_1
  }

  measure: new_hires_yoy_pct_change {
    label: "New Hires YoY % Change"
    description: "New hires YoY percent change."
    # DAX: DIVIDE([New Hires YoY Var], [New Hires SPLY])
    type: number
    sql: SAFE_DIVIDE(${new_hires_yoy_var}, ${new_hires_sply}) ;;
    value_format_name: percent_1
  }

  measure: bad_hires_sply {
    group_label: "Blocked — TODO"
    label: "Bad Hires SPLY"
    description: "BLOCKED: SAMEPERIODLASTYEAR. See BLOCKERS_AND_DEPENDENCIES.md."
    # TODO: CALCULATE([Sum of BadHires], SAMEPERIODLASTYEAR('Date'[Date]))
    type: number
    sql: NULL ;;
  }

  measure: bad_hires_yoy_var {
    label: "Bad Hires YoY Var"
    description: "Bad hires year-over-year variance."
    # DAX: [Sum of BadHires]-[Bad Hires SPLY]
    type: number
    sql: ${sum_of_bad_hires} - ${bad_hires_sply} ;;
  }

  measure: bad_hires_yoy_pct_change {
    label: "Bad Hires YoY % Change"
    description: "Bad hires YoY percent change."
    # DAX: DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])
    type: number
    sql: SAFE_DIVIDE(${bad_hires_yoy_var}, ${bad_hires_sply}) ;;
    value_format_name: percent_1
  }

  # ---------- Ratios ----------
  measure: to_pct {
    label: "TO %"
    description: "Turnover rate = Separations / Actives."
    # DAX: DIVIDE([Seps], [Actives])
    type: number
    sql: SAFE_DIVIDE(${seps}, ${actives}) ;;
    value_format_name: percent_1
  }

  measure: to_pct_norm {
    group_label: "Blocked — TODO"
    label: "TO % Norm"
    description: "BLOCKED: ALL(Gender), ALL(Ethnicity). See BLOCKERS_AND_DEPENDENCIES.md."
    # TODO: CALCULATE([TO %], ALL(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
    # In Looker, use filtered measures that ignore those dimensions, or an unfiltered PDT.
    type: number
    sql: NULL ;;
    value_format_name: percent_1
  }

  measure: to_pct_var {
    label: "TO % Var"
    description: "Variance of turnover vs normalized turnover."
    # DAX: [TO %]-[TO % Norm]
    type: number
    sql: ${to_pct} - ${to_pct_norm} ;;
    value_format_name: percent_1
  }

  measure: sep_pct_of_active {
    label: "Sep % of Active"
    description: "Separations as a share of actives (same as TO %)."
    # DAX: DIVIDE([Seps],[Actives])
    type: number
    sql: SAFE_DIVIDE(${seps}, ${actives}) ;;
    value_format_name: percent_1
  }

  measure: sep_pct_of_smly_actives {
    label: "Sep % of SMLY Actives"
    description: "Prior-year seps / prior-year actives."
    # DAX: DIVIDE([Seps SPLY],[Actives SPLY])
    type: number
    sql: SAFE_DIVIDE(${seps_sply}, ${actives_sply}) ;;
    value_format_name: percent_1
  }

  measure: bad_hire_pct_of_actives {
    label: "Bad Hire % of Actives"
    description: "Bad hires as a share of actives."
    # DAX: DIVIDE([Sum of BadHires],[Actives])
    type: number
    sql: SAFE_DIVIDE(${sum_of_bad_hires}, ${actives}) ;;
    value_format_name: percent_1
  }

  measure: bad_hire_pct_of_active_sply {
    label: "Bad Hire % of Active SPLY"
    description: "Prior-year bad hires / prior-year actives."
    # DAX: DIVIDE([Bad Hires SPLY],[Actives SPLY])
    type: number
    sql: SAFE_DIVIDE(${bad_hires_sply}, ${actives_sply}) ;;
    value_format_name: percent_1
  }
}
