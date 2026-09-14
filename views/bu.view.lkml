# Business Unit / Region dimension.
view: bu {
  label: "Business Unit"
  sql_table_name: `hr.bu` ;;

  dimension: bu {
    label: "BU"
    description: "Business unit / market identifier (primary key)."
    type: string
    sql: ${TABLE}.BU ;;
    primary_key: yes
  }

  dimension: region_seq {
    label: "Region Sequence"
    description: "Region sort label (e.g. 1-North)."
    type: string
    sql: ${TABLE}.RegionSeq ;;
  }

  dimension: vp {
    label: "VP"
    description: "Market director / VP name."
    type: string
    sql: ${TABLE}.VP ;;
  }

  # DAX calculated: mid([RegionSeq], 3, 15) — characters after the ordinal prefix.
  dimension: region {
    label: "Region"
    description: "Region name derived from RegionSeq (e.g. North)."
    type: string
    sql: COALESCE(${TABLE}.Region, SUBSTR(${TABLE}.RegionSeq, 3)) ;;
  }

  measure: count_of_bu {
    label: "Count of BU"
    description: "COUNTA of BU."
    # DAX: COUNTA('BU'[BU])
    type: count
  }
}
