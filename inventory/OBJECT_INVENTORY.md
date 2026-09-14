# OBJECT INVENTORY — Human Resources Sample PBIX

**Source:** `/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`

## 1. Summary

| Metric | Count |
|---|---:|
| Tables | 15 |
| Business tables | 9 |
| Internal tables | 6 |
| Columns | 87 |
| Measures | 30 |
| Calculated columns | 43 |
| Calculated tables | 6 |
| Relationships | 8 |
| Power Query queries | 9 |
| RLS roles | 0 |
| Completeness gate | **PASS** |

## 2. Tables

### `AgeGroup`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 2 (0 calculated)
- **Power Query:** `04_m_raw/AgeGroup.m` (embedded_static)

### `BU`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 4 (1 calculated)
- **Power Query:** `04_m_raw/BU.m` (sql_database)

### `Date`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 12 (1 calculated)
- **Power Query:** `04_m_raw/Date.m` (sql_database)

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `Employee`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 16 (5 calculated)
- **Power Query:** `04_m_raw/Employee.m` (sql_database)

### `Ethnicity`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 2 (0 calculated)
- **Power Query:** `04_m_raw/Ethnicity.m` (embedded_static)

### `FP`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 2 (0 calculated)
- **Power Query:** `04_m_raw/FP.m` (sql_database)

### `Gender`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 3 (0 calculated)
- **Power Query:** `04_m_raw/Gender.m` (embedded_static)

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6`

- **type:** calculated_table
- **business:** False | **internal:** True
- **columns:** 7 (6 calculated)
- **source:** calculated table (DAX)

### `PayType`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 2 (0 calculated)
- **Power Query:** `04_m_raw/PayType.m` (sql_database)

### `SeparationReason`

- **type:** business
- **business:** True | **internal:** False
- **columns:** 2 (0 calculated)
- **Power Query:** `04_m_raw/SeparationReason.m` (sql_database)

## 3. Measures

### `Employee[EmpCount]` — MODERATE

```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
```

### `Employee[Seps]` — MODERATE

```dax
CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
```

### `Employee[Actives]` — MODERATE

```dax
CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
```

### `Employee[New Hires]` — SIMPLE

```dax
SUM([isNewHire])
```

### `Employee[AVG Tenure Days]` — SIMPLE

```dax
AVERAGE([TenureDays])
```

### `Employee[AVG Tenure Months]` — SIMPLE

```dax
ROUND([AVG Tenure Days]/30, 1)-1
```

### `Employee[AVG Age]` — SIMPLE

```dax
ROUND(AVERAGE([Age]), 0)
```

### `Employee[Sum of BadHires]` — SIMPLE

```dax
SUM([BadHires])
```

### `Employee[New Hires SPLY]` — COMPLEX

```dax
CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Actives SPLY]` — COMPLEX

```dax
CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Seps SPLY]` — COMPLEX

```dax
CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[EmpCount SPLY]` — COMPLEX

```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])),SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Seps YoY Var]` — SIMPLE

```dax
[Seps]-[Seps SPLY]
```

### `Employee[Actives YoY Var]` — SIMPLE

```dax
[Actives]-[Actives SPLY]
```

### `Employee[New Hires YoY Var]` — SIMPLE

```dax
[New Hires]-[New Hires SPLY]
```

### `Employee[Seps YoY % Change]` — SIMPLE

```dax
DIVIDE([Seps YoY Var], [Seps SPLY])
```

### `Employee[Actives YoY % Change]` — SIMPLE

```dax
DIVIDE([Actives YoY Var], [Actives SPLY])
```

### `Employee[New Hires YoY % Change]` — SIMPLE

```dax
DIVIDE([New Hires YoY Var], [New Hires SPLY])
```

### `Employee[Bad Hires SPLY]` — COMPLEX

```dax
CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Bad Hires YoY Var]` — SIMPLE

```dax
[Sum of BadHires]-[Bad Hires SPLY]
```

### `Employee[Bad Hires YoY % Change]` — SIMPLE

```dax
DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])
```

### `Employee[TO %]` — SIMPLE

```dax
DIVIDE([Seps], [Actives])
```

### `Employee[TO % Norm]` — MODERATE

```dax
CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
```

### `Employee[TO % Var]` — SIMPLE

```dax
[TO %]-[TO % Norm]
```

### `Employee[Sep%ofActive]` — SIMPLE

```dax
DIVIDE([Seps],[Actives])
```

### `Employee[Sep%ofSMLYActives]` — SIMPLE

```dax
DIVIDE([Seps SPLY],[Actives SPLY])
```

### `Employee[BadHire%ofActives]` — SIMPLE

```dax
DIVIDE([Sum of BadHires],[Actives])
```

### `Employee[BadHire%ofActiveSPLY]` — SIMPLE

```dax
DIVIDE([Bad Hires SPLY],[Actives SPLY])
```

### `BU[Count of BU]` — SIMPLE

```dax
COUNTA('BU'[BU])
```

### `Date[Count of Date]` — SIMPLE

```dax
COUNTA('Date'[Date])
```

## 4. Calculated Columns

### `BU[Region]` — SIMPLE

```dax
mid([RegionSeq], 3,15)
```

### `Date[MonthIncrementNumber]` — MODERATE

```dax
([Year]-MIN([Year]))*12 +[MonthNumber]
```

### `Employee[isNewHire]` — SIMPLE

```dax
IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)
```

### `Employee[AgeGroupID]` — SIMPLE

```dax
IF([Age]<30, 1, IF([Age]<50, 2, 3))
```

### `Employee[TenureDays]` — SIMPLE

```dax
IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])
```

### `Employee[TenureMonths]` — SIMPLE

```dax
CEILING([TenureDays]/30, 1) -1
```

### `Employee[BadHires]` — SIMPLE

```dax
IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Day]` — SIMPLE

```dax
DAY([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Day]` — SIMPLE

```dax
DAY([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Day]` — SIMPLE

```dax
DAY([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Day]` — SIMPLE

```dax
DAY([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Day]` — SIMPLE

```dax
DAY([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Year]` — SIMPLE

```dax
YEAR([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[MonthNo]` — SIMPLE

```dax
MONTH([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Month]` — SIMPLE

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[QuarterNo]` — SIMPLE

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Quarter]` — SIMPLE

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Day]` — SIMPLE

```dax
DAY([Date])
```

## 5. Calculated Tables

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d` — SIMPLE

```dax
Calendar(Date(2015,1,1), Date(2015,1,1))
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782` — MODERATE

```dax
Calendar(Date(Year(MIN('Date'[Date])), 1, 1), Date(Year(MAX('Date'[Date])), 12, 31))
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6` — MODERATE

```dax
Calendar(Date(Year(MIN('Date'[MonthStartDate])), 1, 1), Date(Year(MAX('Date'[MonthStartDate])), 12, 31))
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac` — MODERATE

```dax
Calendar(Date(Year(MIN('Date'[MonthEndDate])), 1, 1), Date(Year(MAX('Date'[MonthEndDate])), 12, 31))
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b` — MODERATE

```dax
Calendar(Date(Year(MIN('Employee'[TermDate])), 1, 1), Date(Year(MAX('Employee'[TermDate])), 12, 31))
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29` — MODERATE

```dax
Calendar(Date(Year(MIN('Employee'[HireDate])), 1, 1), Date(Year(MAX('Employee'[HireDate])), 12, 31))
```

## 6. Relationships

| From | Column | To | Column | Cardinality | Cross-filter | Active |
|---|---|---|---|---|---|---|
| Employee | date | Date | Date | M:1 | Single | True |
| Employee | FP | FP | FP | M:1 | Single | True |
| Employee | EthnicGroup | Ethnicity | Ethnic Group | M:1 | Single | True |
| Employee | Gender | Gender | ID | M:1 | Single | True |
| Employee | PayTypeID | PayType | PayTypeID | M:1 | Single | True |
| Employee | BU | BU | BU | M:1 | Single | True |
| Employee | AgeGroupID | AgeGroup | AgeGroupID | M:1 | Single | True |
| Employee | TermReason | SeparationReason | SeparationTypeID | M:1 | Single | True |

## 7. Power Query

### `BU`

- **file:** `04_m_raw/BU.m`
- **source_type:** sql_database
- **tags:** sql_database, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `FP`

- **file:** `04_m_raw/FP.m`
- **source_type:** sql_database
- **tags:** sql_database, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `PayType`

- **file:** `04_m_raw/PayType.m`
- **source_type:** sql_database
- **tags:** sql_database, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `SeparationReason`

- **file:** `04_m_raw/SeparationReason.m`
- **source_type:** sql_database
- **tags:** sql_database, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `Date`

- **file:** `04_m_raw/Date.m`
- **source_type:** sql_database
- **tags:** sql_database, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `Employee`

- **file:** `04_m_raw/Employee.m`
- **source_type:** sql_database
- **tags:** sql_database, append_union, query_reference, transformation_heavy
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `Ethnicity`

- **file:** `04_m_raw/Ethnicity.m`
- **source_type:** embedded_static
- **tags:** embedded_seed, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `Gender`

- **file:** `04_m_raw/Gender.m`
- **source_type:** embedded_static
- **tags:** embedded_seed, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

### `AgeGroup`

- **file:** `04_m_raw/AgeGroup.m`
- **source_type:** embedded_static
- **tags:** embedded_seed, query_reference
- **referenced_queries:** Renamed Columns, Changed Type, Renamed Columns, Changed Type

## 8. TM Extras

- **partitions:** 122
- **hierarchies:** 7
- **RLS:** 0 (explicitly captured; empty = none)
- **perspectives:** 0
- **annotations:** 158
- **sort-by columns:** 0
- **display folders:** 0
- **format strings:** 5
- **auto date tables:** 6

### Hierarchies

- `Date.YQM`: Year(Year) → QtrNumber(QtrNumber) → PeriodNumber(PeriodNumber)
- `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)
- `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)
- `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)
- `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)
- `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)
- `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Date Hierarchy`: Year(Year) → Quarter(Quarter) → Month(Month) → Day(Day)

## 9. Migration Notes

Direct Power BI → LookML conversion is not enough because business logic is split across layers:

```text
M (Power Query) → warehouse tables/seeds
              → calculated columns (DAX or SQL)
              → measures (DAX → LookML)
relationships → LookML joins
date tables / PeriodNumber → time intelligence (SPLY, EmpCount)
```

Key dependency chains in this PBIX:

1. **Employee.m** (SQL UNION actives+seps) must exist in warehouse before any HR KPI.
2. Seed dims (AgeGroup, Gender, Ethnicity) are embedded M — warehouse seeds, not SQL Server.
3. Complex DAX (`SAMEPERIODLASTYEAR`, max `PeriodNumber`, `ALL(Gender/Ethnicity)`) needs LookML PoP / filtered measures + parity tests.
4. Internal `LocalDateTable_*` / `DateTableTemplate_*` are captured but should be `SKIP_PBI_INTERNAL` for LookML; use business `Date`.
5. **RLS:** none in this PBIX (`rls: []`).

### Blockers (inventory phase)

```text
BLOCKER
Depends on: inventory/04_m_raw/Employee.m
Impact: No runnable Employee fact in Looker until warehouse load
Unlocks: Actives, Seps, New Hires, Bad Hires, TO %, all YoY/SPLY
Resolution: warehouse SQL from M (or PBIX export load) — Phase 2
```

```text
BLOCKER
Depends on: SAMEPERIODLASTYEAR DAX (multiple measures)
Impact: * SPLY and dependent YoY / ratio measures
Unlocks: YoY Var/%, Sep%ofSMLY*, BadHire%ofActiveSPLY
Resolution: LookML time comparison + KPI parity test — after Phase 1 PASS
```

