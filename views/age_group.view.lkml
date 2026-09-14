# MIGRATION NOTE:
# Source: Power BI AgeGroup table
# Decision: LookML dimension view over warehouse seed
# Reason: Phase 2 DIRECT / WAREHOUSE_SEED
view: age_group {
  label: "Age Group"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.age_group` ;;

  dimension: age_group_id {
    label: "Age Group ID"
    primary_key: yes
    type: number
    sql: ${TABLE}.AgeGroupID ;;
  }

  dimension: age_group {
    label: "Age Group"
    type: string
    sql: ${TABLE}.AgeGroup ;;
  }
}
