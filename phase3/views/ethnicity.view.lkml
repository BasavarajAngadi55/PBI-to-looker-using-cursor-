view: ethnicity {
  label: "Ethnicity"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;

  dimension: ethnic_group {
    label: "Ethnic Group Code"
    primary_key: yes
    type: string
    sql: ${TABLE}.`Ethnic Group` ;;
  }

  dimension: ethnicity {
    label: "Ethnicity"
    type: string
    sql: ${TABLE}.Ethnicity ;;
  }
}
