# Warehouse SQL (Phase 3)

BigQuery dialect templates derived from Phase 2 mapping (`WAREHOUSE_SQL` / `WAREHOUSE_SEED`).

Replace `YOUR_PROJECT.YOUR_DATASET` and `YOUR_PROJECT.SOURCE_DATASET` with your environment.

Do **not** treat these scripts as KPI-validated. Load → point LookML `sql_table_name` → parity test vs Power BI.

| File | Power BI object | Type |
|------|-----------------|------|
| 01_seed_age_group.sql | AgeGroup | Seed |
| 02_seed_gender.sql | Gender | Seed |
| 03_seed_ethnicity.sql | Ethnicity | Seed |
| 04_dim_fp.sql | FP | SQL |
| 05_dim_pay_type.sql | PayType | SQL |
| 06_dim_separation_reason.sql | SeparationReason | SQL |
| 07_dim_bu.sql | BU (+ Region) | SQL |
| 08_dim_date.sql | Date (+ MonthIncrementNumber) | SQL |
| 09_fact_employee.sql | Employee (+ calc cols) | SQL |
