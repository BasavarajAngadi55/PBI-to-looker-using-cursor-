# Extract Validation Proof — Phase 1

**Verdict:** `FAIL`  
**Checks passed:** 14 / 15  
**Source PBIX:** `/Users/Basavaraj_Angadi/Desktop/data eng /phase1/uploads/dashboards.pbix`

Phase 1 extract is **deterministic** (no LLM). Method: compare inventory JSON against a **fresh live pbixray read**, then cross-check extract stages against each other.

## Check results

| # | Check | Status | Detail |
|---|--------|--------|--------|
| 1 | A1 tables == live pbix.tables | **PASS** | `inventory=18 live=18 missing_in_inv=[] extra_in_inv=[]` |
| 2 | A1 columns present | **PASS** | `columns=152` |
| 3 | A2 relationships == live count | **PASS** | `inventory=10 live=10` |
| 4 | A2 relationships reference known tables | **PASS** | `all from/to tables exist in schema extract` |
| 5 | A3 measures == live dax_measures | **PASS** | `inventory=32 live=32` |
| 6 | A3 calc columns == live dax_columns | **PASS** | `inventory=63 live=63` |
| 7 | A3 calc tables == live dax_tables | **PASS** | `inventory=8 live=8` |
| 8 | A3 measure expressions match (sample) | **PASS** | `checked=5 matched=5` |
| 9 | A4 power query == live count | **PASS** | `inventory=11 live=11` |
| 10 | A4 m_raw files == queries | **FAIL** | `m_files=['CptCode_Lookup', 'DiagnosisCode_Lookup', 'DimDate', 'FactTable', 'Hospital_Lookup', 'Measure_Table', 'Patient_Lookup', 'Payer_Lookup', 'Physcian_Lookup', 'Speciality_Lookup', 'Trancstion_Lookup'] queries=['CptCode_Lookup', 'DiagnosisCode_Lookup', 'DimDate', 'FactTable', 'Hospital_Lookup', 'Measure Table', 'Patient_Lookup', 'Payer_Lookup', 'Physcian_Lookup', 'Speciality_Lookup', 'Trancstion_Lookup']` |
| 11 | A4 m files non-empty | **PASS** | `bytes=['CptCode_Lookup:474', 'DiagnosisCode_Lookup:516', 'DimDate:1713', 'FactTable:1443', 'Hospital_Lookup:566', 'Measure_Table:414', 'Patient_Lookup:943', 'Payer_Lookup:420', 'Physcian_Lookup:628', 'Speciality_Lookup:772', 'Trancstion_Lookup:498']` |
| 12 | A5 RLS captured as list | **PASS** | `rls_count=0` |
| 13 | A5 auto date tables captured | **PASS** | `auto_date=6` |
| 14 | Cross: calc table names align A1/A3 | **PASS** | `calculated_tables name sets equal` |
| 15 | Merger counts file present | **PASS** | `OBJECT_COUNTS.json + OBJECT_INVENTORY.md` |

## Live table list (pbixray)

```text
Adjustment factor (%)
BadDebtTable
CptCode_Lookup
DateTableTemplate_be97c3f8-f201-4a00-a952-d6592f333bdd
DiagnosisCode_Lookup
DimDate
FactTable
Hospital_Lookup
LocalDateTable_2c2a61ff-39c4-4f0c-97ac-a6a7efb97db4
LocalDateTable_39bba987-77ed-4008-8322-dd29e2cc2f25
LocalDateTable_a249ec34-7878-4151-b4c2-6a7b636bf3c0
LocalDateTable_d31a6fc7-dba3-4410-a53a-de9bb2d5b1c2
LocalDateTable_ef34a3ff-4085-4eda-a1df-b58a8db8be46
Patient_Lookup
Payer_Lookup
Physcian_Lookup
Speciality_Lookup
Trancstion_Lookup
```

## Measure expression samples

| Measure | Match | Preview |
|---------|-------|---------|
| `TotalInsurancePay` | PASS | `SUM(FactTable[Insurance_Payment])` |
| `TotalPatientPay` | PASS | `SUM(FactTable[Patient_Payment])` |
| `AverageInsurancePay` | PASS | `AVERAGE(FactTable[Insurance_Payment])` |
| `AveragePatientPay` | PASS | `AVERAGE(FactTable[Patient_Payment])` |
| `TotalPayment` | PASS | `SUM(FactTable[Insurance_Payment]) + SUM(FactTable[Patient_Payment])` |

## Relationship sample (inventory)

```json
[
  {
    "from_table": "FactTable",
    "from_column": "dimCPTCodeFK",
    "to_table": "CptCode_Lookup",
    "to_column": "dimCPTCodePK",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 1259,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "FactTable",
    "from_column": "dimDiagnosisCodeFK",
    "to_table": "DiagnosisCode_Lookup",
    "to_column": "dimDiagnosisCodePK",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 4804,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "FactTable",
    "from_column": "dimHospitalFK",
    "to_table": "Hospital_Lookup",
    "to_column": "dimHospitalPK",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 14,
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
  "CptCode_Lookup.m": 474,
  "DiagnosisCode_Lookup.m": 516,
  "DimDate.m": 1713,
  "FactTable.m": 1443,
  "Hospital_Lookup.m": 566,
  "Measure_Table.m": 414,
  "Patient_Lookup.m": 943,
  "Payer_Lookup.m": 420,
  "Physcian_Lookup.m": 628,
  "Speciality_Lookup.m": 772,
  "Trancstion_Lookup.m": 498
}
```

### Employee.m preview (first 400 chars)

```m

```

## Object counts (merger)

```json
{
  "tables": 18,
  "business_tables": 12,
  "internal_tables": 6,
  "columns": 152,
  "measures": 32,
  "calculated_columns": 63,
  "calculated_tables": 8,
  "relationships": 10,
  "power_query": 11,
  "m_files": 11,
  "rls_roles": 0,
  "hierarchies": 6,
  "partitions": 192,
  "auto_date_tables": 6,
  "annotations": 254,
  "sort_by_columns": 0,
  "format_strings": 52,
  "perspectives": 0,
  "display_folders": 0
}
```
