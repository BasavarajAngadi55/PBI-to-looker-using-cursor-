# LookML Developer Guide — HR Sample (Power BI → Looker)

**Audience:** Looker / LookML developers starting from zero on this migration.  
**Principle:** Build what you *can* now. When a blocker appears, **name it**, link the **M/DAX dependency**, and list **KPIs that wait**. Do not stop the whole project for one complex measure.

**Repo evidence:** inventory gate PASSED (15 tables, 30 measures, 9 M scripts, 8 joins).  
**Related docs:** [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) · [inventory/ACTION_MATRIX.csv](inventory/ACTION_MATRIX.csv) · [PROMPT.md](PROMPT.md)

> **No dbt.** Load BigQuery with SQL / seeds / PDTs.  
> **No report migration.** Semantic layer + Explores only.

**Built with specialist agents (then merged):**  
[Warehouse BQ](a32e0b09-fd29-4dea-97e8-139b6963863b) · [Views/joins](8b8c56c7-37bf-44ac-ba6b-055f46514117) · [Measures](95e9e0a1-2afb-4f79-9eb6-b75e8205f997) · [Day-by-day playbook](08687f2b-ad30-46ae-8b87-52d65f3920c2)

> Draft model still says `connection: "hr_warehouse"`. **Rename to `hr_bigquery`** (or your Admin connection name) when you wire Looker.

---

## How to use this guide

| Symbol | Meaning |
|--------|---------|
| **BUILD NOW** | Do this even if other things are blocked |
| **BLOCKER** | Stop *this* path; escalate or park with a `# TODO`; continue other paths |
| **UNLOCKS** | KPIs / features that start working after the blocker is cleared |

Follow phases **A → B → C → D**. Do not jump to SPLY measures before BigQuery tables exist.

---

## Phase A — Prerequisites (Day 0)

### A1. What you need

| Need | Why |
|------|-----|
| GCP project + BigQuery dataset (suggested: `hr`) | Physical tables Looker will query |
| Looker instance (or Looker Studio Connected Sheets is **not** enough — need LookML project) | Host LookML |
| Clone this repo | Inventory, draft views, M files, blockers |
| BigQuery connection credentials in Looker Admin | `connection:` in the model |

### A2. Read these files first (30–45 min)

1. [inventory/OBJECT_INVENTORY.md](inventory/OBJECT_INVENTORY.md) — what exists in PBIX  
2. [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) — M → KPI chains  
3. [models/human_resources.model.lkml](models/human_resources.model.lkml) — target explore  
4. [inventory/04_m_raw/Employee.m](inventory/04_m_raw/Employee.m) — biggest data dependency  

### A3. Mental model (star schema)

```text
                    ┌─ date
                    ├─ bu
                    ├─ age_group
 employee (FACT) ───┼─ ethnicity
                    ├─ fp
                    ├─ gender
                    ├─ pay_type
                    └─ separation_reason
```

Grain of `employee`: **one row per EmplID per month-end snapshot** (`date` is month grain).

---

## Phase B — BigQuery tables first (before LookML validates)

> **BUILD NOW:** Create all 9 business tables in BigQuery.  
> LookML files already exist as drafts, but Explores return errors until tables exist.

### B0. Suggested naming

| Looker connection name | BigQuery dataset | Example table |
|------------------------|------------------|---------------|
| `hr_bigquery` (rename from draft `hr_warehouse`) | `hr` | `your-project.hr.employee` |

In model file set:

```lookml
connection: "hr_bigquery"
```

In each view, `sql_table_name` like:

```lookml
sql_table_name: `your-project.hr.employee` ;;
# or after connection default dataset:
sql_table_name: `hr.employee` ;;
```

### B1. Load order (dims before fact)

| Order | BQ table | PBIX source | How to load | BLOCKER if missing |
|------:|----------|-------------|-------------|--------------------|
| 1 | `hr.age_group` | M seed `04_m_raw/AgeGroup.m` | Seed INSERT / CSV | Age-band joins & filters |
| 2 | `hr.gender` | M seed `Gender.m` | Seed (D=Male, C=Female) | Gender splits; TO % Norm |
| 3 | `hr.ethnicity` | M seed `Ethnicity.m` | Seed | Ethnicity splits; TO % Norm |
| 4 | `hr.fp` | M SQL `FP.m` | SQL or sample CSV | FP filters |
| 5 | `hr.pay_type` | M SQL `PayType.m` | SQL or sample CSV | Pay type filters |
| 6 | `hr.separation_reason` | M SQL `SeparationReason.m` | SQL or sample CSV | Separation reason charts |
| 7 | `hr.bu` | M SQL `BU.m` | SQL or sample CSV | Region / VP |
| 8 | `hr.date` | M SQL `Date.m` | SQL or sample CSV | **All time filters, SPLY, EmpCount** |
| 9 | `hr.employee` | M SQL `Employee.m` (**complex**) | Recreate SQL **or** load PBIX extract | **Almost every KPI** |

Sample column schemas / small CSVs: `pbix_analysis/table_*_sample.csv` and `table_*_schema.json`.

### B2. Seed SQL examples (BUILD NOW — tiny dims)

```sql
-- hr.age_group
CREATE TABLE `your-project.hr.age_group` AS
SELECT 1 AS AgeGroupID, '<30' AS AgeGroup UNION ALL
SELECT 2, '30-49' UNION ALL
SELECT 3, '50+';

-- hr.gender  (PBIX sample mapping: D=Male, C=Female)
CREATE TABLE `your-project.hr.gender` AS
SELECT 'D' AS ID, 'Male' AS Gender, 1 AS Sort UNION ALL
SELECT 'C', 'Female', 2;

-- hr.ethnicity (extend to all codes present in employee.EthnicGroup)
CREATE TABLE `your-project.hr.ethnicity` AS
SELECT '1' AS `Ethnic Group`, 'Group A' AS Ethnicity UNION ALL
SELECT '2', 'Group B' UNION ALL
SELECT '3', 'Group C' UNION ALL
SELECT '4', 'Group D';
```

### B3. Employee table — critical BLOCKER

```text
BLOCKER: hr.employee not loaded
  └── depends on: inventory/04_m_raw/Employee.m
  └── UNLOCKS: Actives, Seps, New Hires, Bad Hires, tenure, TO %, all YoY/SPLY
  └── HOW:
        Option A) Recreate M SQL in BigQuery (UNION actives + seps; see Employee.m)
        Option B) Export Employee from PBIX / use large extract into BQ
        Option C) Temporary: load pbix_analysis sample only for LookML syntax testing (NOT for parity)
```

**Required columns on `hr.employee`:**

| Column | Type (logical) | Notes |
|--------|----------------|-------|
| date | DATE/TIMESTAMP | Snapshot month key → joins `hr.date` |
| EmplID | INT64 | Employee id |
| Gender | STRING | Join key to `gender.ID` (C/D) |
| Age | INT64 | |
| EthnicGroup | STRING | Join to ethnicity.`Ethnic Group` |
| FP | STRING | F/P |
| TermDate | DATE (nullable) | NULL = active |
| BU | STRING | |
| HireDate | DATE | |
| PayTypeID | STRING | H/S |
| TermReason | STRING | V/U when separated |
| isNewHire | INT64 | Calc — see below |
| AgeGroupID | INT64 | Calc — 1/2/3 |
| TenureDays | FLOAT64 | Calc |
| TenureMonths | INT64 | Calc |
| BadHires | FLOAT64/INT64 | Calc |

### B4. Calculated columns — BUILD in BQ **or** LookML

| Column | Logic (from DAX) | Prefer |
|--------|------------------|--------|
| `isNewHire` | snapshot year/month = hire year/month → 1 | BQ column **or** LookML dim (draft exists) |
| `AgeGroupID` | Age&lt;30→1; &lt;50→2; else 3 | BQ **or** LookML |
| `TenureDays` | abs(date − HireDate) | BQ **or** LookML |
| `TenureMonths` | CEILING(TenureDays/30)−1 | BQ **or** LookML |
| `BadHires` | term within 60 days of hire → 1 else 0 | BQ **or** LookML |
| `BU.Region` | SUBSTR(RegionSeq, 3) | BQ **or** LookML |
| `Date.MonthIncrementNumber` | months since min year | BQ preferred |

```text
BLOCKER EXAMPLE:
  New Hires measure needs isNewHire
    └── needs hr.employee (+ calc column or LookML dim)
          └── needs Employee.m load
```

### B5. Validate in BigQuery before Looker

```sql
SELECT COUNT(*) FROM `your-project.hr.employee`;
SELECT COUNT(*) FROM `your-project.hr.date`;
-- Join sanity
SELECT COUNT(*) 
FROM `your-project.hr.employee` e
LEFT JOIN `your-project.hr.gender` g ON e.Gender = g.ID
WHERE g.ID IS NULL;  -- should be 0 after clean load
```

---

## Phase C — Looker connection & project setup

### C1. Admin: create BigQuery connection

In Looker **Admin → Connections → Add Connection**:

| Setting | Suggested value |
|---------|-----------------|
| Name | `hr_bigquery` |
| Dialect | BigQuery Standard SQL |
| Project / Dataset | your GCP project; optional default dataset `hr` |
| Auth | Service account JSON with BQ Data Viewer (+ Job User) |

**BUILD NOW:** Connection can be created as soon as *any* table exists (even seeds).

```text
BLOCKER: Connection test fails
  └── usually IAM / wrong project / billing
  └── UNLOCKS: nothing in Looker validates until green
  └── HOW: fix GCP IAM; retest connection
```

### C2. LookML project layout (match this repo)

```text
your-lookml-project/
  models/
    human_resources.model.lkml
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
```

**BUILD NOW:** Copy draft files from this repo into your LookML project (IDE or Git integration).

### C3. Wire connection + includes

Edit `models/human_resources.model.lkml`:

```lookml
connection: "hr_bigquery"   # was hr_warehouse in draft — change to your Admin connection name

include: "/views/*.view.lkml"
```

Update every view `sql_table_name` to your project.dataset.table.

```text
BLOCKER mid-build: LookML validates but Explore says "table not found"
  └── sql_table_name / dataset / connection mismatch
  └── HOW: bq ls your-project:hr  and align names exactly
```

---

## Phase D — Views then joins (BUILD ORDER)

### D1. Build dimension views first

| # | File | sql_table_name | PK dimension |
|---|------|----------------|--------------|
| 1 | `age_group.view.lkml` | `hr.age_group` | `age_group_id` |
| 2 | `gender.view.lkml` | `hr.gender` | `id` |
| 3 | `ethnicity.view.lkml` | `hr.ethnicity` | `ethnic_group` (column `` `Ethnic Group` ``) |
| 4 | `fp.view.lkml` | `hr.fp` | `fp` |
| 5 | `pay_type.view.lkml` | `hr.pay_type` | `pay_type_id` |
| 6 | `separation_reason.view.lkml` | `hr.separation_reason` | `separation_type_id` |
| 7 | `bu.view.lkml` | `hr.bu` | `bu` (+ `region`) |
| 8 | `date.view.lkml` | `hr.date` | `calendar_date` / Date |

**BUILD NOW** even if Employee is still loading — you can Explore dims alone for QA.

### D2. Build fact view

| File | Notes |
|------|-------|
| `employee.view.lkml` | Dimensions + measures; draft already has calc dims and measure stubs |

### D3. Explore joins (exact mapping from PBIX)

Use existing explore in `human_resources.model.lkml`:

| Join | sql_on | type | relationship |
|------|--------|------|--------------|
| date | `${employee.snapshot_date} = ${date.calendar_date}` | left_outer | many_to_one |
| bu | `${employee.bu} = ${bu.bu}` | left_outer | many_to_one |
| age_group | `${employee.age_group_id} = ${age_group.age_group_id}` | left_outer | many_to_one |
| ethnicity | `${employee.ethnic_group} = ${ethnicity.ethnic_group}` | left_outer | many_to_one |
| fp | `${employee.fp} = ${fp.fp}` | left_outer | many_to_one |
| gender | `${employee.gender_id} = ${gender.id}` | left_outer | many_to_one |
| pay_type | `${employee.pay_type_id} = ${pay_type.pay_type_id}` | left_outer | many_to_one |
| separation_reason | `${employee.term_reason} = ${separation_reason.separation_type_id}` | left_outer | many_to_one |

```text
BLOCKER: Join returns null labels (e.g. Gender blank)
  └── often C/D vs M/F mismatch, or Ethnic Group type/spacing
  └── HOW: SELECT DISTINCT Gender FROM hr.employee; compare to gender.ID
```

---

## Phase E — Measures: what to build vs what to park

### E1. BUILD NOW (after `hr.employee` exists) — Phase E “Simple”

Implement / verify these first (draft names in `employee.view.lkml`):

| Business KPI | LookML measure (draft) | Logic |
|--------------|------------------------|-------|
| Separations | `seps` | count distinct EmplID where TermDate not null |
| Actives | `actives` | count distinct EmplID where TermDate null |
| New Hires | `new_hires` | sum of `is_new_hire` |
| Sum of BadHires | `sum_of_bad_hires` | sum of `bad_hires_flag` |
| AVG Age | `avg_age` | average Age |
| AVG Tenure Days/Months | `avg_tenure_*` | average tenure dims |
| TO % | `to_pct` | seps / actives |
| Sep%ofActive | `sep_pct_of_active` | same pattern |
| BadHire%ofActives | `bad_hire_pct_of_actives` | bad hires / actives |
| Count of BU / Date | on dim views | type: count |

**Definition of done (Phase E Simple):** Explore returns non-null Actives, Seps, New Hires for a known month filter.

### E2. PARK with visible BLOCKERS — do not fake numbers

Keep measures in LookML but mark clearly:

```lookml
measure: new_hires_sply {
  label: "New Hires SPLY"
  description: "BLOCKED: needs SAMEPERIODLASTYEAR pattern. See BLOCKERS §5."
  # TODO: CALCULATE([New Hires], SAMEPERIODLASTYEAR('Date'[Date]))
  type: number
  sql: NULL ;;
}
```

| KPI | Why blocked | Dependency chain | How to achieve later |
|-----|-------------|------------------|----------------------|
| **New Hires SPLY** | `SAMEPERIODLASTYEAR` | Employee.m → isNewHire → New Hires → SPLY | Looker PoP / prior-year join |
| **Actives SPLY** | same | Employee + TermDate blank → SPLY | same |
| **Seps SPLY** | same | TermDate set → SPLY | same |
| **Bad Hires SPLY** | same | BadHires → SPLY | same |
| **EmpCount** | MAX(PeriodNumber) | Date.m → PeriodNumber → EmpCount | always_filter latest period or SQL max period |
| **EmpCount SPLY** | EmpCount + SPLY | both above | both patterns |
| **TO % Norm** | ALL(Gender/Ethnicity) | dims + TO% | measure ignoring those filters |
| **BadHire%ofActiveSPLY** | needs two SPLYs | Bad Hires SPLY / Actives SPLY | after SPLY works |
| **All YoY Var / %** | arithmetic on SPLY | parent KPI − SPLY | after SPLY works |
| **Sep%ofSMLYActives** | SPLY ratio | Seps SPLY / Actives SPLY | after SPLY works |
| **TO % Var** | needs TO % Norm | TO% − Norm | after Norm works |

### E3. Mid-build blocker protocol (required)

When you hit a blocker mid-sprint:

1. **Do not delete** the measure — keep name for mapping traceability.  
2. Add `# TODO:` with **exact DAX** from `inventory/02_dax_objects.json`.  
3. Add one line to a tracker (or extend BLOCKERS doc):

```text
DATE | MEASURE | BLOCKED_ON | UNLOCKS | OWNER | STATUS
```

4. Continue with next **BUILD NOW** item (dims, simple measures, Explore UX).

---

## Phase F — First Explore smoke test

1. Open Explore **Human Resources** (`employee`).  
2. Filters: one Year or Month from `date`.  
3. Measures: Actives, Seps, New Hires.  
4. Pivot: `gender.gender`, `age_group.age_group`, `bu.region`.  

| Result | Action |
|--------|--------|
| Numbers look plausible | Proceed to KPI parity checklist |
| Zeros everywhere | BLOCKER: table empty / wrong filter / isNewHire all null |
| Join fanout / huge counts | BLOCKER: grain wrong (duplicate snapshot rows) |

---

## Phase G — KPI parity (after simple measures work)

Compare Power BI vs Looker (same filters). Mark PASS/FAIL — never invent PASS.

| # | Check | Power BI | Looker | Status |
|---|-------|----------|--------|--------|
| 1 | Actives (all / latest month) | | | PENDING |
| 2 | Seps (same) | | | PENDING |
| 3 | New Hires (same) | | | PENDING |
| 4 | Sum of BadHires | | | PENDING |
| 5 | Actives by Region | | | PENDING |
| 6 | Actives by Gender | | | PENDING |
| 7 | Actives by AgeGroup | | | PENDING |
| 8 | New Hires by Month | | | PENDING |
| 9 | Seps by SeparationReason | | | PENDING |
| 10 | TO % | | | PENDING |
| 11 | BadHire%ofActives | | | PENDING |
| 12 | AVG Age | | | PENDING |
| 13–15 | SPLY / YoY / EmpCount | | | **BLOCKED until Phase E2** |

---

## Phase H — Complex time intelligence (only after G 1–12)

Order:

1. Implement one SPLY pattern (recommend **New Hires SPLY**) end-to-end.  
2. Clone pattern to Actives / Seps / Bad Hires SPLY.  
3. Turn on YoY Var / % measures (already drafted as arithmetic).  
4. EmpCount max-period logic (+ revisit Actives if PBIX used EmpCount inside Actives).  
5. TO % Norm / Var.  
6. Re-run parity rows 13–15.

---

## Quick reference — files to open while coding

| Task | Open |
|------|------|
| Column list / types | `inventory/01_tables_columns.json` |
| Full DAX text | `inventory/02_dax_objects.json` |
| Joins | `inventory/03_relationships.json` + `models/human_resources.model.lkml` |
| M / SQL source | `inventory/04_m_raw/*.m` |
| What to build vs skip | `inventory/ACTION_MATRIX.csv` |
| Blocker chains | `BLOCKERS_AND_DEPENDENCIES.md` |
| Draft LookML | `views/*.view.lkml` |

---

## Common mistakes

1. **Starting LookML Explores before `hr.employee` exists** — validate connection with dims first, but don’t promise KPIs.  
2. **Treating Gender as M/F** — this sample uses **D/C** codes.  
3. **Skipping Employee.m complexity** — without UNION actives+seps logic, Seps/Actives are wrong.  
4. **Building SPLY first** — wastes time; unblock warehouse + simple measures first.  
5. **Ignoring internal LocalDateTable_*** — captured in inventory; **do not** require them in Looker; use `hr.date` + `dimension_group`.  
6. **Silent NULL measures** — always `# TODO` + blocker tracker entry.

---

## One-page “start Monday morning” checklist

- [ ] Clone repo; skim BLOCKERS + OBJECT_INVENTORY  
- [ ] Create BQ dataset `hr`  
- [ ] Load 3 seeds (age_group, gender, ethnicity)  
- [ ] Load dim SQL tables (fp, pay_type, separation_reason, bu, date)  
- [ ] Load **employee** (or escalate BLOCKER with Employee.m attached)  
- [ ] Create Looker connection `hr_bigquery`  
- [ ] Copy views/ + model; fix `connection` + `sql_table_name`  
- [ ] Validate Explore joins on Gender / Region / AgeGroup  
- [ ] Ship simple measures (Actives, Seps, New Hires, Bad Hires, TO %)  
- [ ] Park SPLY/EmpCount/TO% Norm with `# TODO` + tracker  
- [ ] Run parity rows 1–12  
- [ ] Only then schedule Phase H complex TI  

---

## Summary for the developer

You are not blocked from **starting**. You *are* blocked from **finishing every KPI** until:

1. BigQuery has the nine tables (especially **employee** from **Employee.m**), and  
2. Looker time-intelligence patterns replace `SAMEPERIODLASTYEAR` / max-period EmpCount / TO % Norm.

**Start at BigQuery → connection → dim views → fact → joins → simple measures.**  
Highlight every mid-build blocker with the M/DAX chain so data engineers know exactly what to deliver next.

---

## Appendix A — BigQuery type map & load options (per table)

| Extract dtype | BigQuery |
|---------------|----------|
| `string` | `STRING` |
| `Int64` | `INT64` |
| `Float64` | `FLOAT64` |
| `datetime64[ns]` | `DATE` (preferred for this sample) |

| Option | When to use |
|--------|-------------|
| **A. Recreate SQL from `.m`** | Source `IP`/`HR.*` available; best for Employee/Date/BU |
| **B. Full PBIX export → BQ load** | No live SQL Server; best for parity |
| **C. `pbix_analysis/table_*_sample.csv`** | Smoke tests only (samples truncated — **not** KPI parity) |
| **D. Seed INSERT** | Ethnicity, Gender, AgeGroup (embedded M) |

### Ethnicity seed (all 7 groups from extract)

```sql
INSERT INTO `hr.ethnicity` (`Ethnic Group`, Ethnicity) VALUES
 ('1','Group A'),('2','Group B'),('3','Group C'),('4','Group D'),
 ('5','Group E'),('6','Group F'),('7','Group G');
```

### Temporary datagroup note

Until `hr.employee` exists, the model datagroup trigger will fail:

```lookml
sql_trigger: SELECT MAX(date) FROM `hr.employee` ;;
```

**BUILD NOW:** Comment out `persist_with` / datagroup while scaffolding; re-enable after Employee loads.

---

## Appendix B — LookML ↔ warehouse join field cheat sheet

| LookML field | Warehouse column | Join |
|--------------|------------------|------|
| `employee.snapshot_date` | `date` | → `date.calendar_date` (`Date`) |
| `employee.bu` | `BU` | → `bu.bu` |
| `employee.age_group_id` | derived CASE on `Age` **or** physical `AgeGroupID` | → `age_group.age_group_id` |
| `employee.ethnic_group` | `EthnicGroup` | → `ethnicity.ethnic_group` (`` `Ethnic Group` ``) |
| `employee.fp` | `FP` | → `fp.fp` |
| `employee.gender_id` | `Gender` (C/D codes) | → `gender.id` |
| `employee.pay_type_id` | `PayTypeID` | → `pay_type.pay_type_id` |
| `employee.term_reason` | `TermReason` | → `separation_reason.separation_type_id` |

**Missing-table blockers (Explore run fails):**

| ID | Missing table | Impact |
|----|---------------|--------|
| B1 | `hr.employee` | Primary explore + datagroup + all fact KPIs |
| B2 | `hr.date` | Time filters, SPLY, EmpCount |
| B3 | `hr.bu` | Region/VP |
| B4–B9 | seed/SQL dims | Labels for age/gender/ethnicity/fp/pay/sep |

**Unblock order:** seeds (B4–B9) → date + bu → **employee**.

---

## Appendix C — Measure build order (exact)

### Ship first (after tables)

| # | DAX | LookML | Depends on |
|--:|-----|--------|------------|
| 1 | Seps | `seps` | TermDate |
| 2 | Actives | `actives` | TermDate *(PBIX uses EmpCount — parity risk)* |
| 3 | New Hires | `new_hires` | `is_new_hire` |
| 4 | Sum of BadHires | `sum_of_bad_hires` | `bad_hires_flag` |
| 5–7 | AVG Tenure / Age | `avg_tenure_*`, `avg_age` | tenure / Age |
| 8–10 | TO %, Sep%ofActive, BadHire%ofActives | `to_pct`, … | seps/actives/bad |
| 11–12 | Count of BU / Date | on dim views | dims |

### Defer (stub + tracker)

| Bucket | Measures | LookML names |
|--------|----------|--------------|
| EmpCount / period | EmpCount, EmpCount SPLY | `emp_count`, `emp_count_sply` |
| SPLY | New/Actives/Seps/Bad Hires SPLY | `*_sply` |
| TO % Norm | TO % Norm | `to_pct_norm` |
| Parent-blocked YoY | all YoY Var/%, Sep%ofSMLY*, BadHire%ofActiveSPLY, TO % Var | keep formulas; hide until parents work |

### Tracker columns (copy for Jira/sheet)

`DATE | DAX | LookML | BLOCKERS | M files | Column deps | Parents | STATUS | OWNER | UNBLOCK`

### Stub pattern

```lookml
measure: new_hires_sply {
  group_label: "Blocked — TODO"
  description: "BLOCKED until SAMEPERIODLASTYEAR / PoP. See BLOCKERS §5."
  # TODO: CALCULATE([New Hires], SAMEPERIODLASTYEAR('Date'[Date]))
  type: number
  sql: NULL ;;
}
```

---

## Appendix D — Day-by-day calendar

| Day | Focus | BUILD THIS | If BLOCKED |
|-----|-------|------------|------------|
| 0 | Access | Clone repo; read gate + Blockers 1–3; confirm BQ + Looker connection names | Escalate platform; do not fake Explore “done” |
| 1 | Dim SQL + seeds | Date, BU, FP, PayType, SeparationReason + AgeGroup/Gender/Ethnicity | Export extracts if SQL Server unreachable |
| 2–3 | Employee fact | Port `Employee.m`; materialize calc columns; keep Gender **C/D** | Escalate Blocker 1 — do not only edit LookML |
| 4 | First Explore | Wire `hr_bigquery`; validate 8 joins; smoke Month×Region×Gender | Fix warehouse names before join cosmetics |
| 5–6 | Simple measures | Section “Ship first” above | Leave SPLY/YoY as TODO |
| 7+ | Complex TI | One SPLY end-to-end → clone → YoY → EmpCount → TO % Norm | Second parity pass after |
| Later | Parity | Checklist rows 1–12 then 13–15 | Never invent PASS |

### Phase A done when

1. Nine BQ tables queryable from Looker  
2. Calc columns available (SQL or LookML)  
3. Explore + 8 joins returns rows  
4. Simple measures non-null on Gender/Region cuts  
5. Blockers 1–4 closed or honestly partial  
6. SPLY/EmpCount/TO% Norm **not** falsely claimed done  

### Phase B done when

SPLY spot-checks match a PBIX month; YoY wired off SPLY; EmpCount max-period documented; TO % Norm ignores Gender/Ethnicity; complex matrix rows updated.

---

## Appendix E — Common mistakes (from playbook agent)

1. Skipping `Employee.m` → 0% runnable KPIs  
2. Normalizing Gender to M/F while seed stays C/D → broken joins  
3. Building LookML for `LocalDateTable_*` — use business `Date` only  
4. YoY before SPLY / before `isNewHire`  
5. Equating LookML Actives with PBIX EmpCount/Actives without max period  
6. Reading `DBT_*` tags as “must use dbt” — means warehouse SQL here  
7. Inventing joins without `03_relationships.json`  
8. Calling inventory gate “KPI ready”

---

## Appendix F — Agent deliverable map

| Section need | Agent |
|--------------|-------|
| BQ tables, seeds, blockers per table | [Warehouse BQ](a32e0b09-fd29-4dea-97e8-139b6963863b) |
| Project layout, connection, joins, build-without-data | [Views/joins](8b8c56c7-37bf-44ac-ba6b-055f46514117) |
| Measure order, stubs, parity checklist | [Measures](95e9e0a1-2afb-4f79-9eb6-b75e8205f997) |
| Day-by-day + Phase A/B DoD | [Day-by-day playbook](08687f2b-ad30-46ae-8b87-52d65f3920c2) |
