# Option A (best practice): straight view on warehouse object
view: date {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: date_sdt {
  derived_table: {
    sql:
      SELECT [HR].[Date].*   FROM [HR].[Date]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
