# Phase 2 Agent A — Tables & Columns Mapping

**Agent:** A — Tables & Columns
**Phase:** 2 — Power BI → LookML mapping assessment only
**Source inventory gate:** `PASS`
**Inputs:** `inventory/01_tables_columns.json`, `inventory/COMPLETENESS_GATE.json` (reference: `LOOKML_MAPPING_ASSESSMENT.md`)
**Rule:** Mapping only. No LookML code, warehouse SQL, PDTs, or report migration.

**Counts:** 15 tables | 87 columns (gate: 15 tables, 87 columns)

## Tables → LookML Views

| Power BI Table | Table Type | Business/Internal | Recommended LookML Object | Suggested View Type | Mapping Status | Comments | Suggestion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AgeGroup | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for AgeGroup attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| BU | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for BU attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| Date | business | Business | view | Date | DIRECT | Business calendar / period dimension used by time intelligence and EmpCount. | Create date view with calendar dimension_group; expose PeriodNumber for EmpCount logic. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| Employee | business | Business | view | Fact | DIRECT | Primary fact: monthly employee snapshot grain (EmplID x date). | Create lookml view employee; point sql_table_name at warehouse table after M load. |
| Ethnicity | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for Ethnicity attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| FP | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for FP attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| Gender | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for Gender attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | calculated_table | Internal | view | Internal/Skip | SKIP_INTERNAL | Power BI auto date/time intelligence table; captured for completeness. | Do not create a business LookML view; use the business Date view + dimension_group for time. |
| PayType | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for PayType attributes. | Create dim view; seeds vs SQL per Power Query M tags. |
| SeparationReason | business | Business | view | Dimension | DIRECT | Dimension table joining to Employee for SeparationReason attributes. | Create dim view; seeds vs SQL per Power Query M tags. |

_Table row count: **15**_

## Columns → LookML Dimensions

| Power BI Table | Power BI Column | Data Type | Calculated? | Recommended LookML Object | LookML Type | Mapping Status | Comments | Suggestion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AgeGroup | AgeGroupID | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| AgeGroup | AgeGroup | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| BU | BU | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| BU | RegionSeq | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| BU | VP | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| BU | Region | 1 (automatic) | Yes | dimension | string | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Date | Date | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. Marked is_key in extraction. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | Month | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | MonthNumber | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | Period | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | PeriodNumber | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | Qtr | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | QtrNumber | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | Year | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | Day | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | MonthStartDate | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | MonthEndDate | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Date | MonthIncrementNumber | 1 (automatic) | Yes | dimension | number | WAREHOUSE_REQUIRED | Calculated column uses model-wide MIN(Year) pattern — awkward as pure LookML. | Materialize in warehouse Date table; do not invent LookML-only logic. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| Employee | date | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | EmplID | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | Gender | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | Age | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | EthnicGroup | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | FP | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | TermDate | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | isNewHire | 1 (automatic) | Yes | dimension | number | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Employee | BU | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | HireDate | 9 (datetime) | No | dimension | date_time | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | PayTypeID | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | TermReason | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Employee | AgeGroupID | 1 (automatic) | Yes | dimension | number | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Employee | TenureDays | 8 (double) | Yes | dimension | number | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Employee | TenureMonths | 1 (automatic) | Yes | dimension | number | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Employee | BadHires | 8 (double) | Yes | dimension | number | PARTIAL | Calculated column — DAX expression present in extraction; map via warehouse or LookML SQL. | Prefer warehouse materialization or LookML dimension SQL; do not invent logic. |
| Ethnicity | Ethnic Group | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Ethnicity | Ethnicity | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| FP | FP | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| FP | FPDesc | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Gender | ID | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| Gender | Gender | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| Gender | Sort | 6 (int64) | No | dimension | number | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date | datetime64[ns] | No | dimension | date_time | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Year | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | MonthNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Month | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | QuarterNo | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Quarter | 1 (automatic) | Yes | dimension | string | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Day | 1 (automatic) | Yes | dimension | number | SKIP_INTERNAL | Column on internal auto date table. | Skip direct migration; use business Date view + dimension_group. |
| PayType | PayTypeID | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| PayType | PayType | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |
| SeparationReason | SeparationTypeID | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. Hidden in Power BI. | Map name/type; preserve labels; honor hidden/key if present. |
| SeparationReason | SeparationReason | 2 (string) | No | dimension | string | DIRECT | Source/business column maps to LookML dimension. | Map name/type; preserve labels; honor hidden/key if present. |

_Column row count: **87**_

## Status legend

| Status | Meaning |
| --- | --- |
| DIRECT | Maps cleanly to a LookML view/dimension from extracted source columns |
| PARTIAL | Calculated or derived; needs DAX→SQL/LookML translation without inventing logic |
| COMPLEX | Non-trivial mapping (not used for simple column dims in this extract) |
| SKIP_INTERNAL | Power BI auto date/internal calculated table — do not migrate as business LookML |
| BLOCKED | Cannot map until a dependency is resolved (none for tables/columns in this extract) |
| WAREHOUSE_REQUIRED | Prefer warehouse materialization before LookML exposure |

