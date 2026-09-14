# Phase 3 Agent L — LookML Accountability Check

**Sources reviewed:** `phase3/views/*.lkml`, `phase3/models/human_resources.model.lkml`, `inventory/01_tables_columns.json`, `inventory/02_dax_objects.json`, `inventory/03_relationships.json`, `LOOKML_MAPPING_ASSESSMENT.md`, `phase3/IMPLEMENTATION_COVERAGE.md`

**Accountability verdict: PARTIAL**

Structural coverage (9 business views, 8 joins, 7 business calc columns, RLS N/A) is complete. Measure parity is incomplete: **7 TODO** + **12 PARTIAL** of 30 DAX measures. KPI parity not validated.

---

## 1. Views present vs 9 business tables

| # | PBI business table | LookML view file | Status | Notes |
| --- | --- | --- | --- | --- |
| 1 | AgeGroup | `phase3/views/age_group.view.lkml` | PRESENT | Joined on explore |
| 2 | BU | `phase3/views/bu.view.lkml` | PRESENT | Includes Region calc dim |
| 3 | Date | `phase3/views/date.view.lkml` | PRESENT | Includes MonthIncrementNumber |
| 4 | Employee | `phase3/views/employee.view.lkml` | PRESENT | Explore base |
| 5 | Ethnicity | `phase3/views/ethnicity.view.lkml` | PRESENT | |
| 6 | FP | `phase3/views/fp.view.lkml` | PRESENT | |
| 7 | Gender | `phase3/views/gender.view.lkml` | PRESENT | |
| 8 | PayType | `phase3/views/pay_type.view.lkml` | PRESENT | |
| 9 | SeparationReason | `phase3/views/separation_reason.view.lkml` | PRESENT | |

**Result: 9/9 PRESENT.** Internal auto-date tables (6) correctly omitted (SKIP_INTERNAL per mapping §13).

---

## 2. Measures present vs 30 DAX measures

| # | PBI measure | LookML measure | Status | File / notes |
| --- | --- | --- | --- | --- |
| 1 | Employee.EmpCount | `emp_count` | TODO | Stub `count_distinct`; missing MAX(PeriodNumber) over ALL PeriodNumber |
| 2 | Employee.Seps | `seps` | IMPLEMENTED | TermDate filter |
| 3 | Employee.Actives | `actives` | PARTIAL | Distinct count where TermDate blank; does not nest EmpCount period logic |
| 4 | Employee.New Hires | `new_hires` | IMPLEMENTED | `sum` of `is_new_hire` |
| 5 | Employee.AVG Tenure Days | `avg_tenure_days` | IMPLEMENTED | |
| 6 | Employee.AVG Tenure Months | `avg_tenure_months` | IMPLEMENTED | Derived from avg tenure days |
| 7 | Employee.AVG Age | `avg_age` | IMPLEMENTED | |
| 8 | Employee.Sum of BadHires | `sum_of_bad_hires` | IMPLEMENTED | |
| 9 | Employee.New Hires SPLY | `new_hires_sply` | TODO | `sql: NULL` — SAMEPERIODLASTYEAR |
| 10 | Employee.Actives SPLY | `actives_sply` | TODO | `sql: NULL` — SAMEPERIODLASTYEAR |
| 11 | Employee.Seps SPLY | `seps_sply` | TODO | `sql: NULL` — SAMEPERIODLASTYEAR |
| 12 | Employee.EmpCount SPLY | `emp_count_sply` | TODO | `sql: NULL` — period + SPLY |
| 13 | Employee.Seps YoY Var | `seps_yoy_var` | PARTIAL | Formula present; blocked by SPLY parent |
| 14 | Employee.Actives YoY Var | `actives_yoy_var` | PARTIAL | Formula present; blocked by SPLY parent |
| 15 | Employee.New Hires YoY Var | `new_hires_yoy_var` | PARTIAL | Formula present; blocked by SPLY parent |
| 16 | Employee.Seps YoY % Change | `seps_yoy_pct_change` | PARTIAL | Formula present; blocked by SPLY parent |
| 17 | Employee.Actives YoY % Change | `actives_yoy_pct_change` | PARTIAL | Formula present; blocked by SPLY parent |
| 18 | Employee.New Hires YoY % Change | `new_hires_yoy_pct_change` | PARTIAL | Formula present; blocked by SPLY parent |
| 19 | Employee.Bad Hires SPLY | `bad_hires_sply` | TODO | `sql: NULL` — SAMEPERIODLASTYEAR |
| 20 | Employee.Bad Hires YoY Var | `bad_hires_yoy_var` | PARTIAL | Formula present; blocked by SPLY parent |
| 21 | Employee.Bad Hires YoY % Change | `bad_hires_yoy_pct_change` | PARTIAL | Formula present; blocked by SPLY parent |
| 22 | Employee.TO % | `to_pct` | IMPLEMENTED | SAFE_DIVIDE seps/actives |
| 23 | Employee.TO % Norm | `to_pct_norm` | TODO | `sql: NULL` — ALL(Gender), ALL(Ethnicity) |
| 24 | Employee.TO % Var | `to_pct_var` | PARTIAL | Formula present; blocked by Norm parent |
| 25 | Employee.Sep%ofActive | `sep_pct_of_active` | IMPLEMENTED | |
| 26 | Employee.Sep%ofSMLYActives | `sep_pct_of_smly_actives` | PARTIAL | Depends on SPLY parents |
| 27 | Employee.BadHire%ofActives | `bad_hire_pct_of_actives` | IMPLEMENTED | |
| 28 | Employee.BadHire%ofActiveSPLY | `bad_hire_pct_of_active_sply` | PARTIAL | Depends on SPLY parents |
| 29 | BU.Count of BU | `count_of_bu` | IMPLEMENTED | `phase3/views/bu.view.lkml` |
| 30 | Date.Count of Date | `count_of_date` | IMPLEMENTED | `phase3/views/date.view.lkml` |

**Totals: IMPLEMENTED 11 · PARTIAL 12 · TODO 7** (of 30).

---

## 3. Joins present vs 8 relationships

| # | PBI relationship | LookML join | Status | `sql_on` |
| --- | --- | --- | --- | --- |
| 1 | Employee.date → Date.Date | `join: date` | PRESENT | `${employee.snapshot_date} = ${date.calendar_date}` |
| 2 | Employee.FP → FP.FP | `join: fp` | PRESENT | `${employee.fp} = ${fp.fp}` |
| 3 | Employee.EthnicGroup → Ethnicity.Ethnic Group | `join: ethnicity` | PRESENT | `${employee.ethnic_group} = ${ethnicity.ethnic_group}` |
| 4 | Employee.Gender → Gender.ID | `join: gender` | PRESENT | `${employee.gender_id} = ${gender.id}` |
| 5 | Employee.PayTypeID → PayType.PayTypeID | `join: pay_type` | PRESENT | `${employee.pay_type_id} = ${pay_type.pay_type_id}` |
| 6 | Employee.BU → BU.BU | `join: bu` | PRESENT | `${employee.bu} = ${bu.bu}` |
| 7 | Employee.AgeGroupID → AgeGroup.AgeGroupID | `join: age_group` | PRESENT | `${employee.age_group_id} = ${age_group.age_group_id}` |
| 8 | Employee.TermReason → SeparationReason.SeparationTypeID | `join: separation_reason` | PRESENT | `${employee.term_reason} = ${separation_reason.separation_type_id}` |

**Result: 8/8 PRESENT** in `phase3/models/human_resources.model.lkml` (`left_outer` / `many_to_one`).

---

## 4. Calc columns present vs 7 business calc columns

| # | PBI calculated column | LookML dimension | Status | Location |
| --- | --- | --- | --- | --- |
| 1 | BU.Region | `region` | PRESENT | `phase3/views/bu.view.lkml` (+ warehouse) |
| 2 | Date.MonthIncrementNumber | `month_increment_number` | PRESENT | `phase3/views/date.view.lkml` (+ warehouse) |
| 3 | Employee.isNewHire | `is_new_hire` | PRESENT | `phase3/views/employee.view.lkml` (+ warehouse) |
| 4 | Employee.AgeGroupID | `age_group_id` | PRESENT | `phase3/views/employee.view.lkml` (+ warehouse) |
| 5 | Employee.TenureDays | `tenure_days` | PRESENT | `phase3/views/employee.view.lkml` (+ warehouse) |
| 6 | Employee.TenureMonths | `tenure_months` | PRESENT | `phase3/views/employee.view.lkml` (+ warehouse) |
| 7 | Employee.BadHires | `bad_hires_flag` | PRESENT | `phase3/views/employee.view.lkml` (+ warehouse) |

**Result: 7/7 PRESENT.** Auto-date calc columns on LocalDateTable_* / DateTableTemplate_* correctly SKIP_INTERNAL.

---

## 5. RLS

| Item | Status | Notes |
| --- | --- | --- |
| Power BI RLS roles | N/A | NONE_IN_SOURCE (`LOOKML_MAPPING_ASSESSMENT.md` §9) |
| LookML access_grant / sql_always_where | N/A | No security mapping required from PBIX |

---

## NOTES (TODO only — no new LookML invented)

Critical gaps already stubbed in existing views/model; do not invent new views:

1. **TODO — EmpCount:** Implement latest-period `FILTER(ALL(Date[PeriodNumber]), PeriodNumber = MAX(...))` (not plain `count_distinct`).
2. **TODO — SPLY set:** `New Hires SPLY`, `Actives SPLY`, `Seps SPLY`, `EmpCount SPLY`, `Bad Hires SPLY` — replace `sql: NULL` with validated period-over-period / SAMEPERIODLASTYEAR equivalent.
3. **TODO — TO % Norm:** Ignore Gender + Ethnicity filter context (`ALL(Gender)`, `ALL(Ethnicity)`); then light up `TO % Var`.
4. **PARTIAL — Actives:** Revisit nesting vs EmpCount once EmpCount period logic exists.
5. **PARTIAL — YoY / % / SMLY dependents:** Formulas exist; unblock after SPLY/Norm parents.
6. **Ops (model):** Set `connection:` (currently `YOUR_LOOKER_CONNECTION`); enable datagroup `sql_trigger` after warehouse tables exist.
7. **Validation:** KPI parity vs Power BI not yet run — required before PASS.

---

## Coverage file

`phase3/IMPLEMENTATION_COVERAGE.md` reviewed against live LookML + inventory: **no refresh required** (paths under `phase3/`, measure/join/view statuses match this audit).

---

## Key TODO list (summary)

1. EmpCount (MAX PeriodNumber)
2. Five SPLY measures (NULL stubs)
3. TO % Norm (ALL Gender/Ethnicity)
4. Actives EmpCount-nesting parity
5. Unblock 12 PARTIAL dependents after parents
6. Looker connection + KPI parity validation

**Verdict: PARTIAL** (structure PASS; measures incomplete)
