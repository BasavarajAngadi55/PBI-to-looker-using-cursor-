# Power BI → Looker Migration Summary

**Source file:** `/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`  
**Report pages:** Info, New Hires, Actives and Separations, Bad Hires, New Hires Scorecard  
**Target:** LookML under `views/` and `models/`

---

## 1. Schema map

| Power BI table | Role | LookML view | PK | Notes |
|---|---|---|---|---|
| Employee | Fact | `employee` | composite (EmplID + date) | ~1.29M snapshot rows in PBIX |
| Date | Dim | `date` | Date | Custom calendar |
| BU | Dim | `bu` | BU | Region derived from RegionSeq |
| AgeGroup | Dim | `age_group` | AgeGroupID | `<30`, `30-49`, `50+` |
| Ethnicity | Dim | `ethnicity` | Ethnic Group | Codes 1–4 → Group A–D |
| FP | Dim | `fp` | FP | F/P |
| Gender | Dim | `gender` | ID | D=Male, C=Female in this sample |
| PayType | Dim | `pay_type` | PayTypeID | H/S |
| SeparationReason | Dim | `separation_reason` | SeparationTypeID | V/U |
| LocalDateTable_* / DateTableTemplate_* | Auto TI | *(skipped)* | — | Power BI auto date tables; not migrated |

---

## 2. Relationships → Looker joins

All PBIX relationships were **M:1**, active, single-direction cross-filter. Mapped as `left_outer` + `many_to_one`:

| From | Column | To | Column |
|---|---|---|---|
| Employee | date | Date | Date |
| Employee | BU | BU | BU |
| Employee | AgeGroupID | AgeGroup | AgeGroupID |
| Employee | EthnicGroup | Ethnicity | Ethnic Group |
| Employee | FP | FP | FP |
| Employee | Gender | Gender | ID |
| Employee | PayTypeID | PayType | PayTypeID |
| Employee | TermReason | SeparationReason | SeparationTypeID |

---

## 3. Measure conversion status

### Converted (ready / near-ready)

| DAX measure | LookML measure | Mapping |
|---|---|---|
| New Hires | `new_hires` | `type: sum` |
| Seps | `seps` | `count_distinct` + TermDate filter |
| Actives | `actives` | `count_distinct` + TermDate blank |
| AVG Tenure Days | `avg_tenure_days` | `type: average` |
| AVG Tenure Months | `avg_tenure_months` | number from avg days |
| AVG Age | `avg_age` | `type: average` |
| Sum of BadHires | `sum_of_bad_hires` | `type: sum` |
| Seps/Actives/New Hires/Bad Hires YoY Var & % | `*_yoy_*` | arithmetic on base + SPLY |
| TO %, Sep%ofActive, BadHire%ofActives | `to_pct`, `sep_pct_of_active`, `bad_hire_pct_of_actives` | `SAFE_DIVIDE` |
| Count of BU / Date | `count_of_bu`, `count_of_date` | `type: count` |

### Needs manual review (`# TODO` in LookML)

| DAX measure | Why |
|---|---|
| EmpCount | `FILTER(ALL(PeriodNumber), PeriodNumber = MAX(...))` — latest-period snapshot pattern |
| EmpCount SPLY | Same + `SAMEPERIODLASTYEAR` |
| New Hires / Actives / Seps / Bad Hires **SPLY** | `SAMEPERIODLASTYEAR` — implement via Looker PoP, date offset, or prior-year join |
| Dependent YoY % / Sep%ofSMLY / BadHire%ofActiveSPLY | Blocked until SPLY measures work |
| TO % Norm | `CALCULATE(..., ALL(Gender), ALL(Ethnicity))` — ignore specific dimensions |
| TO % Var | Depends on TO % Norm |

---

## 4. Calculated columns (DAX → LookML / warehouse)

| Table | Column | DAX | LookML treatment |
|---|---|---|---|
| Employee | isNewHire | year/month match hire | `dimension: is_new_hire` (SQL CASE) |
| Employee | AgeGroupID | age bands | `dimension: age_group_id` |
| Employee | TenureDays | abs date diff | `dimension: tenure_days` |
| Employee | TenureMonths | ceiling(days/30)-1 | `dimension: tenure_months` |
| Employee | BadHires | term within 60 days | `dimension: bad_hires_flag` |
| BU | Region | `MID(RegionSeq,3,15)` | `dimension: region` |
| Date | MonthIncrementNumber | `(Year-MIN(Year))*12+MonthNumber` | column passthrough + TODO |

Prefer **materializing** these in warehouse SQL for performance on large Employee snapshots.

---

## 5. Power Query (M) — do **not** translate to LookML

| Table | Source pattern | Warehouse / dbt action |
|---|---|---|
| Employee | Complex SQL against `IP.HR.AllEmps` + Date/BU/PayGroup/TermReason unions (actives + seps), gender remapped M→C/D, dates shifted +1 year | Rebuild as dbt model(s); largest ETL risk |
| BU, FP, PayType, SeparationReason, Date | `Sql.Database(".", "IP", ...)` | Point Looker `sql_table_name` at warehouse copies of these SQL extracts |
| Ethnicity, Gender, AgeGroup | Embedded `Table.FromRows(Binary.Decompress(...))` seed tables | Seed/CSV/dbt seed — small dims |

---

## 6. Output layout

```
views/
  employee.view.lkml
  date.view.lkml
  bu.view.lkml
  age_group.view.lkml
  ethnicity.view.lkml
  fp.view.lkml
  gender.view.lkml
  pay_type.view.lkml
  separation_reason.view.lkml
models/
  human_resources.model.lkml
pbix_analysis/          # extracted schema CSVs from pbixray
```

---

## 7. Next steps (LookML developer)

Follow [LOOKML_DEVELOPER_GUIDE.md](LOOKML_DEVELOPER_GUIDE.md) — **LookML first**, not warehouse DDL:

1. Set Looker `connection: "hr_bigquery"` (or your Admin connection name).  
2. Align `sql_table_name` to existing `hr.*` tables (escalate missing tables via [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md)).  
3. Validate explore joins; ship simple measures (Actives, Seps, New Hires, Bad Hires, TO %).  
4. Keep SPLY / EmpCount / TO % Norm as `# TODO` until patterns are implemented.  
5. Run KPI parity vs PBIX; auto date tables stay excluded from LookML.
