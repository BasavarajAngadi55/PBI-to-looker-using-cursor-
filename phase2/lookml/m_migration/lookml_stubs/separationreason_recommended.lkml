# Option A (best practice): straight view on warehouse object
view: separationreason {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separationreason` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: separationreason_sdt {
  derived_table: {
    sql:
      SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
