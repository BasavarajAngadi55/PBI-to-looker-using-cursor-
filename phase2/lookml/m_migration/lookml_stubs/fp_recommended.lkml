# Option A (best practice): straight view on warehouse object
view: fp {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: fp_sdt {
  derived_table: {
    sql:
      SELECT [HR].[FP].*   FROM [HR].[FP]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
