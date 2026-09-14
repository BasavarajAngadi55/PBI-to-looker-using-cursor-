# LookML Developer Guide — HR Sample (Power BI → Looker)

**Audience:** Looker / LookML developers.  
**Scope of this guide:** Build and ship **LookML** from the prior PBIX conversion.  
**Out of scope here:** Creating BigQuery / warehouse tables, dbt, and report/dashboard migration.

**Principle:** Start with the LookML already drafted in this repo. Ship what validates today. When a blocker appears, **name it**, link the **M/DAX dependency**, and list **KPIs that wait** — then continue other LookML work.

**Prior conversion (already done):** inventory gate PASSED · draft views · model explore · measure stubs.  
**Related docs:** [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) · [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md) · [inventory/ACTION_MATRIX.csv](inventory/ACTION_MATRIX.csv) · [PROMPT.md](PROMPT.md)

> Warehouse tables (`hr.*`) are assumed to be provided by a data engineer (or already exist).  
> If a table is missing, **do not** stop to invent DDL in this guide — escalate using [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) and keep coding LookML against the draft `sql_table_name`s.

---

## How to use this guide

| Symbol | Meaning |
|--------|---------|
| **BUILD NOW** | Do this in LookML even if other KPIs are blocked |
| **BLOCKER** | Stop *this* path; leave `# TODO`; continue other LookML |
| **UNLOCKS** | Features that work after the blocker clears |

Follow phases **1 → 6**. Do not jump to SPLY before simple measures compile and Explore joins work.

---

## Phase 0 — What previous conversion already gave you

You are **not** starting from a blank LookML project. Use these artifacts:

| Artifact | Path | Your use |
|----------|------|----------|
| Draft fact + dims | `views/*.view.lkml` | Edit labels, SQL, measures — do not recreate from scratch |
| Explore + joins | `models/human_resources.model.lkml` | Wire `connection`; keep join map |
| Full DAX text | `inventory/02_dax_objects.json` | Source of truth for measure logic / TODOs |
| Relationships | `inventory/03_relationships.json` | Validate every `sql_on` |
| M / Power Query | `inventory/04_m_raw/*.m` | Escalate warehouse gaps (not LookML rewrite) |
| Action backlog | `inventory/ACTION_MATRIX.csv` | What is LOOKML vs WAREHOUSE vs SKIP |
| Blocker chains | `BLOCKERS_AND_DEPENDENCIES.md` | Mid-build escalation language |

### Star schema (target Explore)

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

### Mental model: LookML vs warehouse

```text
PBIX inventory ──► LookML (this guide) ──► Explore KPIs
                      ▲
                      │ sql_table_name points at
                      │
               Warehouse hr.* tables
               (owned elsewhere — see BLOCKERS if missing)
```

---

## Phase 1 — Read before you type (45 min)

**BUILD NOW** — no warehouse required.

1. [inventory/OBJECT_INVENTORY.md](inventory/OBJECT_INVENTORY.md) — what exists in PBIX  
2. [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md) — schema map + measure conversion status  
3. [models/human_resources.model.lkml](models/human_resources.model.lkml) — explore joins  
4. [views/employee.view.lkml](views/employee.view.lkml) — calc dims + measures + `# TODO`s  
5. [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) — what you escalate vs what you code  

**Skip for LookML work:** writing `CREATE TABLE` / seed INSERT scripts. That is warehouse ownership.

---

## Phase 2 — Looker project + connection

### 2.1 Project layout (already in repo)

```text
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

**BUILD NOW:** Copy these into your LookML project (Git sync or Looker IDE). Prefer editing in place in this repo.

### 2.2 Set the connection

In Looker **Admin → Connections**, note the existing BigQuery (or warehouse) connection name your org uses.

Edit the model:

```lookml
connection: "hr_bigquery"   # replace with YOUR Admin connection name
include: "/views/*.view.lkml"
```

Draft currently says `connection: "hr_warehouse"` — rename to match Admin.

### 2.3 Align `sql_table_name`

Each view already points at schema `hr`:

```lookml
sql_table_name: `hr.employee` ;;
```

If your dataset/project differs, update **all nine** views consistently (or set a connection default dataset and keep short names).

```text
BLOCKER mid-build: LookML validates but Explore says "table not found"
  └── depends on: warehouse table missing or name mismatch
  └── UNLOCKS: runnable Explores
  └── HOW: escalate to warehouse with BLOCKERS §1–3 + exact table name;
           do NOT invent BQ DDL as part of LookML sprint unless asked
```

### 2.4 Datagroup while scaffolding

```lookml
datagroup: human_resources_default_datagroup {
  sql_trigger: SELECT MAX(date) FROM `hr.employee` ;;
  max_cache_age: "24 hours"
}
```

If `hr.employee` is not ready yet, temporarily comment out `persist_with` / datagroup so LookML still validates. Re-enable when the fact table exists.

---

## Phase 3 — Dimension views first (BUILD NOW)

Open each dim view; confirm PK and labels match inventory. Do **not** recreate LocalDateTable_* — use business `date` only.

| # | File | PK field | Notes from conversion |
|---|------|----------|------------------------|
| 1 | `age_group.view.lkml` | `age_group_id` | `<30`, `30-49`, `50+` |
| 2 | `gender.view.lkml` | `id` | Sample codes **D=Male, C=Female** (not M/F) |
| 3 | `ethnicity.view.lkml` | `ethnic_group` | Column `` `Ethnic Group` `` in warehouse |
| 4 | `fp.view.lkml` | `fp` | F/P |
| 5 | `pay_type.view.lkml` | `pay_type_id` | H/S |
| 6 | `separation_reason.view.lkml` | `separation_type_id` | V/U |
| 7 | `bu.view.lkml` | `bu` | `region` from `RegionSeq` (LookML or column) |
| 8 | `date.view.lkml` | `calendar_date` | `period_number` needed later for EmpCount |

**Definition of done:** LookML validates; optional hidden explores `date` / `bu` open without syntax errors.

---

## Phase 4 — Fact view + calculated columns (already in LookML)

File: `views/employee.view.lkml`

Calc columns from DAX are already expressed as LookML dimensions (prefer warehouse materialization later for performance — **not required to start**):

| DAX column | LookML dimension | Logic |
|------------|------------------|-------|
| isNewHire | `is_new_hire` | snapshot year/month = hire year/month |
| AgeGroupID | `age_group_id` | Age bands 1/2/3 |
| TenureDays | `tenure_days` | abs day diff |
| TenureMonths | `tenure_months` | CEILING(days/30)−1 |
| BadHires | `bad_hires_flag` | term within 60 days of hire |

```text
BLOCKER: is_new_hire always null / New Hires = 0
  └── depends on: HireDate + date populated correctly (Employee.m grain)
  └── UNLOCKS: new_hires, New Hires YoY/SPLY
  └── HOW: warehouse fix for Employee load — LookML CASE is already written
```

---

## Phase 5 — Explore joins (map from PBIX)

All PBIX relationships were **M:1**, active, single-direction. Model uses `left_outer` + `many_to_one`:

| Join | `sql_on` |
|------|----------|
| date | `${employee.snapshot_date} = ${date.calendar_date}` |
| bu | `${employee.bu} = ${bu.bu}` |
| age_group | `${employee.age_group_id} = ${age_group.age_group_id}` |
| ethnicity | `${employee.ethnic_group} = ${ethnicity.ethnic_group}` |
| fp | `${employee.fp} = ${fp.fp}` |
| gender | `${employee.gender_id} = ${gender.id}` |
| pay_type | `${employee.pay_type_id} = ${pay_type.pay_type_id}` |
| separation_reason | `${employee.term_reason} = ${separation_reason.separation_type_id}` |

Source of truth: `inventory/03_relationships.json`.

```text
BLOCKER: Join returns blank Gender / Ethnicity labels
  └── often C/D vs M/F mismatch, or Ethnic Group spacing/type
  └── HOW: compare DISTINCT employee.Gender to gender.ID — warehouse seed fix
```

**Smoke test (BUILD NOW when tables exist):**  
Explore **Human Resources** → one Month filter → pivot `gender.gender`, `bu.region`, `age_group.age_group`.

---

## Phase 6 — Measures: ship simple, park complex

All 30 PBIX measures are named in LookML (`employee.view.lkml` + dim counts). Use this order.

### 6.1 BUILD NOW — simple KPIs

| DAX | LookML | Pattern |
|-----|--------|---------|
| Seps | `seps` | count_distinct EmplID where TermDate not null |
| Actives | `actives` | count_distinct where TermDate null |
| New Hires | `new_hires` | sum `is_new_hire` |
| Sum of BadHires | `sum_of_bad_hires` | sum `bad_hires_flag` |
| AVG Tenure Days / Months | `avg_tenure_*` | average / derived |
| AVG Age | `avg_age` | average Age |
| TO % | `to_pct` | SAFE_DIVIDE(seps, actives) |
| Sep%ofActive | `sep_pct_of_active` | same as TO % |
| BadHire%ofActives | `bad_hire_pct_of_actives` | bad / actives |
| Count of BU / Date | `count_of_bu`, `count_of_date` | type: count on dims |

**Definition of done:** Explore returns non-null Actives, Seps, New Hires for a known month.

> **Parity note:** PBIX `Actives` wraps `EmpCount` (max PeriodNumber). Our `actives` is TermDate-blank distinct count. Document gap until EmpCount filter is implemented.

### 6.2 PARK — keep stubs with `# TODO` (do not fake numbers)

| KPI | Why blocked | Dependency | How later |
|-----|-------------|------------|-----------|
| **New/Actives/Seps/Bad Hires SPLY** | `SAMEPERIODLASTYEAR` | simple KPI + date | Looker PoP / prior-year join |
| **EmpCount** | `FILTER(ALL(PeriodNumber)=MAX(...))` | `date.period_number` | always_filter / liquid / SQL |
| **EmpCount SPLY** | EmpCount + SPLY | both | both patterns |
| **TO % Norm** | `ALL(Gender), ALL(Ethnicity)` | TO % | filtered measure / PDT ignore dims |
| **TO % Var** | needs Norm | TO % Norm | after Norm |
| **All YoY Var / %** | arithmetic on SPLY | `*_sply` | formulas already drafted — light up when SPLY works |
| **Sep%ofSMLY* / BadHire%ofActiveSPLY** | SPLY ratios | SPLY parents | after SPLY |

Stub pattern already in repo:

```lookml
measure: new_hires_sply {
  group_label: "Blocked — TODO"
  label: "New Hires SPLY"
  description: "BLOCKED: SAMEPERIODLASTYEAR. See BLOCKERS."
  # TODO: CALCULATE([New Hires], SAMEPERIODLASTYEAR('Date'[Date]))
  type: number
  sql: NULL ;;
}
```

### 6.3 Mid-build blocker protocol

1. **Do not delete** the measure — keep the DAX name for traceability.  
2. `# TODO:` with **exact DAX** from `inventory/02_dax_objects.json`.  
3. Log one line: `DATE | MEASURE | BLOCKED_ON | UNLOCKS | OWNER | STATUS`  
4. Continue next **BUILD NOW** item.

---

## Phase 7 — KPI parity (after simple measures)

Compare Power BI vs Looker with the **same filters**. Never invent PASS.

| # | Check | Status |
|---|-------|--------|
| 1 | Actives (latest month) | PENDING |
| 2 | Seps | PENDING |
| 3 | New Hires | PENDING |
| 4 | Sum of BadHires | PENDING |
| 5–7 | Actives by Region / Gender / AgeGroup | PENDING |
| 8 | New Hires by Month | PENDING |
| 9 | Seps by SeparationReason | PENDING |
| 10–11 | TO % / BadHire%ofActives | PENDING |
| 12 | AVG Age | PENDING |
| 13–15 | SPLY / YoY / EmpCount | **BLOCKED until Phase 6.2 cleared** |

---

## Phase 8 — Complex time intelligence (only after 1–12)

1. Implement **one** SPLY end-to-end (recommend New Hires SPLY).  
2. Clone to Actives / Seps / Bad Hires SPLY.  
3. Enable YoY Var / % (arithmetic already in LookML).  
4. EmpCount max-period (+ revisit Actives if needed for parity).  
5. TO % Norm / Var.  
6. Re-run parity rows 13–15.

---

## Quick reference — files while coding LookML

| Task | Open |
|------|------|
| Draft LookML | `views/*.view.lkml`, `models/human_resources.model.lkml` |
| Full DAX | `inventory/02_dax_objects.json` |
| Joins | `inventory/03_relationships.json` |
| Columns / types | `inventory/01_tables_columns.json` |
| What to build vs skip | `inventory/ACTION_MATRIX.csv` |
| Warehouse / M escalations | `inventory/04_m_raw/*.m` + `BLOCKERS_AND_DEPENDENCIES.md` |
| Conversion status | `MIGRATION_SUMMARY.md` |

---

## Common mistakes (LookML-focused)

1. **Rewriting views from scratch** — prior conversion already mapped schema, joins, and 30 measures.  
2. **Treating Gender as M/F** — this sample uses **D/C**.  
3. **Building LookML for LocalDateTable_*** — captured in inventory; SKIP for Looker; use `date`.  
4. **Starting with SPLY** — ship simple measures first.  
5. **Silent NULL measures** — always `# TODO` + blocker log.  
6. **Assuming Actives = PBIX EmpCount/Actives** — document max-period gap.  
7. **Stopping the sprint to build BQ tables** — escalate with BLOCKERS; keep LookML moving.  
8. **Calling inventory gate “KPI ready”** — gate = capture complete, not parity.

---

## Monday-morning LookML checklist

- [ ] Clone / open this repo; skim MIGRATION_SUMMARY + BLOCKERS  
- [ ] Confirm Looker connection name; set `connection:` in model  
- [ ] Align `sql_table_name` to your dataset (or escalate missing tables)  
- [ ] Validate LookML project (dims → employee → explore)  
- [ ] Confirm 8 joins match `03_relationships.json`  
- [ ] Ship simple measures (Actives, Seps, New Hires, Bad Hires, TO %)  
- [ ] Park SPLY / EmpCount / TO % Norm with `# TODO` + tracker  
- [ ] Run parity rows 1–12 when data is available  
- [ ] Only then schedule Phase 8 complex TI  

---

## Summary for the LookML developer

**Start here:** `views/` + `models/human_resources.model.lkml` from the previous conversion.  

**Your job:** wire connection → validate views/joins → ship simple measures → park complex DAX with clear blockers.  

**Not your job in this guide:** building BigQuery tables. If Explore cannot find `hr.*`, escalate using [BLOCKERS_AND_DEPENDENCIES.md](BLOCKERS_AND_DEPENDENCIES.md) (Employee.m is the critical chain) and continue LookML polish.

You are not blocked from **starting LookML**. You *are* blocked from **claiming full KPI parity** until warehouse tables exist **and** SPLY / EmpCount / TO % Norm patterns are implemented.

---

## Appendix A — Join field cheat sheet

| LookML field | Warehouse column | Joins to |
|--------------|------------------|----------|
| `employee.snapshot_date` | `date` | `date.calendar_date` |
| `employee.bu` | `BU` | `bu.bu` |
| `employee.age_group_id` | derived or `AgeGroupID` | `age_group.age_group_id` |
| `employee.ethnic_group` | `EthnicGroup` | `ethnicity.ethnic_group` |
| `employee.fp` | `FP` | `fp.fp` |
| `employee.gender_id` | `Gender` (C/D) | `gender.id` |
| `employee.pay_type_id` | `PayTypeID` | `pay_type.pay_type_id` |
| `employee.term_reason` | `TermReason` | `separation_reason.separation_type_id` |

---

## Appendix B — Measure status map (from prior conversion)

### Implemented (logic ready; needs data to validate)

`seps`, `actives`, `new_hires`, `sum_of_bad_hires`, `avg_tenure_days`, `avg_tenure_months`, `avg_age`, `to_pct`, `sep_pct_of_active`, `bad_hire_pct_of_actives`, `count_of_bu`, `count_of_date`, YoY arithmetic measures (depend on SPLY parents).

### Stubbed with `# TODO`

`emp_count` (needs max PeriodNumber), `*_sply`, `to_pct_norm`, and anything that only divides SPLY parents.

---

## Appendix C — Escalation one-liner (copy/paste)

```text
BLOCKER: <what fails in Looker>
  └── depends on: <M file or DAX from inventory>
  └── UNLOCKS: <KPI names>
  └── HOW: warehouse SQL | LookML PoP | filtered measure
  └── LookML status: view/measure already drafted at <path>
```
