# Phase 3 Agent W — Warehouse gaps (M/DAX only)

**Assumption:** Base warehouse / source tables (`AllEmps`, `Date`, `BU`, `FP`, `PayGroup`, `TermReason`, etc.) **already exist**. Phase 3 does **not** require recreating those bases.

**In scope:** Only what Power Query M / DAX adds that is **not** assumed on those bases — embedded seeds, Employee.m transforms, and business calculated columns.

**Out of scope:** Thin SQL-pass-through dims (FP, Date casts, PayType/SeparationReason projections) unless a gap below applies. Full recreate scripts under `phase3/warehouse_sql/` remain as **gap / reference templates only** — do not treat them as mandatory base DDL.

Sources: `inventory/04_m_raw/*.m`, `inventory/02_dax_objects.json`, `phase2_agents/02_dax_mapping.md`, `phase2_agents/03_rels_m_tm_mapping.md`.

---

## Gap inventory

| Power BI Object | Gap Type | M/DAX Source | Assumed Base Has? | Required Add-on | File in phase3/warehouse_sql if any | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AgeGroup | Embedded seed | `04_m_raw/AgeGroup.m` — `Table.FromRows` seed (`AgeGroupID`, `AgeGroup`) | No | Seed/load dim if missing (`1/<30`, `2/30-49`, `3/50+`) | `01_seed_age_group.sql` | TEMPLATE |
| Gender | Embedded seed | `04_m_raw/Gender.m` — embedded seed (`ID`, `Gender`, `Sort`); codes `C`/`D` | No | Seed/load dim if missing (required for Employee gender join after remap) | `02_seed_gender.sql` | TEMPLATE |
| Ethnicity | Embedded seed | `04_m_raw/Ethnicity.m` — embedded seed (`Ethnic Group`, `Ethnicity`) | No | Seed/load dim if missing | `03_seed_ethnicity.sql` | TEMPLATE |
| Employee | M transforms | `04_m_raw/Employee.m` — month spine × `AllEmps`; `dateadd(+1 year)` on Date/HireDate/TermDate; gender remap `M→C` else `D`; Age as-of; PayTypeID/BU joins; active vs sep **UNION ALL**; filters `Date < 2014-01-01`, `EmplID % 2 = 0` | No (base is raw `AllEmps` / related tables, not this fact grain) | Materialize Employee fact **only if** base does not already match M grain/logic | `09_fact_employee.sql` (transform portion) | TEMPLATE |
| Employee.isNewHire | Calculated column | DAX: `IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)` | No | Warehouse CASE or LookML dimension | `09_fact_employee.sql` | TEMPLATE |
| Employee.AgeGroupID | Calculated column | DAX: `IF([Age]<30, 1, IF([Age]<50, 2, 3))` | No | Warehouse CASE or LookML; join key to AgeGroup seed | `09_fact_employee.sql` | TEMPLATE |
| Employee.TenureDays | Calculated column | DAX: `IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])` | No | Warehouse abs date-diff (or LookML) | `09_fact_employee.sql` | TEMPLATE |
| Employee.TenureMonths | Calculated column | DAX: `CEILING([TenureDays]/30, 1) -1` | No | Warehouse column after TenureDays (confirm CEILING parity) | `09_fact_employee.sql` | TEMPLATE |
| Employee.BadHires | Calculated column | DAX: `IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)` | No | Warehouse CASE on HireDate/TermDate | `09_fact_employee.sql` | TEMPLATE |
| BU.Region | Calculated column | DAX: `mid([RegionSeq], 3,15)` | No (`RegionSeq`/source title may exist; display `Region` is DAX) | `SUBSTR`/`MID` column or LookML dimension | `07_dim_bu.sql` | TEMPLATE |
| Date.MonthIncrementNumber | Calculated column | DAX: `([Year]-MIN([Year]))*12 +[MonthNumber]` | No | Materialize using model-wide `MIN(Year)` (awkward as pure LookML) | `08_dim_date.sql` | TEMPLATE |

---

## Counts

| Category | Gap rows |
| --- | ---: |
| Embedded seeds (if missing) | 3 |
| Employee.m transforms (if not in base) | 1 |
| Calculated columns | 7 |
| **Total gaps** | **11** |

Status `TEMPLATE` = reference SQL exists under `phase3/warehouse_sql/`; not executed; apply only when the corresponding base object is missing or incomplete.

---

## Explicit non-gaps (assumed on base)

Do **not** treat as warehouse gaps under this Phase 3 rule:

- Base tables / columns already landed from source for Date, FP, BU (`BU`/`RegionSeq`/`VP`), PayGroup→PayType keys, TermReason→SeparationReason keys, AllEmps attributes used by Employee.m.
- Thin type-cast / `SELECT *` M queries (e.g. FP, Date) when warehouse already matches model columns.
- Internal LocalDateTable_* / DateTableTemplate_* (SKIP — use business Date).

Files `04_dim_fp.sql`, `05_dim_pay_type.sql`, `06_dim_separation_reason.sql` (and full recreate paths in `07`–`09`) may remain for reference; they are **not** listed as gaps when bases are assumed present.
