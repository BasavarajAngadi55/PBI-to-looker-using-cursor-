# LOOKML Mapping Assessment — Phase 2

**Phase:** 2 — Power BI → LookML mapping assessment only
**Source inventory gate:** `PASS`
**Rule:** Analysis and mapping only. No LookML, warehouse SQL, PDTs, or report migration in this phase.

**Specialist agents (this Phase 2 run):**

| Agent | Role | Run ID | Source file |
| --- | --- | --- | --- |
| Agent A | Tables/Columns | `50c88854-f6dc-4dcf-91e1-a341271cf74f` | `phase2_agents/01_tables_columns_mapping.md` |
| Agent B | DAX (measures / calc columns / calc tables) | `c0350563-a279-4e91-9675-4abd0cd0dd97` | `phase2_agents/02_dax_mapping.md` |
| Agent C | Relationships / M / TM extras | `2fca12df-73c6-4de1-92e6-c6ca845c3d94` | `phase2_agents/03_rels_m_tm_mapping.md` |
| Agent D | Mapping Merger (this document) | this run | merges A+B+C + `inventory/COMPLETENESS_GATE.json` |

Inputs used: specialist Phase 2 mapping files above, plus Phase 1 `inventory/COMPLETENESS_GATE.json` (status PASS). Content is merged from specialists only — nothing invented.

## Section 1 — Tables → LookML Views

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

## Section 2 — Columns → LookML Dimensions

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

## Section 3 — Measures → LookML Measures

| Table | Measure | Original DAX | Recommended LookML Object | Suggested Measure Type | Mapping Status | Complexity | Comments | Suggestion | KPI Impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Employee | EmpCount | CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber]))) | measure | count_distinct | COMPLEX | COMPLEX | EmpCount uses FILTER(ALL(PeriodNumber), PeriodNumber = MAX(...)) latest-period pattern. | Use always_filter / liquid / SQL max-period filter; do not treat as plain COUNT. | Affects EmpCount, EmpCount SPLY, and Actives if Actives wraps EmpCount. |
| Employee | Seps | CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate])))) | measure | count_distinct | PARTIAL | MODERATE | CALCULATE COUNT with FILTER where TermDate is not blank. Employee.m UNION supplies TermDate only on sep rows. | Filtered count_distinct on EmplID where TermDate is not null; confirm with Employee.m active/sep union grain. | Separations KPI. |
| Employee | Actives | CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate]))) | measure | count_distinct | PARTIAL | MODERATE | CALCULATE([EmpCount], ISBLANK(TermDate)). Depends on EmpCount latest-period logic and Employee.m active rows (TermDate null). | Filtered EmpCount / count where TermDate is null; resolve EmpCount COMPLEX pattern first. | Actives KPI; blocked until EmpCount period logic is designed. |
| Employee | New Hires | SUM([isNewHire]) | measure | sum | DIRECT | SIMPLE | Additive sum over a column/flag. | Implement as type:sum on the corresponding dimension/flag. | Core volume KPI. |
| Employee | AVG Tenure Days | AVERAGE([TenureDays]) | measure | average | DIRECT | SIMPLE | Average aggregation. | Implement as type:average (apply ROUND in SQL/LookML if needed). | Average KPI. |
| Employee | AVG Tenure Months | ROUND([AVG Tenure Days]/30, 1)-1 | measure | average | PARTIAL | SIMPLE | Derived from another measure with ROUND arithmetic. | Implement as type:number referencing base average measure; confirm rounding parity. | Tenure months KPI. |
| Employee | AVG Age | ROUND(AVERAGE([Age]), 0) | measure | average | DIRECT | SIMPLE | Average aggregation. | Implement as type:average (apply ROUND in SQL/LookML if needed). | Average KPI. |
| Employee | Sum of BadHires | SUM([BadHires]) | measure | sum | DIRECT | SIMPLE | Additive sum over a column/flag. | Implement as type:sum on the corresponding dimension/flag. | Core volume KPI. |
| Employee | New Hires SPLY | CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date])) | measure | number | COMPLEX | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. |
| Employee | Actives SPLY | CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date])) | measure | number | COMPLEX | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. |
| Employee | Seps SPLY | CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date])) | measure | number | COMPLEX | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. |
| Employee | EmpCount SPLY | CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])),SAMEPERIODLASTYEAR('Date'[Date])) | measure | number | COMPLEX | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. |
| Employee | Seps YoY Var | [Seps]-[Seps SPLY] | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Actives YoY Var | [Actives]-[Actives SPLY] | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | New Hires YoY Var | [New Hires]-[New Hires SPLY] | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Seps YoY % Change | DIVIDE([Seps YoY Var], [Seps SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Actives YoY % Change | DIVIDE([Actives YoY Var], [Actives SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | New Hires YoY % Change | DIVIDE([New Hires YoY Var], [New Hires SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Bad Hires SPLY | CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date])) | measure | number | COMPLEX | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. |
| Employee | Bad Hires YoY Var | [Sum of BadHires]-[Bad Hires SPLY] | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Bad Hires YoY % Change | DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | TO % | DIVIDE([Seps], [Actives]) | measure | number | DIRECT | SIMPLE | Ratio of existing measures; maps to SAFE_DIVIDE pattern in LookML. | Implement as type:number with SAFE_DIVIDE; format as percent. | Ratio KPI. |
| Employee | TO % Norm | CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity])) | measure | number | COMPLEX | COMPLEX | Uses ALL() to ignore Gender/Ethnicity filter context (TO % Norm pattern). | Implement via filtered measure / explore that ignores those dimensions; parity-test vs Power BI. | Blocks TO % Norm and TO % Var. |
| Employee | TO % Var | [TO %]-[TO % Norm] | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | Sep%ofActive | DIVIDE([Seps],[Actives]) | measure | number | DIRECT | SIMPLE | Ratio of existing measures; maps to SAFE_DIVIDE pattern in LookML. | Implement as type:number with SAFE_DIVIDE; format as percent. | Ratio KPI. |
| Employee | Sep%ofSMLYActives | DIVIDE([Seps SPLY],[Actives SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| Employee | BadHire%ofActives | DIVIDE([Sum of BadHires],[Actives]) | measure | number | DIRECT | SIMPLE | Ratio of existing measures; maps to SAFE_DIVIDE pattern in LookML. | Implement as type:number with SAFE_DIVIDE; format as percent. | Ratio KPI. |
| Employee | BadHire%ofActiveSPLY | DIVIDE([Bad Hires SPLY],[Actives SPLY]) | measure | number | PARTIAL | SIMPLE | Arithmetic on parent measures that include blocked SPLY/Norm parents. | Keep formula ready; light up only after parent SPLY/Norm measures work. | Dependent KPI until parents resolve. |
| BU | Count of BU | COUNTA('BU'[BU]) | measure | count_distinct | DIRECT | SIMPLE | COUNTA on BU dimension key. | Implement as count/count_distinct on BU; validate grain. | Dimension count KPI. |
| Date | Count of Date | COUNTA('Date'[Date]) | measure | count_distinct | DIRECT | SIMPLE | COUNTA on Date calendar key. | Implement as count/count_distinct on Date; rarely used as HR KPI. | Calendar count KPI. |

## Section 4 — Calculated Columns → LookML Dimensions / Other

| Table | Calculated Column | Original DAX | Recommended LookML Object | Mapping Status | Complexity | Comments | Suggestion | Dependency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BU | Region | mid([RegionSeq], 3,15) | dimension | DIRECT | SIMPLE | MID/SUBSTR of RegionSeq — simple string derivation. | LookML SUBSTR or warehouse column Region. | BU.m |
| Date | MonthIncrementNumber | ([Year]-MIN([Year]))*12 +[MonthNumber] | warehouse calculation | WAREHOUSE_REQUIRED | MODERATE | Uses model-wide MIN(Year) pattern — awkward as pure LookML. | Materialize in warehouse Date table. | Date.m / Date table |
| Employee | isNewHire | IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1) | dimension | DIRECT | SIMPLE | Flags hire month vs snapshot date. Employee.m provides HireDate (shifted SenDate) and monthly date grain. | Prefer warehouse CASE; LookML dimension acceptable for prototype. | Employee.m (HireDate, date) |
| Employee | AgeGroupID | IF([Age]<30, 1, IF([Age]<50, 2, 3)) | dimension | DIRECT | SIMPLE | Buckets Age for AgeGroup join. Employee.m supplies Age adjusted by snapshot year. | Prefer warehouse CASE or LookML; join to AgeGroup seed. | Employee.m (Age) |
| Employee | TenureDays | IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate]) | dimension | DIRECT | SIMPLE | Abs days between snapshot date and HireDate. Depends on Employee.m date/HireDate columns. | Materialize in warehouse for large Employee; else LookML SQL. | Employee.m (date, HireDate) |
| Employee | TenureMonths | CEILING([TenureDays]/30, 1) -1 | dimension | DIRECT | SIMPLE | Derived from TenureDays (CEILING/30 - 1). | Warehouse column after TenureDays; confirm CEILING parity. | Employee calculated TenureDays / Employee.m |
| Employee | BadHires | IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1) | dimension | DIRECT | SIMPLE | 1 if terminated within 61 days of hire; 0 if active (blank TermDate) or longer tenure. Employee.m sets TermDate null on active UNION branch. | Warehouse CASE using HireDate/TermDate from Employee.m. | Employee.m (HireDate, TermDate) |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Year | YEAR([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | MonthNo | MONTH([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Month | FORMAT([Date], "MMMM") | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | QuarterNo | INT(([MonthNo] + 2) / 3) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Quarter | "Qtr " & [QuarterNo] | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Day | DAY([Date]) | no direct equivalent | SKIP_INTERNAL | SIMPLE | Calculated column on auto date table. | Skip; use business Date model. | Auto date table |

## Section 5 — Calculated Tables

| Power BI Table | Original DAX | Recommended LookML Representation | Mapping Status | Comments | Suggestion | Dependency |
| --- | --- | --- | --- | --- | --- | --- |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Calendar(Date(2015,1,1), Date(2015,1,1)) | no direct equivalent | SKIP_INTERNAL | Power BI auto-generated date table (Calendar DAX). | Skip LookML view; rely on business Date + Looker timeframes. | Power BI time intelligence |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Calendar(Date(Year(MIN('Date'[Date])), 1, 1), Date(Year(MAX('Date'[Date])), 12, 31)) | no direct equivalent | SKIP_INTERNAL | Power BI auto LocalDateTable driven by Date column range. | Skip LookML view; rely on business Date + Looker timeframes. | Date.m / Date table |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Calendar(Date(Year(MIN('Date'[MonthStartDate])), 1, 1), Date(Year(MAX('Date'[MonthStartDate])), 12, 31)) | no direct equivalent | SKIP_INTERNAL | Power BI auto LocalDateTable driven by Date column range. | Skip LookML view; rely on business Date + Looker timeframes. | Date.m / Date table |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Calendar(Date(Year(MIN('Date'[MonthEndDate])), 1, 1), Date(Year(MAX('Date'[MonthEndDate])), 12, 31)) | no direct equivalent | SKIP_INTERNAL | Power BI auto LocalDateTable driven by Date column range. | Skip LookML view; rely on business Date + Looker timeframes. | Date.m / Date table |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Calendar(Date(Year(MIN('Employee'[TermDate])), 1, 1), Date(Year(MAX('Employee'[TermDate])), 12, 31)) | no direct equivalent | SKIP_INTERNAL | Power BI auto LocalDateTable driven by Employee date column range. | Skip LookML view; rely on business Date + Looker timeframes. | Employee.m date bounds (HireDate/TermDate) |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Calendar(Date(Year(MIN('Employee'[HireDate])), 1, 1), Date(Year(MAX('Employee'[HireDate])), 12, 31)) | no direct equivalent | SKIP_INTERNAL | Power BI auto LocalDateTable driven by Employee date column range. | Skip LookML view; rely on business Date + Looker timeframes. | Employee.m date bounds (HireDate/TermDate) |

## Section 6 — Relationships → LookML Joins

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter | Active | Recommended LookML Join | LookML Relationship | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Employee | date | Date | Date | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Fact→dim date; single-direction filter matches Looker left_outer. |
| Employee | FP | FP | FP | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Standard dim join on FP key. |
| Employee | EthnicGroup | Ethnicity | Ethnic Group | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Column names differ (`EthnicGroup` vs `Ethnic Group`) — align in sql_on. |
| Employee | Gender | Gender | ID | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Fact holds Gender codes that match dim `ID` (not display label). |
| Employee | PayTypeID | PayType | PayTypeID | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Standard dim join. |
| Employee | BU | BU | BU | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Standard dim join on market/BU key. |
| Employee | AgeGroupID | AgeGroup | AgeGroupID | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | AgeGroupID is calculated on Employee in model; join still M:1 to seed dim. |
| Employee | TermReason | SeparationReason | SeparationTypeID | M:1 | Single | true | left_outer on explore | many_to_one | DIRECT | Fact `TermReason` stores SeparationTypeID values. |

## Section 7 — Power Query / M → Looker Data Layer

| Power Query | M file | Tags | Recommended Destination | Mapping Status | Comments (M delta vs base tables) |
| --- | --- | --- | --- | --- | --- |
| BU | `04_m_raw/BU.m` | sql_database, query_reference | Warehouse SQL | WAREHOUSE_REQUIRED | Not a raw `hr.bu` dump: `SELECT DISTINCT` with aliases `market→BU`, `REGIONTITLE→Region` then M rename **Region→RegionSeq**, `MARKETDIRECTOR→VP`. If base `hr.bu` has UNIT/other columns, model shape is this 3-col projection only. |
| FP | `04_m_raw/FP.m` | sql_database, query_reference | Review | PARTIAL | `SELECT [HR].[FP].*` + type cast only. If warehouse `HR.FP` already matches `FP`/`FPDesc`, LookML can point at base; else thin SQL/view for types. |
| PayType | `04_m_raw/PayType.m` | sql_database, query_reference | Warehouse SQL | WAREHOUSE_REQUIRED | Built from **`[HR].[PayGroup]`**, not a PayType table: `DISTINCT PayTypeID, [Hrly-Salaried] AS PayType`. Label column and grain may not exist as-is on base PayGroup. |
| SeparationReason | `04_m_raw/SeparationReason.m` | sql_database, query_reference | Warehouse SQL | WAREHOUSE_REQUIRED | From **`[HR].[TermReason]`**: `DISTINCT SeparationTypeID, [Vol-Invol] AS SeparationReason`. Renames source columns; not a 1:1 table copy. |
| Date | `04_m_raw/Date.m` | sql_database, query_reference | Review | PARTIAL | `SELECT [HR].[Date].*` + casts. If warehouse `HR.Date` already has Date/Month/Period/Qtr/Year/MonthStart/End, Review only; M adds no business transforms. |
| Employee | `04_m_raw/Employee.m` | sql_database, append_union, query_reference, transformation_heavy | Warehouse SQL | WAREHOUSE_REQUIRED | **Not** base `AllEmps`. M SQL adds: month-start spine via Date join; **dateadd(+1 year)** on Date/HireDate/TermDate; **Gender remap** `M→C` else `D`; **Age as-of** formula; PayTypeID via PayGroup; BU via Market/UNIT; active vs sep **UNION ALL**; TermReason from TermReason; filters `d.Date < 2014-01-01`, `EmplID % 2 = 0`. Must materialize even if AllEmps/Date/BU/PayGroup exist. |
| Ethnicity | `04_m_raw/Ethnicity.m` | embedded_seed, query_reference | Seed | WAREHOUSE_REQUIRED | Entire dim is **embedded** `Table.FromRows` (no SQL source). Not on any base table — load seed (Ethnic Group, Ethnicity). |
| Gender | `04_m_raw/Gender.m` | embedded_seed, query_reference | Seed | WAREHOUSE_REQUIRED | Embedded seed (ID, Gender, Sort). Not on SQL Server — required for join keys `C`/`D` used by Employee M. |
| AgeGroup | `04_m_raw/AgeGroup.m` | embedded_seed, query_reference | Seed | WAREHOUSE_REQUIRED | Embedded seed (AgeGroupID, AgeGroup). Not on SQL Server; needed once AgeGroupID calc column exists. |

## Section 8 — Hierarchies

| Table | Hierarchy | Levels (ordinal) | Recommended LookML Approach | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| Date | YQM | 0 Year(Year) > 1 QtrNumber(QtrNumber) > 2 PeriodNumber(PeriodNumber) | drill_fields / ordered dimensions | PARTIAL | Only **business** hierarchy; approximate with drill_fields on Date view. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |

## Section 9 — RLS / Security

| RLS | Status | Comments |
| --- | --- | --- |
| — | NONE_IN_SOURCE | No RLS roles, role memberships, or column permissions in `05_tmschema_extras.json` (`rls=0`, `ols=0`, `role_memberships=0`, `column_permissions=0`). |

## Section 10 — Partitions

| Table / Group | Partition Name | Type | Mode | Recommended Treatment | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| BU | BU | 4 (M) | 0 (Import) | Warehouse refresh / view | PARTIAL | M partition = BU query. LookML has no partition object. |
| FP | FP | 4 | 0 | Warehouse refresh / view | PARTIAL | M partition = FP query. |
| PayType | PayGroup | 4 | 0 | Warehouse refresh / view | PARTIAL | Partition **Name** is `PayGroup` (source query name); table is PayType. |
| SeparationReason | TermReason | 4 | 0 | Warehouse refresh / view | PARTIAL | Partition **Name** is `TermReason`; table is SeparationReason. |
| Date | Date | 4 | 0 | Warehouse refresh / view | PARTIAL | M partition = Date query. |
| Employee | Employee | 4 | 0 | Warehouse refresh / view | PARTIAL | Heavy M partition; drives fact grain. |
| Ethnicity | Ethnicity | 4 | 0 | Seed load | PARTIAL | Embedded M partition. |
| Gender | Gender | 4 | 0 | Seed load | PARTIAL | Embedded M partition. |
| AgeGroup | AgeGroup | 4 | 0 | Seed load | PARTIAL | Embedded M partition. |
| *(internals)* | — | — | — | SKIP_INTERNAL | SKIP_INTERNAL | **113** remaining partitions: 6 auto-date table partitions + 87 `H$*` attribute-hierarchy + 7 `U$*` user-hierarchy + 13 `R$*` relationship storage. Not migrated. |

## Section 11 — Sort-By Columns

| Table | Column | Sort By Column | Status | Comments |
| --- | --- | --- | --- | --- |
| — | — | — | NONE_IN_SOURCE | `sort_by_columns` list empty in TM extras. Note: Gender seed has a `Sort` **column** but no SortByColumn metadata linking another column to it. |

## Section 12 — Formatting / Display Metadata

| Table | Object | Power BI Format | Recommended LookML Formatting | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| Date | Date | General Date | value_format_name: date | PARTIAL | Column format_string from TM extras. |
| Date | MonthStartDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Date | MonthEndDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Employee | date | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Employee | TermDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| *(display_folders)* | — | — | group_label | NONE_IN_SOURCE | `display_folders` empty. |
| *(PBI_FormatHint)* | various columns/measures | `{"isGeneralNumber":true}` × 18 annotations | value_format_name: decimal | PARTIAL | Annotation hints only; not full format strings. |

## Section 13 — Auto Date Tables

| Internal Table | Columns | Hierarchy | Recommended Treatment | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Template auto calendar; use business `Date` + Looker timeframes. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[Date]` variation. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[MonthStartDate]`. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[MonthEndDate]`. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Employee[TermDate]`. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Employee[HireDate]`. |

## Section 14 — Annotations / Other Tabular Metadata

| Object | Metadata Type | Power BI Value | LookML Equivalent | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| perspectives | perspectives | — | Explore curation | NONE_IN_SOURCE | Empty (`perspectives=0`). |
| rls / ols | security | — | access_grant / sql_always_where | NONE_IN_SOURCE | Empty (see §4). |
| connections | other.connections | — | Looker connection | NONE_IN_SOURCE | Empty array. |
| aggregations | other.aggregations | — | aggregate_table | NONE_IN_SOURCE | Empty array. |
| annotations (bulk) | annotations | 158 records | No 1:1 | PARTIAL | Mostly `SummarizationSetBy` (87), `TemplateId` (42), `PBI_FormatHint` (18), auto-date flags — do not auto-migrate. |
| __PBI_TimeIntelligenceEnabled | metadata | 1 | — | PARTIAL | Informational; prefer business Date + PoP patterns. |
| __PBI_LegacyCustomDateTable | annotation | true (on Date) | — | PARTIAL | Confirms business Date is custom calendar, not auto-date. |
| PBIDesktopVersion | metadata | 2.109.6661.0001 (Main) | — | PARTIAL | Informational. |
| PBI_QueryOrder | metadata | BU, FP, PayType, SeparationReason, Date, Employee, Ethnicity, Gender, AgeGroup | — | PARTIAL | Refresh/order hint only. |
| cultures | cultures | en-US | locale / value formats | PARTIAL | One culture row. |
| variations | variations | 5 (Date×3, Employee TermDate/HireDate) | No direct equivalent | SKIP_INTERNAL | Tie date columns to LocalDateTable hierarchies; skip with auto dates. |
| attribute_hierarchies | attribute_hierarchies | 102 | — | SKIP_INTERNAL | Engine storage; not business objects. |
| linguistic_metadata_present | other | true | — | PARTIAL | Present but not required for LookML. |

## Section 15 — Complex / Unmapped Objects

| Object Type | Table | Object | Mapping Status | Why Direct Mapping Is Difficult | Dependency | Recommended Approach | KPI Impact | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| measure | Employee | EmpCount | COMPLEX | EmpCount uses FILTER(ALL(PeriodNumber), PeriodNumber = MAX(...)) latest-period pattern. | Date / filter context / parent measures | Use always_filter / liquid / SQL max-period filter; do not treat as plain COUNT. | Affects EmpCount, EmpCount SPLY, and Actives if Actives wraps EmpCount. | HIGH |
| measure | Employee | New Hires SPLY | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Date / filter context / parent measures | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. | HIGH |
| measure | Employee | Actives SPLY | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Date / filter context / parent measures | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. | HIGH |
| measure | Employee | Seps SPLY | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Date / filter context / parent measures | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. | HIGH |
| measure | Employee | EmpCount SPLY | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Date / filter context / parent measures | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. | HIGH |
| measure | Employee | Bad Hires SPLY | COMPLEX | Uses SAMEPERIODLASTYEAR and requires date-filter context validation. | Date / filter context / parent measures | Review LookML time-based / PoP implementation and validate against Power BI KPI results. | Blocks YoY and SPLY-dependent KPIs until implemented. | HIGH |
| measure | Employee | TO % Norm | COMPLEX | Uses ALL() to ignore Gender/Ethnicity filter context (TO % Norm pattern). | Date / filter context / parent measures | Implement via filtered measure / explore that ignores those dimensions; parity-test vs Power BI. | Blocks TO % Norm and TO % Var. | HIGH |
| calculated_column | Date | MonthIncrementNumber | WAREHOUSE_REQUIRED | Uses model-wide MIN(Year) pattern — awkward as pure LookML. | Date.m / Date table | Materialize in warehouse Date table. | Feeds measures that reference this column | MEDIUM |
| power_query | Employee | `04_m_raw/Employee.m` | WAREHOUSE_REQUIRED | **Not** base `AllEmps`. M SQL adds: month-start spine via Date join; **dateadd(+1 year)** on Date/HireDate/TermDate; **Gender remap** `M→C` else `D`; **Age as-of** formula; PayTypeID via PayGroup; BU via Market/UNIT; active vs sep **UNION ALL**; TermReason from TermReason; filters `d.Date < 2014-01-01`, `EmplID % 2 = 0`. Must materialize even if AllEmps/Date/BU/PayGroup exist. | `04_m_raw/Employee.m` | Port M to Warehouse SQL before LookML KPIs. | ALL Employee measures / KPIs | HIGH |

_Derived from specialist rows marked COMPLEX / WAREHOUSE_REQUIRED (and Employee.m as critical warehouse dependency)._

## Section 16 — Overall Object Mapping Summary

| Power BI Object Type | Total | Direct Mapping | Partial | Complex | Warehouse Required | Skip Internal | Blocked |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tables | 15 | 9 | 0 | 0 | 0 | 6 | 0 |
| Columns | 87 | 38 | 6 | 0 | 1 | 42 | 0 |
| Measures | 30 | 9 | 14 | 7 | 0 | 0 | 0 |
| Calculated Columns | 43 | 6 | 0 | 0 | 1 | 36 | 0 |
| Calculated Tables | 6 | 0 | 0 | 0 | 0 | 6 | 0 |
| Relationships | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| Power Query | 9 | 0 | 2 | 0 | 7 | 0 | 0 |
| Hierarchies | 7 | 0 | 1 | 0 | 0 | 6 | 0 |
| RLS | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

_Totals derived from Phase 1 extraction (gate `PASS`): tables=15, columns=87, measures=30, calculated_columns=43, calculated_tables=6, relationships=8, power_query=9, hierarchies=7, partitions=122, rls_roles=0._

## Mapping Status Definitions (reference)

| Status | Meaning |
| --- | --- |
| DIRECT | Clear one-to-one conceptual mapping |
| PARTIAL | Representable in LookML with extra design/validation |
| COMPLEX | Not safe as a simple LookML object |
| WAREHOUSE_REQUIRED | Prefer warehouse before LookML |
| SKIP_INTERNAL | Captured PBI internal; normally not migrated |
| BLOCKED | Required information missing from extraction |
| NONE_IN_SOURCE / NO_DIRECT_EQUIVALENT | Empty category or no LookML equivalent |

# Next Phase

This document is the **design/mapping layer only**.

The next phase will use this assessment to generate:

1. Warehouse SQL where required
2. LookML views
3. LookML measures
4. LookML joins
5. LookML model/explore
6. Security implementation
7. KPI parity testing

Those tasks are **not** performed in Phase 2.
