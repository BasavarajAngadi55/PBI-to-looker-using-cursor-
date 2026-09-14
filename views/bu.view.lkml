# MIGRATION NOTE:
# Source: Power BI BU + calculated Region
# Decision: Region from warehouse (SUBSTR) with LookML COALESCE fallback
view: bu {
  label: "Business Unit"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;

  dimension: bu {
    label: "BU"
    primary_key: yes
    type: string
    sql: ${TABLE}.BU ;;
  }

  dimension: region_seq {
    label: "Region Sequence"
    type: string
    sql: ${TABLE}.RegionSeq ;;
  }

  dimension: vp {
    label: "VP"
    type: string
    sql: ${TABLE}.VP ;;
  }

  # DAX: MID([RegionSeq], 3, 15)
  dimension: region {
    label: "Region"
    type: string
    sql: COALESCE(${TABLE}.Region, SUBSTR(${TABLE}.RegionSeq, 3)) ;;
  }

  measure: count_of_bu {
    label: "Count of BU"
    description: "Power BI: COUNTA('BU'[BU])"
    type: count
  }
}
