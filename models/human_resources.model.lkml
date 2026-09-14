# Human Resources Sample — LookML model migrated from Power BI PBIX
# Source: Human Resources Sample PBIX.pbix (obviEnce / Microsoft sample)
#
# Update `connection` to your Looker warehouse connection name.
# sql_table_name values assume schema `hr` — adjust to match dbt/warehouse objects.

connection: "hr_warehouse"

include: "/views/*.view.lkml"

datagroup: human_resources_default_datagroup {
  sql_trigger: SELECT MAX(date) FROM `hr.employee` ;;
  max_cache_age: "24 hours"
}

persist_with: human_resources_default_datagroup

# Primary star-schema explore: Employee fact → dimension tables.
# Power BI cardinalities were all many_to_one (M:1) with single-direction cross-filter.
explore: employee {
  label: "Human Resources"
  description: "HR analytics: actives, new hires, separations, and bad hires."

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

# Optional dimension-only explores for reference / QA
explore: date {
  label: "Date Dimension"
  hidden: yes
}

explore: bu {
  label: "BU Dimension"
  hidden: yes
}
