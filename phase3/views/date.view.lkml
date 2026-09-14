# MIGRATION NOTE:
# Source: Power BI Date + MonthIncrementNumber (warehouse preferred)
# Hierarchy YQM approximated via drill_fields
view: date {
  label: "Date"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;

  dimension_group: calendar {
    label: "Calendar"
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.Date ;;
    datatype: date
    primary_key: yes
  }

  dimension: month {
    label: "Month Name"
    type: string
    sql: ${TABLE}.Month ;;
  }

  dimension: month_number {
    label: "Month Number"
    type: number
    sql: ${TABLE}.MonthNumber ;;
  }

  dimension: period {
    label: "Period"
    type: string
    sql: ${TABLE}.Period ;;
  }

  dimension: period_number {
    label: "Period Number"
    description: "Used by EmpCount latest-period FILTER(ALL(...)=MAX(...)) pattern."
    type: number
    sql: ${TABLE}.PeriodNumber ;;
  }

  dimension: qtr {
    label: "Quarter Number"
    type: number
    sql: ${TABLE}.Qtr ;;
  }

  dimension: qtr_number {
    label: "Quarter Label"
    type: string
    sql: ${TABLE}.QtrNumber ;;
  }

  dimension: year {
    label: "Year"
    type: number
    sql: ${TABLE}.Year ;;
    drill_fields: [qtr_number, month, calendar_date]
  }

  dimension: day {
    label: "Day of Month"
    type: number
    sql: ${TABLE}.Day ;;
  }

  dimension_group: month_start {
    label: "Month Start"
    type: time
    timeframes: [raw, date]
    sql: ${TABLE}.MonthStartDate ;;
    datatype: date
  }

  dimension_group: month_end {
    label: "Month End"
    type: time
    timeframes: [raw, date]
    sql: ${TABLE}.MonthEndDate ;;
    datatype: date
  }

  # Prefer warehouse MonthIncrementNumber; passthrough column
  dimension: month_increment_number {
    label: "Month Increment Number"
    type: number
    sql: ${TABLE}.MonthIncrementNumber ;;
  }

  measure: count_of_date {
    label: "Count of Date"
    description: "Power BI: COUNTA('Date'[Date])"
    type: count
  }

  # Hierarchy replacement for Date[YQM]
  set: yqm_drill {
    fields: [year, qtr_number, month, calendar_date]
  }
}
