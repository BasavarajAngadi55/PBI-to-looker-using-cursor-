# Extract Validation Proof — Phase 1

**Verdict:** `PASS`  
**Checks passed:** 15 / 15  
**Source PBIX:** `/Users/Basavaraj_Angadi/Desktop/data eng /phase1/uploads/movie_rental_analysis.pbix`

Phase 1 extract is **deterministic** (no LLM). Method: compare inventory JSON against a **fresh live pbixray read**, then cross-check extract stages against each other.

## Check results

| # | Check | Status | Detail |
|---|--------|--------|--------|
| 1 | A1 tables == live pbix.tables | **PASS** | `inventory=36 live=36 missing_in_inv=[] extra_in_inv=[]` |
| 2 | A1 columns present | **PASS** | `columns=231` |
| 3 | A2 relationships == live count | **PASS** | `inventory=16 live=16` |
| 4 | A2 relationships reference known tables | **PASS** | `all from/to tables exist in schema extract` |
| 5 | A3 measures == live dax_measures | **PASS** | `inventory=5 live=5` |
| 6 | A3 calc columns == live dax_columns | **PASS** | `inventory=121 live=121` |
| 7 | A3 calc tables == live dax_tables | **PASS** | `inventory=20 live=20` |
| 8 | A3 measure expressions match (sample) | **PASS** | `checked=5 matched=5` |
| 9 | A4 power query == live count | **PASS** | `inventory=16 live=16` |
| 10 | A4 m_raw files == queries | **PASS** | `m_files=['actor', 'address', 'category', 'city', 'country', 'customer', 'film', 'film_actor', 'film_category', 'film_text', 'inventory', 'language', 'payment', 'rentat', 'staff', 'store'] queries=['actor', 'address', 'category', 'city', 'country', 'customer', 'film', 'film_actor', 'film_category', 'film_text', 'inventory', 'language', 'payment', 'rentat', 'staff', 'store']` |
| 11 | A4 m files non-empty | **PASS** | `bytes=['actor:463', 'address:569', 'category:416', 'city:436', 'country:417', 'customer:580', 'film:713', 'film_actor:419', 'film_category:425', 'film_text:410', 'inventory:448', 'language:416', 'payment:533', 'rentat:540', 'staff:617', 'store:451']` |
| 12 | A5 RLS captured as list | **PASS** | `rls_count=0` |
| 13 | A5 auto date tables captured | **PASS** | `auto_date=20` |
| 14 | Cross: calc table names align A1/A3 | **PASS** | `calculated_tables name sets equal` |
| 15 | Merger counts file present | **PASS** | `OBJECT_COUNTS.json + OBJECT_INVENTORY.md` |

## Live table list (pbixray)

```text
DateTableTemplate_a2d2931e-28fc-49d4-8f86-8eba292beccb
LocalDateTable_2da133f1-f68d-4b4b-8ac9-f0599639b604
LocalDateTable_4239b3b1-3dd6-4664-9851-e18de09a0567
LocalDateTable_50a2d13e-fe1d-4c9d-a15d-eb4645f9255d
LocalDateTable_5bb36e84-426a-46fa-a13a-582ef5d6dc26
LocalDateTable_6086d83f-4701-4a3c-bc1d-3559af3b0892
LocalDateTable_6a8a1b8a-08db-41d5-8644-a433e0a4df0b
LocalDateTable_6f8b0d1f-465a-4e1d-aeb7-5159a1a4f632
LocalDateTable_70e91751-9ad0-4624-a9f6-239b895d4c07
LocalDateTable_87276294-e462-4311-ae3b-ed5eff935d96
LocalDateTable_874aff1d-fcfb-4b81-ac6e-ffb89b0ffde4
LocalDateTable_8765a386-0fbd-4b49-b6b6-3081c9e155ce
LocalDateTable_9aade881-448f-4a31-ad80-a5a3f46b3dae
LocalDateTable_9f8673ee-bb2e-4fbb-bb1c-ec9378110b48
LocalDateTable_a8f0fb53-b463-4fac-b8e7-a889be094bc7
LocalDateTable_c928e018-84d6-4ce3-ae3b-63bafef00319
LocalDateTable_d0d09aee-878f-400a-9b99-c55fb13a7bb3
LocalDateTable_e54b6b64-66e9-4425-bfb5-60e11fa998ee
LocalDateTable_ee80cc38-2934-4181-972c-f0b7d5752b22
LocalDateTable_fc9173f0-2a64-4402-a7d0-c24da1027bc5
actor
address
category
city
country
customer
film
film_actor
film_category
film_text
inventory
language
payment
rentat
staff
store
```

## Measure expression samples

| Measure | Match | Preview |
|---------|-------|---------|
| `Revenue` | PASS | `SUM(payment[amount])` |
| `Total Films Rented` | PASS | `COUNTROWS('inventory')` |
| `Average Inventory Value` | PASS | `AVERAGE('film'[rental_rate])` |
| `Inventory Turnover Rate` | PASS | `[Total Films Rented] / [Average Inventory Value]` |
| `FilmPopularity` | PASS | `SUMX('film',COUNT(film[rental_rate]) )` |

## Relationship sample (inventory)

```json
[
  {
    "from_table": "film_actor",
    "from_column": "actor_id",
    "to_table": "actor",
    "to_column": "actor_id",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 203,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "address",
    "from_column": "city_id",
    "to_table": "city",
    "to_column": "city_id",
    "cardinality": "M:1",
    "cross_filter": "Both",
    "active": true,
    "from_key_count": 603,
    "to_key_count": null,
    "rely_on_referential_integrity": false,
    "relationship_type": "single_column"
  },
  {
    "from_table": "city",
    "from_column": "country_id",
    "to_table": "country",
    "to_column": "country_id",
    "cardinality": "M:1",
    "cross_filter": "Single",
    "active": true,
    "from_key_count": 112,
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
  "actor.m": 463,
  "address.m": 569,
  "category.m": 416,
  "city.m": 436,
  "country.m": 417,
  "customer.m": 580,
  "film.m": 713,
  "film_actor.m": 419,
  "film_category.m": 425,
  "film_text.m": 410,
  "inventory.m": 448,
  "language.m": 416,
  "payment.m": 533,
  "rentat.m": 540,
  "staff.m": 617,
  "store.m": 451
}
```

### Employee.m preview (first 400 chars)

```m

```

## Object counts (merger)

```json
{
  "tables": 36,
  "business_tables": 16,
  "internal_tables": 20,
  "columns": 231,
  "measures": 5,
  "calculated_columns": 121,
  "calculated_tables": 20,
  "relationships": 16,
  "power_query": 16,
  "m_files": 16,
  "rls_roles": 0,
  "hierarchies": 20,
  "partitions": 322,
  "auto_date_tables": 20,
  "annotations": 433,
  "sort_by_columns": 0,
  "format_strings": 63,
  "perspectives": 0,
  "display_folders": 0
}
```
