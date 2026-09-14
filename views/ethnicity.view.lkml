view: ethnicity {
  label: "Ethnicity"
  sql_table_name: `hr.ethnicity` ;;

  dimension: ethnic_group {
    label: "Ethnic Group"
    description: "Ethnic group code (primary key). Column name has a space in PBIX: [Ethnic Group]."
    type: string
    sql: ${TABLE}.`Ethnic Group` ;;
    primary_key: yes
  }

  dimension: ethnicity {
    label: "Ethnicity"
    description: "Ethnicity display label (e.g. Group A)."
    type: string
    sql: ${TABLE}.Ethnicity ;;
  }
}
