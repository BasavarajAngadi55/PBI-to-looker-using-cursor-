# Power BI Data Model Diagram — Human Resources Sample

Generated from Phase 1 inventory. Includes **business**, **calculated**, and **internal auto-date** tables.

## Star schema (business relationships)

```mermaid
erDiagram
  AgeGroup {
    Int64 AgeGroupID PK
    string AgeGroup
  }
  BU {
    string BU PK
    string RegionSeq
    string VP
    string Region CALC
  }
  Date {
    datetime64[ns] Date PK
    string Month
    Int64 MonthNumber
    string Period
    Int64 PeriodNumber
    Int64 Qtr
    string QtrNumber
    Int64 Year
    Int64 Day
    datetime64[ns] MonthStartDate
    datetime64[ns] MonthEndDate
    Int64 MonthIncrementNumber CALC
  }
  Employee {
    datetime64[ns] date
    Int64 EmplID
    string Gender
    Int64 Age
    string EthnicGroup
    string FP
    datetime64[ns] TermDate
    Int64 isNewHire CALC
    string BU
    datetime64[ns] HireDate
    string PayTypeID
    string TermReason
    Int64 AgeGroupID CALC
    Float64 TenureDays CALC
    Int64 TenureMonths CALC
    Float64 BadHires CALC
  }
  Ethnicity {
    string Ethnic_Group PK
    string Ethnicity
  }
  FP {
    string FP PK
    string FPDesc
  }
  Gender {
    string ID PK
    string Gender
    Int64 Sort
  }
  PayType {
    string PayTypeID PK
    string PayType
  }
  SeparationReason {
    string SeparationTypeID PK
    string SeparationReason
  }
  Employee }o--|| Date : "date->Date (M:1)"
  Employee }o--|| FP : "FP->FP (M:1)"
  Employee }o--|| Ethnicity : "EthnicGroup->Ethnic Group (M:1)"
  Employee }o--|| Gender : "Gender->ID (M:1)"
  Employee }o--|| PayType : "PayTypeID->PayTypeID (M:1)"
  Employee }o--|| BU : "BU->BU (M:1)"
  Employee }o--|| AgeGroup : "AgeGroupID->AgeGroupID (M:1)"
  Employee }o--|| SeparationReason : "TermReason->SeparationTypeID (M:1)"
```

## Relationship inventory (all 8 — active, Single, M:1)

| # | From Table | From Column (FK) | To Table | To Column (PK side) | Cardinality | Cross-filter | Active |
|---|---|---|---|---|---|---|---|
| 1 | Employee | `date` | Date | `Date` | M:1 | Single | True |
| 2 | Employee | `FP` | FP | `FP` | M:1 | Single | True |
| 3 | Employee | `EthnicGroup` | Ethnicity | `Ethnic Group` | M:1 | Single | True |
| 4 | Employee | `Gender` | Gender | `ID` | M:1 | Single | True |
| 5 | Employee | `PayTypeID` | PayType | `PayTypeID` | M:1 | Single | True |
| 6 | Employee | `BU` | BU | `BU` | M:1 | Single | True |
| 7 | Employee | `AgeGroupID` | AgeGroup | `AgeGroupID` | M:1 | Single | True |
| 8 | Employee | `TermReason` | SeparationReason | `SeparationTypeID` | M:1 | Single | True |

## Business tables — columns & keys

### `AgeGroup` (business)

- **Logical key / grain:** AgeGroupID
- **Column count:** 2

| Column | Type | Calculated | Role |
|---|---|---|---|
| `AgeGroupID` | Int64 | No | PK, PK-side (joined from Employee) |
| `AgeGroup` | string | No | attr |

### `BU` (business)

- **Logical key / grain:** BU
- **Column count:** 4

| Column | Type | Calculated | Role |
|---|---|---|---|
| `BU` | string | No | PK, PK-side (joined from Employee) |
| `RegionSeq` | string | No | attr |
| `VP` | string | No | attr |
| `Region` | string | Yes | DAX calc |

### `Date` (business)

- **Logical key / grain:** Date
- **Column count:** 12

| Column | Type | Calculated | Role |
|---|---|---|---|
| `Date` | datetime64[ns] | No | PK, PK-side (joined from Employee) |
| `Month` | string | No | attr |
| `MonthNumber` | Int64 | No | attr |
| `Period` | string | No | attr |
| `PeriodNumber` | Int64 | No | attr |
| `Qtr` | Int64 | No | attr |
| `QtrNumber` | string | No | attr |
| `Year` | Int64 | No | attr |
| `Day` | Int64 | No | attr |
| `MonthStartDate` | datetime64[ns] | No | attr |
| `MonthEndDate` | datetime64[ns] | No | attr |
| `MonthIncrementNumber` | Int64 | Yes | DAX calc |

### `Employee` (business)

- **Logical key / grain:** (grain: EmplID + date) — no single PK in PBIX
- **Column count:** 16

| Column | Type | Calculated | Role |
|---|---|---|---|
| `date` | datetime64[ns] | No | FK → Date.Date |
| `EmplID` | Int64 | No | attr |
| `Gender` | string | No | FK → Gender.ID |
| `Age` | Int64 | No | attr |
| `EthnicGroup` | string | No | FK → Ethnicity.Ethnic Group |
| `FP` | string | No | FK → FP.FP |
| `TermDate` | datetime64[ns] | No | attr |
| `isNewHire` | Int64 | Yes | DAX calc |
| `BU` | string | No | FK → BU.BU |
| `HireDate` | datetime64[ns] | No | attr |
| `PayTypeID` | string | No | FK → PayType.PayTypeID |
| `TermReason` | string | No | FK → SeparationReason.SeparationTypeID |
| `AgeGroupID` | Int64 | Yes | FK → AgeGroup.AgeGroupID, DAX calc |
| `TenureDays` | Float64 | Yes | DAX calc |
| `TenureMonths` | Int64 | Yes | DAX calc |
| `BadHires` | Float64 | Yes | DAX calc |

### `Ethnicity` (business)

- **Logical key / grain:** Ethnic Group
- **Column count:** 2

| Column | Type | Calculated | Role |
|---|---|---|---|
| `Ethnic Group` | string | No | PK, PK-side (joined from Employee) |
| `Ethnicity` | string | No | attr |

### `FP` (business)

- **Logical key / grain:** FP
- **Column count:** 2

| Column | Type | Calculated | Role |
|---|---|---|---|
| `FP` | string | No | PK, PK-side (joined from Employee) |
| `FPDesc` | string | No | attr |

### `Gender` (business)

- **Logical key / grain:** ID
- **Column count:** 3

| Column | Type | Calculated | Role |
|---|---|---|---|
| `ID` | string | No | PK, PK-side (joined from Employee) |
| `Gender` | string | No | attr |
| `Sort` | Int64 | No | attr |

### `PayType` (business)

- **Logical key / grain:** PayTypeID
- **Column count:** 2

| Column | Type | Calculated | Role |
|---|---|---|---|
| `PayTypeID` | string | No | PK, PK-side (joined from Employee) |
| `PayType` | string | No | attr |

### `SeparationReason` (business)

- **Logical key / grain:** SeparationTypeID
- **Column count:** 2

| Column | Type | Calculated | Role |
|---|---|---|---|
| `SeparationTypeID` | string | No | PK, PK-side (joined from Employee) |
| `SeparationReason` | string | No | attr |

## Calculated columns (business) — DAX

| Table | Column | DAX |
|---|---|---|
| BU | `Region` | `mid([RegionSeq], 3,15)` |
| Date | `MonthIncrementNumber` | `([Year]-MIN([Year]))*12 +[MonthNumber]` |
| Employee | `isNewHire` | `IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)` |
| Employee | `AgeGroupID` | `IF([Age]<30, 1, IF([Age]<50, 2, 3))` |
| Employee | `TenureDays` | `IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])` |
| Employee | `TenureMonths` | `CEILING([TenureDays]/30, 1) -1` |
| Employee | `BadHires` | `IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)` |

## Internal / calculated auto-date tables

Power BI auto time-intelligence tables. **No relationships** to business tables in `03_relationships.json` (hidden TI). Captured for completeness; LookML migration = SKIP_INTERNAL.

| Internal Table | Type | Columns | Calculated cols | Hierarchy |
|---|---|---:|---:|---|
| `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d` | calculated_table | 7 | 6 | Date Hierarchy |
| `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782` | calculated_table | 7 | 6 | Date Hierarchy |
| `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29` | calculated_table | 7 | 6 | Date Hierarchy |
| `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac` | calculated_table | 7 | 6 | Date Hierarchy |
| `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b` | calculated_table | 7 | 6 | Date Hierarchy |
| `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6` | calculated_table | 7 | 6 | Date Hierarchy |

### Typical auto-date columns

Example from `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782`:

| Column | Type | Calculated |
|---|---|---|
| `Date` | datetime64[ns] | No |
| `Year` | Int64 | Yes |
| `MonthNo` | Int64 | Yes |
| `Month` | string | Yes |
| `QuarterNo` | Int64 | Yes |
| `Quarter` | string | Yes |
| `Day` | Int64 | Yes |

### Calculated table DAX (Calendar)

#### `DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d`

```dax
Calendar(Date(2015,1,1), Date(2015,1,1))
```

#### `LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782`

```dax
Calendar(Date(Year(MIN('Date'[Date])), 1, 1), Date(Year(MAX('Date'[Date])), 12, 31))
```

#### `LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6`

```dax
Calendar(Date(Year(MIN('Date'[MonthStartDate])), 1, 1), Date(Year(MAX('Date'[MonthStartDate])), 12, 31))
```

#### `LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac`

```dax
Calendar(Date(Year(MIN('Date'[MonthEndDate])), 1, 1), Date(Year(MAX('Date'[MonthEndDate])), 12, 31))
```

#### `LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b`

```dax
Calendar(Date(Year(MIN('Employee'[TermDate])), 1, 1), Date(Year(MAX('Employee'[TermDate])), 12, 31))
```

#### `LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29`

```dax
Calendar(Date(Year(MIN('Employee'[HireDate])), 1, 1), Date(Year(MAX('Employee'[HireDate])), 12, 31))
```

## Model notes

1. **Fact:** `Employee` — monthly snapshot grain (`date` × `EmplID`).
2. **All 8 relationships** are many-to-one from Employee → dimensions, active, single-direction cross-filter.
3. **AgeGroupID** on Employee is a calculated column used as FK to AgeGroup.
4. **Internal LocalDateTable_*** / **DateTableTemplate_*** are auto-generated; not part of the business star.
5. **RLS:** none in this PBIX.
