# Blockers & Dependencies (No dbt)

This file lists what is **blocked**, **why**, and **how to unblock** — with clear **M-code → table → KPI** chains.  
Reports/dashboards are out of scope on purpose.

---

## How to read this

```
BLOCKER (what is missing)
  └── depends on: M file / DAX / Looker pattern
  └── unlocks KPIs: measure names that cannot be trusted until this is done
  └── how to achieve: concrete next step (warehouse SQL or LookML — not dbt)
```

---

## BLOCKER 1 — Employee fact table not in warehouse

**Status:** BLOCKED  
**Why:** Power BI builds `Employee` in Power Query from SQL Server. Looker has no table to query yet.  
**M dependency:** [`inventory/04_m_raw/Employee.m`](04_m_raw/Employee.m)

What that M does (must be reproduced outside LookML):
- Reads `IP.HR.AllEmps` + `HR.Date` + `HR.BU` + `hr.PayGroup` + `hr.TermReason`
- **UNION ALL** of actives (TermDate null) and separations (TermDate set)
- Shifts dates by +1 year (`dateadd(year, 1, …)`)
- Remaps gender `M→C`, else `D`
- Adjusts age; keeps only `EmplID % 2 = 0`
- Month-grain snapshots (`d.day = 1`)

**Unlocks these KPIs (ALL employee measures):**

| KPI | Needs Employee rows? |
|---|---|
| Actives, Seps, EmpCount | Yes |
| New Hires, New Hires SPLY, YoY | Yes |
| Sum of BadHires, Bad Hire % | Yes |
| AVG Age, AVG Tenure Days/Months | Yes |
| TO %, TO % Norm, TO % Var | Yes |
| Sep%ofActive, Sep%ofSMLYActives | Yes |

**How to achieve (no dbt):**
1. Create warehouse view/table `hr.employee` using the SQL inside `Employee.m` (adapt server/`IP` to your warehouse).  
2. Or load a export of the PBIX Employee table into the warehouse.  
3. Point LookML `employee.sql_table_name` at that table.

**Until then:** LookML views are templates only — **0% runnable KPI conversion for HR metrics.**

---

## BLOCKER 2 — Dimension tables from M/SQL not in warehouse

**Status:** BLOCKED for joins/filters that use these dims  

| Table | M file | Source pattern | Needed for |
|---|---|---|---|
| Date | `04_m_raw/Date.m` | `SELECT HR.Date.*` | Time filters, SPLY, EmpCount period logic, all YoY |
| BU | `04_m_raw/BU.m` | SQL distinct market/region/VP | Region / VP slicing |
| FP | `04_m_raw/FP.m` | `HR.FP` | Full/Part-time filters |
| PayType | `04_m_raw/PayType.m` | PayGroup → Hourly/Salaried | Pay type filters |
| SeparationReason | `04_m_raw/SeparationReason.m` | TermReason Vol/Invol | Voluntary vs involuntary seps |

**Unlocks KPIs when sliced by:**
- Region / VP → needs **BU** (+ calc column Region — see Blocker 4)
- Month / Year / Period → needs **Date**
- Separation reason charts → needs **SeparationReason**
- FP / PayType breakdowns → needs **FP**, **PayType**

**How to achieve:** Warehouse views from each `.m` SQL, then LookML `sql_table_name`.

---

## BLOCKER 3 — Seed dimensions embedded in M (not SQL Server)

**Status:** BLOCKED until small lookup tables exist  

| Table | M file | Why special | Unlocks |
|---|---|---|---|
| AgeGroup | `04_m_raw/AgeGroup.m` | Embedded `Table.FromRows` (seed) | Age band pie/filters; join on AgeGroupID |
| Gender | `04_m_raw/Gender.m` | Embedded seed (D=Male, C=Female) | Gender splits; TO % Norm |
| Ethnicity | `04_m_raw/Ethnicity.m` | Embedded seed (Group A–…) | Ethnicity splits; TO % Norm |

**KPI examples that depend on these:**
- Actives by Age Group / Gender / Ethnicity  
- Bad Hires by Gender  
- **TO % Norm** (explicitly clears Gender + Ethnicity filters — still needs the dims to exist)

**How to achieve:** Create tiny warehouse tables (or Looker `derived_table` with fixed rows). Sample values already known from PBIX extract (`<30`, `30-49`, `50+`, etc.).

---

## BLOCKER 4 — Calculated columns (DAX) not materialized

**Status:** PARTIAL — LookML has SQL sketches; warehouse may not  

These were **DAX calculated columns** in Power BI. Several KPIs are computed **from** them.

| Column | DAX (summary) | KPIs that depend on it |
|---|---|---|
| `Employee[isNewHire]` | Snapshot month = hire month → 1 | **New Hires**, New Hires SPLY, New Hires YoY Var/% |
| `Employee[BadHires]` | Terminated within 60 days of hire → 1 | **Sum of BadHires**, Bad Hires SPLY, BadHire%ofActives, BadHire%ofActiveSPLY, Bad Hires YoY |
| `Employee[TenureDays]` / `[TenureMonths]` | Date diff / ceiling | **AVG Tenure Days**, **AVG Tenure Months** |
| `Employee[AgeGroupID]` | Age → 1/2/3 | Join to AgeGroup; all age-band visuals/KPIs |
| `BU[Region]` | `MID(RegionSeq,3,15)` | Region slicing (North/East/…) |
| `Date[MonthIncrementNumber]` | Months since min year | Rarely used in measures; keep for parity |

**How to achieve:**
- Prefer: add columns in warehouse SQL when building Blocker 1–2 tables, **or**
- Keep LookML `dimension` SQL (already drafted in `views/employee.view.lkml` / `bu.view.lkml`).

**Clear dependency example:**
```
M: Employee.m  →  table hr.employee
DAX: isNewHire  →  column on that table (or LookML dim)
KPI: New Hires = SUM(isNewHire)
```
If Employee.m is not loaded, **New Hires cannot be calculated** — even if LookML measure exists.

---

## BLOCKER 5 — Time intelligence DAX (LookML complex)

**Status:** BLOCKED in LookML (stubs / incomplete)  
**Not an M issue** — tables alone are not enough.

| KPI | Depends on DAX pattern | Also depends on |
|---|---|---|
| **New Hires SPLY** | `SAMEPERIODLASTYEAR(Date[Date])` | Employee + Date + isNewHire |
| **Actives SPLY** | same | Employee + Date + TermDate blank |
| **Seps SPLY** | same | Employee + Date + TermDate set |
| **Bad Hires SPLY** | same | Employee + Date + BadHires |
| **EmpCount SPLY** | SPLY + max PeriodNumber | Date[PeriodNumber] |
| **Seps/Actives/New Hires/Bad Hires YoY Var** | `[This]-[SPLY]` | **parent SPLY KPI** |
| **Seps/Actives/New Hires/Bad Hires YoY %** | `Var / SPLY` | **parent SPLY KPI** |
| **Sep%ofSMLYActives** | Seps SPLY / Actives SPLY | both SPLY KPIs |
| **BadHire%ofActiveSPLY** | Bad Hires SPLY / Actives SPLY | both SPLY KPIs |

**Chain example (call out clearly):**
```
BLOCKED: New Hires YoY % Change
  └── needs: New Hires YoY Var
        └── needs: New Hires SPLY          ← LOOKML_TODO (SAMEPERIODLASTYEAR)
              └── needs: New Hires         ← SUM(isNewHire)
                    └── needs: isNewHire   ← calc column
                          └── needs: hr.employee from Employee.m   ← M DEPENDENCY
```

**How to achieve:** Implement Looker period-over-period (date offset / prior-year join / PoP), then YoY measures become simple arithmetic.

---

## BLOCKER 6 — EmpCount “latest period” logic

**Status:** BLOCKED (LookML not equivalent yet)

**DAX:**
```dax
CALCULATE(
  COUNT([EmplID]),
  FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber]))
)
```

**Why:** Not a normal count — forces **max PeriodNumber** in context.  
**Depends on:** `Date` table + `PeriodNumber` (from `Date.m`).  
**Unlocks:** EmpCount, and any report tile that used EmpCount as “current headcount”.  
**Note:** Actives in this model is `CALCULATE([EmpCount], TermDate blank)` in PBIX — so **Actives also inherits EmpCount’s period behavior** in Power BI. Our LookML Actives uses distinct count with TermDate filter only — **parity risk** until EmpCount logic is matched.

**How to achieve:** Looker always_filter on latest period, or measure SQL restricted to `MAX(PeriodNumber)`.

---

## BLOCKER 7 — TO % Norm (ignore filters)

**Status:** BLOCKED

**DAX:** `CALCULATE([TO %], ALL(Gender[Gender]), ALL(Ethnicity[Ethnicity]))`  
**Meaning:** Turnover as if Gender & Ethnicity filters were not applied.  
**Depends on:** Actives, Seps, Gender dim, Ethnicity dim.  
**Unlocks:** TO % Norm, **TO % Var** (`TO % - TO % Norm`).

**How to achieve:** Separate Looker measure/explore that does not apply those filters, or SQL that recomputes TO% without those predicates.

---

## BLOCKER 8 — KPI parity not run

**Status:** NOT STARTED (by design until Blockers 1–7 unblock)

**Why:** Even perfect LookML can disagree with Power BI on grain/filters/SPLY.  
**How:** After warehouse + measures work, compare 10–15 KPIs (see checklist below).

Suggested first parity set (only after Blocker 1+2+3):
1. Actives (all)  
2. Seps (all)  
3. New Hires (all)  
4. Sum of BadHires (all)  
5. Actives by Region  
6. Actives by Gender  
7. Actives by AgeGroup  
8. New Hires by Month  
9. Seps by SeparationReason  
10. TO % (all)  
Then later: SPLY / YoY / EmpCount / TO % Norm.

---

## Summary scoreboard

| Blocker | Type | Blocks runnable KPIs? |
|---|---|---|
| 1 Employee.m → warehouse | **M dependency** | Yes — almost all |
| 2 Dim SQL M files | **M dependency** | Yes — sliced KPIs |
| 3 Seed M (Age/Gender/Ethnicity) | **M dependency** | Yes — diversity / joins |
| 4 Calc columns | DAX → SQL/LookML | Yes — New Hires, Bad Hires, Tenure, AgeGroup |
| 5 SPLY / YoY chain | LookML complex | Yes — all SPLY & YoY KPIs |
| 6 EmpCount max period | LookML complex | Yes — EmpCount (+ Actives parity risk) |
| 7 TO % Norm | LookML complex | Yes — TO % Norm/Var |
| 8 KPI parity tests | Validation | Confidence, not build |

---

## What is NOT blocked (once tables exist)

These LookML measures can work after Blockers 1–4 only (no SPLY needed):
- Seps, Actives (approx), New Hires, Sum of BadHires  
- AVG Age, AVG Tenure Days/Months  
- TO %, Sep%ofActive, BadHire%ofActives  
- Count of BU / Date  
- All 8 joins (once dims exist)

---

## Bottom line

We are **not** silent on gaps: if something is blocked by M, we name the **`.m` file**, the **table**, and the **KPIs that sit on top of it**.  

Next build step (no dbt): implement **Blocker 1–3 warehouse SQL** from `inventory/04_m_raw/`, then fix **Blocker 5–7** in LookML, then run **Blocker 8** parity.
