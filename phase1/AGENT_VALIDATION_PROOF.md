# Extract Validation Proof — Phase 1

**Verdict:** `PASS`  
**Checks passed:** 15 / 15  
**Source PBIX:** `/Users/Basavaraj_Angadi/Desktop/data eng /phase1/uploads/Human Resources Sample PBIX.pbix`

Phase 1 extract is **deterministic** (no LLM). Method: compare inventory JSON against a **fresh live pbixray read**, then cross-check extract stages against each other.

## Check results

| # | Check | Status | Detail |
|---|--------|--------|--------|
| 1 | A1 tables == live pbix.tables | **PASS** | `inventory=15 live=15 missing_in_inv=[] extra_in_inv=[]` |
| 2 | A1 columns present | **PASS** | `columns=87` |
| 3 | A2 relationships == live count | **PASS** | `inventory=8 live=8` |
| 4 | A2 relationships reference known tables | **PASS** | `all from/to tables exist in schema extract` |
| 5 | A3 measures == live dax_measures | **PASS** | `inventory=30 live=30` |
| 6 | A3 calc columns == live dax_columns | **PASS** | `inventory=43 live=43` |
| 7 | A3 calc tables == live dax_tables | **PASS** | `inventory=6 live=6` |
| 8 | A3 measure expressions match (sample) | **PASS** | `checked=5 matched=5` |
| 9 | A4 power query == live count | **PASS** | `inventory=9 live=9` |
| 10 | A4 m_raw files == queries | **PASS** | `m_files=['AgeGroup', 'BU', 'Date', 'Employee', 'Ethnicity', 'FP', 'Gender', 'PayType', 'SeparationReason'] queries=['AgeGroup', 'BU', 'Date', 'Employee', 'Ethnicity', 'FP', 'Gender', 'PayType', 'SeparationReason']` |
| 11 | A4 m files non-empty | **PASS** | `bytes=['AgeGroup:443', 'BU:411', 'Date:805', 'Employee:2114', 'Ethnicity:468', 'FP:316', 'Gender:453', 'PayType:380', 'SeparationReason:449']` |
| 12 | A5 RLS captured as list | **PASS** | `rls_count=0` |
| 13 | A5 auto date tables captured | **PASS** | `auto_date=6` |
| 14 | Cross: calc table names align A1/A3 | **PASS** | `calculated_tables name sets equal` |
| 15 | Merger counts file present | **PASS** | `OBJECT_COUNTS.json + OBJECT_INVENTORY.md` |

## Live table list (pbixray)

```text
AgeGroup
BU
Date
DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d
Employee
Ethnicity
FP
Gender
LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782
LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29
LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac
LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b
LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6
PayType
SeparationReason
```

## Measure expression samples

| Measure | Match | Preview |
|---------|-------|---------|
| `EmpCount` | PASS | `CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber...` |
| `Seps` | PASS | `CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))` |
| `Actives` | PASS | `CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))` |
| `New Hires` | PASS | `SUM([isNewHire])` |
| `AVG Tenure Days` | PASS | `AVERAGE([TenureDays])` |

## Relationship sample (inventory)

```json
[
  {
    "from_table": "Employee",
    "from_column": "date",
    "to_table": "Date",
    "to_column": "Date",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 51,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "Employee",
    "from_column": "FP",
    "to_table": "FP",
    "to_column": "FP",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 5,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "Employee",
    "from_column": "EthnicGroup",
    "to_table": "Ethnicity",
    "to_column": "Ethnic Group",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 10,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  }
]
```

## Power Query M proof

### File sizes

```json
{
  "AgeGroup.m": 443,
  "BU.m": 411,
  "Date.m": 805,
  "Employee.m": 2114,
  "Ethnicity.m": 468,
  "FP.m": 316,
  "Gender.m": 453,
  "PayType.m": 380,
  "SeparationReason.m": 449
}
```

### Employee.m preview (first 400 chars)

```m
let
    Source = Sql.Database(".", "IP", [Query="SELECT dateadd(year, 1, d.date) Date#(lf)  ,Market BU#(lf)  ,[EmplID]#(lf)  ,iif([Gender]='M', 'C', 'D') Gender --  ,iif([Gender]='M', 'F', 'M') Gender#(lf)  ,[Age] - (2013 - year(d.date)) Age#(lf)  ,[EthnicGroup]#(lf)  ,[FP]#(lf)  ,dateadd(year, 1, [SenDate]) HireDate#(lf)  ,p.PayTypeID#(lf)  ,null [TermDate]#(lf)  ,null [TermReason]#(lf) FROM [IP]
```

## Object counts (merger)

```json
{
  "tables": 15,
  "business_tables": 9,
  "internal_tables": 6,
  "columns": 87,
  "measures": 30,
  "calculated_columns": 43,
  "calculated_tables": 6,
  "relationships": 8,
  "power_query": 9,
  "m_files": 9,
  "rls_roles": 0,
  "hierarchies": 7,
  "partitions": 122,
  "auto_date_tables": 6,
  "annotations": 158,
  "sort_by_columns": 0,
  "format_strings": 5,
  "perspectives": 0,
  "display_folders": 0
}
```
