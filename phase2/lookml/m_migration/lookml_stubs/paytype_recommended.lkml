# Option A (best practice): straight view on warehouse object
view: paytype {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.paytype` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: paytype_sdt {
  derived_table: {
    sql:
      select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
