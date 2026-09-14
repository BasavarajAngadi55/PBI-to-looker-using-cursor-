# Phase 2 Agent C — Relationships, Power Query M, Hierarchies, RLS, Partitions, Auto Dates

**Source inventories:** `inventory/03_relationships.json`, `inventory/04_power_query_m.json`, `inventory/05_tmschema_extras.json`, `inventory/04_m_raw/*.m` (names/tags only)  
**Output only:** mapping tables (no LookML / SQL generation)

---

## 1. Relationships → LookML Joins

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

**Section count:** 8 relationships

---

## 2. Power Query → Looker Data Layer

Assumption: **base warehouse / source tables may already exist**. Destination is chosen among **Warehouse SQL / Seed / Review**. Comments focus on what M adds that may **not** already be on those base tables.

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

**Section count:** 9 queries (6 SQL / 3 embedded seed)

---

## 3. Hierarchies

| Table | Hierarchy | Levels (ordinal) | Recommended LookML Approach | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| Date | YQM | 0 Year(Year) > 1 QtrNumber(QtrNumber) > 2 PeriodNumber(PeriodNumber) | drill_fields / ordered dimensions | PARTIAL | Only **business** hierarchy; approximate with drill_fields on Date view. |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date Hierarchy | Year > Quarter > Month > Day | timeframes on business date | SKIP_INTERNAL | Auto-date hierarchy. |

**Section count:** 7 hierarchies (1 business + 6 SKIP_INTERNAL)

---

## 4. RLS

| RLS | Status | Comments |
| --- | --- | --- |
| — | NONE_IN_SOURCE | No RLS roles, role memberships, or column permissions in `05_tmschema_extras.json` (`rls=0`, `ols=0`, `role_memberships=0`, `column_permissions=0`). |

**Section count:** 0 RLS roles (explicit NONE_IN_SOURCE)

---

## 5. Partitions

122 partition rows in TM extras. Summarized: **one row per business table** + internal rollup.

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

**Section count:** 9 business rows + 1 internal summary (covers 122 total)

---

## 6. Sort-by

| Table | Column | Sort By Column | Status | Comments |
| --- | --- | --- | --- | --- |
| — | — | — | NONE_IN_SOURCE | `sort_by_columns` list empty in TM extras. Note: Gender seed has a `Sort` **column** but no SortByColumn metadata linking another column to it. |

**Section count:** 0 (NONE)

---

## 7. Formatting metadata

| Table | Object | Power BI Format | Recommended LookML Formatting | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| Date | Date | General Date | value_format_name: date | PARTIAL | Column format_string from TM extras. |
| Date | MonthStartDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Date | MonthEndDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Employee | date | General Date | value_format_name: date | PARTIAL | Column format_string. |
| Employee | TermDate | General Date | value_format_name: date | PARTIAL | Column format_string. |
| *(display_folders)* | — | — | group_label | NONE_IN_SOURCE | `display_folders` empty. |
| *(PBI_FormatHint)* | various columns/measures | `{"isGeneralNumber":true}` × 18 annotations | value_format_name: decimal | PARTIAL | Annotation hints only; not full format strings. |

**Section count:** 5 format_strings + empty display_folders + 18 FormatHint annotations noted

---

## 8. Auto date tables

| Internal Table | Columns | Hierarchy | Recommended Treatment | Mapping Status | Comments |
| --- | --- | --- | --- | --- | --- |
| DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Template auto calendar; use business `Date` + Looker timeframes. |
| LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[Date]` variation. |
| LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[MonthStartDate]`. |
| LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Date[MonthEndDate]`. |
| LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Employee[TermDate]`. |
| LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date, Year, MonthNo, Month, QuarterNo, Quarter, Day | Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | Local date for `Employee[HireDate]`. |

**Section count:** 6 auto date tables (all SKIP_INTERNAL)

---

## 9. Annotations / other TM

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

**Section count:** 13 annotation/other rows (empty categories marked NONE_IN_SOURCE)

---

## Section counts (summary)

| # | Section | Rows / count |
| ---: | --- | --- |
| 1 | Relationships → LookML Joins | **8** |
| 2 | Power Query → Looker data layer | **9** |
| 3 | Hierarchies | **7** |
| 4 | RLS | **0** (NONE_IN_SOURCE) |
| 5 | Partitions | **9** business + **113** internals summarized |
| 6 | Sort-by | **0** (NONE) |
| 7 | Formatting metadata | **5** format_strings (+ empty folders / FormatHints noted) |
| 8 | Auto date tables | **6** (all SKIP_INTERNAL) |
| 9 | Annotations / other TM | **13** rows (empties = NONE_IN_SOURCE) |

**Path:** `phase2_agents/03_rels_m_tm_mapping.md`
