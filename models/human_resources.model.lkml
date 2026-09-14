# MIGRATION NOTE:
# Source: Power BI Human Resources Sample — 8 M:1 relationships
# Decision: single explore `employee` with left_outer many_to_one joins
# Reason: Phase 2 Section 6 DIRECT mappings
#
# TODO: USER INPUT REQUIRED — set connection to your Looker Admin connection name
connection: "YOUR_LOOKER_CONNECTION"

include: "/views/*.view.lkml"

datagroup: human_resources_default_datagroup {
  # TODO: enable after employee warehouse table exists
  # sql_trigger: SELECT MAX(date) FROM `YOUR_PROJECT.YOUR_DATASET.employee` ;;
  max_cache_age: "24 hours"
}

# persist_with: human_resources_default_datagroup

explore: employee {
  label: "Human Resources"
  description: "HR semantic model migrated from Power BI. KPI parity NOT YET VALIDATED."

  join: date {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.snapshot_date} = ${date.calendar_date} ;;
  }

  join: bu {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.bu} = ${bu.bu} ;;
  }

  join: age_group {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.age_group_id} = ${age_group.age_group_id} ;;
  }

  join: ethnicity {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.ethnic_group} = ${ethnicity.ethnic_group} ;;
  }

  join: fp {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.fp} = ${fp.fp} ;;
  }

  join: gender {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.gender_id} = ${gender.id} ;;
  }

  join: pay_type {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.pay_type_id} = ${pay_type.pay_type_id} ;;
  }

  join: separation_reason {
    type: left_outer
    relationship: many_to_one
    sql_on: ${employee.term_reason} = ${separation_reason.separation_type_id} ;;
  }
}

# Optional dim explores for QA (hidden)
explore: date {
  label: "Date Dimension"
  hidden: yes
}

explore: bu {
  label: "BU Dimension"
  hidden: yes
}
