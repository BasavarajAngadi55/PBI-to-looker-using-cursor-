# Calendar / period dimension from Power BI Date table.
view: date {
  label: "Date"
  sql_table_name: `hr.date` ;;

  dimension_group: calendar {
    label: "Calendar"
    description: "Primary calendar date (Date[Date])."
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.Date ;;
    datatype: date
    primary_key: yes
  }

  dimension: month {
    label: "Month Name"
    description: "Short month name (e.g. Jul)."
    type: string
    sql: ${TABLE}.Month ;;
  }

  dimension: month_number {
    label: "Month Number"
    description: "Calendar month number 1-12."
    type: number
    sql: ${TABLE}.MonthNumber ;;
  }

  dimension: period {
    label: "Period"
    description: "Period label (e.g. Jul-10)."
    type: string
    sql: ${TABLE}.Period ;;
  }

  dimension: period_number {
    label: "Period Number"
    description: "Sortable period key (e.g. 201007). Used by EmpCount latest-period logic."
    type: number
    sql: ${TABLE}.PeriodNumber ;;
  }

  dimension: qtr {
    label: "Quarter Number"
    description: "Numeric quarter."
    type: number
    sql: ${TABLE}.Qtr ;;
  }

  dimension: qtr_number {
    label: "Quarter Label"
    description: "Quarter label (e.g. Q3)."
    type: string
    sql: ${TABLE}.QtrNumber ;;
  }

  dimension: year {
    label: "Year"
    type: number
    sql: ${TABLE}.Year ;;
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

  # DAX calculated: ([Year]-MIN([Year]))*12 + [MonthNumber]
  # MIN([Year]) is model-wide; materialize in warehouse or use a constant/min subquery.
  dimension: month_increment_number {
    label: "Month Increment Number"
    description: "Sequential month index from model min year. Prefer warehouse materialization."
    # TODO: Exact DAX uses MIN(Year) over the whole Date table — confirm with a scalar subquery or warehouse column.
    type: number
    sql: ${TABLE}.MonthIncrementNumber ;;
  }

  measure: count_of_date {
    label: "Count of Date"
    description: "COUNTA of Date column."
    # DAX: COUNTA('Date'[Date])
    type: count
  }
}
