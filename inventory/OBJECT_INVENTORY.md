# Power BI Object Inventory

**Source:** `/Users/Basavaraj_Angadi/Downloads/Human Resources Sample PBIX.pbix`

Semantic-model objects only (report visuals out of scope).

## Completeness gate

**PASSED** — all capture gates succeeded.

| Gate | Expected | Actual |
|---|---|---|
| Tables | 15 | 15 |
| Schema columns | (all) | 87 |
| Measures | 30 | 30 |
| Calculated columns | (all) | 43 |
| Calculated tables | 6 | 6 |
| Relationships | 8 | 8 |
| Power Query queries | 9 | 9 |
| `.m` files | 9 | 9 |
| TM empty categories listed | yes | 29 |

## Action summary

| Action tag | Count |
|---|---|
| `DBT_SEED` | 3 |
| `DBT_SQL` | 20 |
| `LOOKML_JOIN` | 8 |
| `LOOKML_MEASURE` | 22 |
| `LOOKML_TODO_COMPLEX` | 14 |
| `LOOKML_VIEW_DIM` | 35 |
| `LOOKML_VIEW_FACT` | 12 |
| `NONE_IN_SOURCE` | 29 |
| `SKIP_PBI_INTERNAL` | 94 |

| Object class | Count |
|---|---|
| column | 87 |
| dax_calculated_column | 43 |
| dax_calculated_table | 6 |
| measure | 30 |
| power_query | 9 |
| relationship | 8 |
| table | 15 |
| tmschema | 39 |

## Tables

### `AgeGroup` → `LOOKML_VIEW_DIM` (2 columns)

- `AgeGroupID` (Int64)
- `AgeGroup` (string)

### `BU` → `LOOKML_VIEW_DIM` (4 columns)

- `BU` (string)
- `RegionSeq` (string)
- `VP` (string)
- `Region` (string)

### `Date` → `LOOKML_VIEW_DIM` (12 columns)

- `Date` (datetime64[ns])
- `Month` (string)
- `MonthNumber` (Int64)
- `Period` (string)
- `PeriodNumber` (Int64)
- `Qtr` (Int64)
- `QtrNumber` (string)
- `Year` (Int64)
- `Day` (Int64)
- `MonthStartDate` (datetime64[ns])
- `MonthEndDate` (datetime64[ns])
- `MonthIncrementNumber` (Int64)

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `Employee` → `LOOKML_VIEW_FACT` (16 columns)

- `date` (datetime64[ns])
- `EmplID` (Int64)
- `Gender` (string)
- `Age` (Int64)
- `EthnicGroup` (string)
- `FP` (string)
- `TermDate` (datetime64[ns])
- `isNewHire` (Int64)
- `BU` (string)
- `HireDate` (datetime64[ns])
- `PayTypeID` (string)
- `TermReason` (string)
- `AgeGroupID` (Int64)
- `TenureDays` (Float64)
- `TenureMonths` (Int64)
- `BadHires` (Float64)

### `Ethnicity` → `LOOKML_VIEW_DIM` (2 columns)

- `Ethnic Group` (string)
- `Ethnicity` (string)

### `FP` → `LOOKML_VIEW_DIM` (2 columns)

- `FP` (string)
- `FPDesc` (string)

### `Gender` → `LOOKML_VIEW_DIM` (3 columns)

- `ID` (string)
- `Gender` (string)
- `Sort` (Int64)

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6` → `SKIP_PBI_INTERNAL` (7 columns)

- `Date` (datetime64[ns])
- `Year` (Int64)
- `MonthNo` (Int64)
- `Month` (string)
- `QuarterNo` (Int64)
- `Quarter` (string)
- `Day` (Int64)

### `PayType` → `LOOKML_VIEW_DIM` (2 columns)

- `PayTypeID` (string)
- `PayType` (string)

### `SeparationReason` → `LOOKML_VIEW_DIM` (2 columns)

- `SeparationTypeID` (string)
- `SeparationReason` (string)

## Measures (full DAX)

### `Employee[EmpCount]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
```

### `Employee[Seps]` → `LOOKML_MEASURE`

```dax
CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
```

### `Employee[Actives]` → `LOOKML_MEASURE`

```dax
CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
```

### `Employee[New Hires]` → `LOOKML_MEASURE`

```dax
SUM([isNewHire])
```

### `Employee[AVG Tenure Days]` → `LOOKML_MEASURE`

```dax
AVERAGE([TenureDays])
```

### `Employee[AVG Tenure Months]` → `LOOKML_MEASURE`

```dax
ROUND([AVG Tenure Days]/30, 1)-1
```

### `Employee[AVG Age]` → `LOOKML_MEASURE`

```dax
ROUND(AVERAGE([Age]), 0)
```

### `Employee[Sum of BadHires]` → `LOOKML_MEASURE`

```dax
SUM([BadHires])
```

### `Employee[New Hires SPLY]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Actives SPLY]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Seps SPLY]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[EmpCount SPLY]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])),SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Seps YoY Var]` → `LOOKML_MEASURE`

```dax
[Seps]-[Seps SPLY]
```

### `Employee[Actives YoY Var]` → `LOOKML_MEASURE`

```dax
[Actives]-[Actives SPLY]
```

### `Employee[New Hires YoY Var]` → `LOOKML_MEASURE`

```dax
[New Hires]-[New Hires SPLY]
```

### `Employee[Seps YoY % Change]` → `LOOKML_MEASURE`

```dax
DIVIDE([Seps YoY Var], [Seps SPLY])
```

### `Employee[Actives YoY % Change]` → `LOOKML_MEASURE`

```dax
DIVIDE([Actives YoY Var], [Actives SPLY])
```

### `Employee[New Hires YoY % Change]` → `LOOKML_MEASURE`

```dax
DIVIDE([New Hires YoY Var], [New Hires SPLY])
```

### `Employee[Bad Hires SPLY]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date]))
```

### `Employee[Bad Hires YoY Var]` → `LOOKML_MEASURE`

```dax
[Sum of BadHires]-[Bad Hires SPLY]
```

### `Employee[Bad Hires YoY % Change]` → `LOOKML_MEASURE`

```dax
DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])
```

### `Employee[TO %]` → `LOOKML_MEASURE`

```dax
DIVIDE([Seps], [Actives])
```

### `Employee[TO % Norm]` → `LOOKML_TODO_COMPLEX`

```dax
CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
```

### `Employee[TO % Var]` → `LOOKML_MEASURE`

```dax
[TO %]-[TO % Norm]
```

### `Employee[Sep%ofActive]` → `LOOKML_MEASURE`

```dax
DIVIDE([Seps],[Actives])
```

### `Employee[Sep%ofSMLYActives]` → `LOOKML_MEASURE`

```dax
DIVIDE([Seps SPLY],[Actives SPLY])
```

### `Employee[BadHire%ofActives]` → `LOOKML_MEASURE`

```dax
DIVIDE([Sum of BadHires],[Actives])
```

### `Employee[BadHire%ofActiveSPLY]` → `LOOKML_TODO_COMPLEX`

```dax
DIVIDE([Bad Hires SPLY],[Actives SPLY])
```

### `BU[Count of BU]` → `LOOKML_MEASURE`

```dax
COUNTA('BU'[BU])
```

### `Date[Count of Date]` → `LOOKML_MEASURE`

```dax
COUNTA('Date'[Date])
```

## Calculated columns (full DAX)

### `BU[Region]` → `DBT_SQL`

```dax
mid([RegionSeq], 3,15)
```

### `Date[MonthIncrementNumber]` → `DBT_SQL`

```dax
([Year]-MIN([Year]))*12 +[MonthNumber]
```

### `Employee[isNewHire]` → `DBT_SQL`

```dax
IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)
```

### `Employee[AgeGroupID]` → `DBT_SQL`

```dax
IF([Age]<30, 1, IF([Age]<50, 2, 3))
```

### `Employee[TenureDays]` → `DBT_SQL`

```dax
IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])
```

### `Employee[TenureMonths]` → `DBT_SQL`

```dax
CEILING([TenureDays]/30, 1) -1
```

### `Employee[BadHires]` → `DBT_SQL`

```dax
IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Year]` → `SKIP_PBI_INTERNAL`

```dax
YEAR([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[MonthNo]` → `SKIP_PBI_INTERNAL`

```dax
MONTH([Date])
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Month]` → `SKIP_PBI_INTERNAL`

```dax
FORMAT([Date], "MMMM")
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[QuarterNo]` → `SKIP_PBI_INTERNAL`

```dax
INT(([MonthNo] + 2) / 3)
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Quarter]` → `SKIP_PBI_INTERNAL`

```dax
"Qtr " & [QuarterNo]
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29[Day]` → `SKIP_PBI_INTERNAL`

```dax
DAY([Date])
```

## Calculated tables (full DAX)

### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(2015,1,1), Date(2015,1,1))
```

### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(Year(MIN('Date'[Date])), 1, 1), Date(Year(MAX('Date'[Date])), 12, 31))
```

### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(Year(MIN('Date'[MonthStartDate])), 1, 1), Date(Year(MAX('Date'[MonthStartDate])), 12, 31))
```

### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(Year(MIN('Date'[MonthEndDate])), 1, 1), Date(Year(MAX('Date'[MonthEndDate])), 12, 31))
```

### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(Year(MIN('Employee'[TermDate])), 1, 1), Date(Year(MAX('Employee'[TermDate])), 12, 31))
```

### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29` → `SKIP_PBI_INTERNAL`

```dax
Calendar(Date(Year(MIN('Employee'[HireDate])), 1, 1), Date(Year(MAX('Employee'[HireDate])), 12, 31))
```

## Relationships

| From | To | Cardinality | Active | Cross-filter | Action |
|---|---|---|---|---|---|
| Employee.date | Date.Date | M:1 | True | Single | LOOKML_JOIN |
| Employee.FP | FP.FP | M:1 | True | Single | LOOKML_JOIN |
| Employee.EthnicGroup | Ethnicity.Ethnic Group | M:1 | True | Single | LOOKML_JOIN |
| Employee.Gender | Gender.ID | M:1 | True | Single | LOOKML_JOIN |
| Employee.PayTypeID | PayType.PayTypeID | M:1 | True | Single | LOOKML_JOIN |
| Employee.BU | BU.BU | M:1 | True | Single | LOOKML_JOIN |
| Employee.AgeGroupID | AgeGroup.AgeGroupID | M:1 | True | Single | LOOKML_JOIN |
| Employee.TermReason | SeparationReason.SeparationTypeID | M:1 | True | Single | LOOKML_JOIN |

## Power Query (M)

### `BU` → `DBT_SQL` (complexity=high; tags=sql_database)

Raw file: `04_m_raw/BU.m`

Embedded SQL:

```sql
select distinct market BU,
  REGIONTITLE Region,
  MARKETDIRECTOR VP
from hr.bu
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"BU", "BU"}, {"Region", "RegionSeq"}, {"VP", "VP"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"BU", type text}, {"RegionSeq", type text}, {"VP", type text}})
in
    #"Changed Type"
```

</details>

### `FP` → `DBT_SQL` (complexity=high; tags=sql_database)

Raw file: `04_m_raw/FP.m`

Embedded SQL:

```sql
SELECT [HR].[FP].*   FROM [HR].[FP]
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="SELECT [HR].[FP].*   FROM [HR].[FP]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"FP", "FP"}, {"FPDesc", "FPDesc"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"FP", type text}, {"FPDesc", type text}})
in
    #"Changed Type"
```

</details>

### `PayType` → `DBT_SQL` (complexity=high; tags=sql_database)

Raw file: `04_m_raw/PayType.m`

Embedded SQL:

```sql
select distinct PayTypeID, [Hrly-Salaried] PayType
from [HR].[PayGroup]
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"PayTypeID", "PayTypeID"}, {"PayType", "PayType"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"PayTypeID", type text}, {"PayType", type text}})
in
    #"Changed Type"
```

</details>

### `SeparationReason` → `DBT_SQL` (complexity=high; tags=sql_database)

Raw file: `04_m_raw/SeparationReason.m`

Embedded SQL:

```sql
SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason
  FROM [IP].[HR].[TermReason]
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"SeparationTypeID", "SeparationTypeID"}, {"SeparationReason", "SeparationReason"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"SeparationTypeID", type text}, {"SeparationReason", type text}})
in
    #"Changed Type"
```

</details>

### `Date` → `DBT_SQL` (complexity=high; tags=sql_database)

Raw file: `04_m_raw/Date.m`

Embedded SQL:

```sql
SELECT [HR].[Date].*   FROM [HR].[Date]
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="SELECT [HR].[Date].*   FROM [HR].[Date]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Date", "Date"}, {"Month", "Month"}, {"MonthNumber", "MonthNumber"}, {"Period", "Period"}, {"PeriodNumber", "PeriodNumber"}, {"Qtr", "Qtr"}, {"QtrNumber", "QtrNumber"}, {"Year", "Year"}, {"Day", "Day"}, {"MonthStartDate", "MonthStartDate"}, {"MonthEndDate", "MonthEndDate"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"Date", type datetime}, {"Month", type text}, {"MonthNumber", Int64.Type}, {"Period", type text}, {"PeriodNumber", Int64.Type}, {"Qtr", Int64.Type}, {"QtrNumber", type text}, {"Year", Int64.Type}, {"Day", Int64.Type}, {"MonthStartDate", type datetime}, {"MonthEndDate", type datetime}})
in
    #"Changed Type"
```

</details>

### `Employee` → `DBT_SQL` (complexity=high; tags=sql_database, union_combine, complex)

Raw file: `04_m_raw/Employee.m`

Embedded SQL:

```sql
SELECT dateadd(year, 1, d.date) Date
  ,Market BU
  ,[EmplID]
  ,iif([Gender]='M', 'C', 'D') Gender --  ,iif([Gender]='M', 'F', 'M') Gender
  ,[Age] - (2013 - year(d.date)) Age
  ,[EthnicGroup]
  ,[FP]
  ,dateadd(year, 1, [SenDate]) HireDate
  ,p.PayTypeID
  ,null [TermDate]
  ,null [TermReason]
 FROM [IP].[HR].[AllEmps] E , [HR].[Date] d , [HR].[BU] b , hr.PayGroup p --, hr.TermReason t
 where d.day = 1 and e.SenDate <= d.MonthEndDate and isnull(e.termdate, '9999-01-01') >= d.MonthEndDate and d.Date < '2014-01-01'
  and p.PayGroup = e.PayGroup
  and b.UNIT = e.Unit and [EmplID] % 2 = 0
union all
--seps
SELECT dateadd(year, 1, d.date) Date
    ,Market BU
      ,[EmplID]
      ,iif([Gender]='M', 'C', 'D') Gender
      ,[Age] - (2013 - year(d.date)) Age
      ,[EthnicGroup]
      ,[FP]
      ,dateadd(year, 1,[SenDate]) HireDate
      ,p.PayTypeID
      ,dateadd(year, 1, [TermDate]) [TermDate]
      ,t.[SeparationTypeID] [TermReason]
  FROM [IP].[HR].[AllEmps] E, [HR].[Date] d , [HR].[BU] b, hr.PayGroup p , hr.TermReason t
 where d.day = 1 and e.TermDate <= d.MonthEndDate and e.TermDate >= d.MonthStartDate and d.Date < '2014-01-01'
  and p.PayGroup = e.PayGroup 
  and t.[Term-Discharge]= e.[Term-Discharge]
  and b.UNIT = e.Unit and [EmplID] % 2 = 0
```

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Sql.Database(".", "IP", [Query="SELECT dateadd(year, 1, d.date) Date#(lf)  ,Market BU#(lf)  ,[EmplID]#(lf)  ,iif([Gender]='M', 'C', 'D') Gender --  ,iif([Gender]='M', 'F', 'M') Gender#(lf)  ,[Age] - (2013 - year(d.date)) Age#(lf)  ,[EthnicGroup]#(lf)  ,[FP]#(lf)  ,dateadd(year, 1, [SenDate]) HireDate#(lf)  ,p.PayTypeID#(lf)  ,null [TermDate]#(lf)  ,null [TermReason]#(lf) FROM [IP].[HR].[AllEmps] E , [HR].[Date] d , [HR].[BU] b , hr.PayGroup p --, hr.TermReason t#(lf) where d.day = 1 and e.SenDate <= d.MonthEndDate and isnull(e.termdate, '9999-01-01') >= d.MonthEndDate and d.Date < '2014-01-01'#(lf)  and p.PayGroup = e.PayGroup#(lf)  and b.UNIT = e.Unit and [EmplID] % 2 = 0#(lf)union all#(lf)--seps#(lf)SELECT dateadd(year, 1, d.date) Date#(lf)    ,Market BU#(lf)      ,[EmplID]#(lf)      ,iif([Gender]='M', 'C', 'D') Gender#(lf)      ,[Age] - (2013 - year(d.date)) Age#(lf)      ,[EthnicGroup]#(lf)      ,[FP]#(lf)      ,dateadd(year, 1,[SenDate]) HireDate#(lf)      ,p.PayTypeID#(lf)      ,dateadd(year, 1, [TermDate]) [TermDate]#(lf)      ,t.[SeparationTypeID] [TermReason]#(lf)  FROM [IP].[HR].[AllEmps] E, [HR].[Date] d , [HR].[BU] b, hr.PayGroup p , hr.TermReason t#(lf) where d.day = 1 and e.TermDate <= d.MonthEndDate and e.TermDate >= d.MonthStartDate and d.Date < '2014-01-01'#(lf)  and p.PayGroup = e.PayGroup #(lf)  and t.[Term-Discharge]= e.[Term-Discharge]#(lf)  and b.UNIT = e.Unit and [EmplID] % 2 = 0"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"date", "date"}, {"EmplID", "EmplID"}, {"Gender", "Gender"}, {"Age", "Age"}, {"EthnicGroup", "EthnicGroup"}, {"FP", "FP"}, {"TermDate", "TermDate"}, {"BU", "BU"}, {"HireDate", "HireDate"}, {"PayTypeID", "PayTypeID"}, {"TermReason", "TermReason"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"date", type datetime}, {"EmplID", Int64.Type}, {"Gender", type text}, {"Age", Int64.Type}, {"EthnicGroup", type text}, {"FP", type text}, {"TermDate", type datetime}, {"BU", type text}, {"HireDate", type datetime}, {"PayTypeID", type text}, {"TermReason", type text}})
in
    #"Changed Type"
```

</details>

### `Ethnicity` → `DBT_SEED` (complexity=low; tags=embedded_seed)

Raw file: `04_m_raw/Ethnicity.m`

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUXIvyi8tUHBUitWJVjKC853AfGM43xnMN4HzXcB8UzjfFcw3g/PdwHxzON9dKTYWAA==", BinaryEncoding.Base64), Compression.Deflate))),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Column1", "Ethnic Group"}, {"Column2", "Ethnicity"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"Ethnic Group", type text}, {"Ethnicity", type text}})
 in
    #"Changed Type"
```

</details>

### `Gender` → `DBT_SEED` (complexity=low; tags=embedded_seed)

Raw file: `04_m_raw/Gender.m`

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WclHSUfJNzEkFUoZKsTrRSs5AlltqLkTISCk2FgA=", BinaryEncoding.Base64), Compression.Deflate))),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Column1", "ID"}, {"Column2", "Gender"}, {"Column3", "Sort"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"ID", type text}, {"Gender", type text}, {"Sort", Int64.Type}})
 in
    #"Changed Type"
```

</details>

### `AgeGroup` → `DBT_SEED` (complexity=low; tags=embedded_seed)

Raw file: `04_m_raw/AgeGroup.m`

<details><summary>Full M expression</summary>

```powerquery
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUYopNTAwTjY2UIrViVYyAgoYG+iaWIJ5xkCeqYG2UmwsAA==", BinaryEncoding.Base64), Compression.Deflate))),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Column1", "AgeGroupID"}, {"Column2", "AgeGroup"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"AgeGroupID", Int64.Type}, {"AgeGroup", type text}})
 in
    #"Changed Type"
```

</details>

## TM schema extras

### Non-empty

- `tmschema_partitions` (122 records)
- `tmschema_hierarchies` (7 records)
- `tmschema_levels` (27 records)
- `tmschema_annotations` (158 records)
- `tmschema_cultures` (1 records)
- `tmschema_variations` (5 records)
- `tmschema_attribute_hierarchies` (102 records)
- `tmschema_model` (1 records)
- `tmschema_linguistic_metadata` (1 records)
- `metadata` (3 records)

### Empty (confirmed NONE_IN_SOURCE)

- `tmschema_datasources`
- `tmschema_kpis`
- `tmschema_calendars`
- `tmschema_calendar_column_groups`
- `tmschema_calendar_column_refs`
- `tmschema_format_string_definitions`
- `tmschema_perspectives`
- `tmschema_perspective_tables`
- `tmschema_perspective_columns`
- `tmschema_perspective_measures`
- `tmschema_perspective_hierarchies`
- `tmschema_translations`
- `tmschema_calculation_groups`
- `tmschema_calculation_items`
- `tmschema_calculation_expressions`
- `tmschema_functions`
- `tmschema_sets`
- `tmschema_extended_properties`
- `tmschema_detail_rows_definitions`
- `tmschema_refresh_policies`
- `tmschema_query_groups`
- `tmschema_binding_info`
- `tmschema_role_memberships`
- `tmschema_column_permissions`
- `aggregations`
- `perspectives`
- `connections`
- `rls`
- `ols`

## Artifact index

| File | Description |
|---|---|
| `01_tables_columns.json` | Tables, columns, stats, TM columns |
| `02_dax_objects.json` | Measures, calc columns, calc tables |
| `03_relationships.json` | Relationships |
| `04_power_query_m.json` | M metadata + embedded SQL |
| `04_m_raw/*.m` | Verbatim M per table |
| `05_tmschema_extras.json` | Partitions, hierarchies, RLS, etc. |
| `ACTION_MATRIX.csv` | Every object → Looker/dbt/SKIP action |
| `OBJECT_INVENTORY.md` | This document |

## What to do next in Looker / dbt

1. **dbt:** Implement all `DBT_SQL` / `DBT_SEED` rows (especially Employee M SQL + calc columns).
2. **LookML views/joins:** Cover all `LOOKML_VIEW_*` and `LOOKML_JOIN` rows.
3. **Complex measures:** Hand-implement each `LOOKML_TODO_COMPLEX` (SPLY, EmpCount period max, TO % Norm).
4. **Skip:** `SKIP_PBI_INTERNAL` auto date tables unless product requires them.
5. **Ignore:** `NONE_IN_SOURCE` categories (nothing to migrate).

