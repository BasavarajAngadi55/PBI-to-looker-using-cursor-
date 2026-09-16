# Option A (best practice): straight view on warehouse object
view: bu {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: bu_sdt {
  derived_table: {
    sql:
      select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
