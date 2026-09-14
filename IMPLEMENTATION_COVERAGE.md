# IMPLEMENTATION_COVERAGE — Phase 3

Generated against Phase 1 inventory + Phase 2 mapping. **KPI parity: NOT YET VALIDATED.**

| Power BI Object Type | Object | Expected Destination | Implemented | Status | File | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| table | AgeGroup | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/age_group.view.lkml; warehouse_sql/01_seed_age_group.sql | Business table |
| table | BU | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/bu.view.lkml; warehouse_sql/07_dim_bu.sql | Business table |
| table | Date | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml; warehouse_sql/08_dim_date.sql | Business table |
| table | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | Employee | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml; warehouse_sql/09_fact_employee.sql | Business table |
| table | Ethnicity | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/ethnicity.view.lkml; warehouse_sql/03_seed_ethnicity.sql | Business table |
| table | FP | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/fp.view.lkml; warehouse_sql/04_dim_fp.sql | Business table |
| table | Gender | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/gender.view.lkml; warehouse_sql/02_seed_gender.sql | Business table |
| table | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Auto date — not migrated as business view |
| table | PayType | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/pay_type.view.lkml; warehouse_sql/05_dim_pay_type.sql | Business table |
| table | SeparationReason | LookML view + warehouse | IMPLEMENTED | IMPLEMENTED | views/separation_reason.view.lkml; warehouse_sql/06_dim_separation_reason.sql | Business table |
| column | AgeGroup.AgeGroupID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/age_group.view.lkml | Source column |
| column | AgeGroup.AgeGroup | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/age_group.view.lkml | Source column |
| column | BU.BU | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/bu.view.lkml | Source column |
| column | BU.RegionSeq | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/bu.view.lkml | Source column |
| column | BU.VP | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/bu.view.lkml | Source column |
| column | Date.Date | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.Month | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.MonthNumber | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.Period | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.PeriodNumber | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.Qtr | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.QtrNumber | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.Year | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.Day | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.MonthStartDate | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | Date.MonthEndDate | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | Source column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | Employee.date | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.EmplID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.Gender | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.Age | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.EthnicGroup | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.FP | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.TermDate | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.BU | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.HireDate | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.PayTypeID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Employee.TermReason | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | Source column |
| column | Ethnicity.Ethnic Group | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/ethnicity.view.lkml | Source column |
| column | Ethnicity.Ethnicity | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/ethnicity.view.lkml | Source column |
| column | FP.FP | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/fp.view.lkml | Source column |
| column | FP.FPDesc | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/fp.view.lkml | Source column |
| column | Gender.ID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/gender.view.lkml | Source column |
| column | Gender.Gender | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/gender.view.lkml | Source column |
| column | Gender.Sort | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/gender.view.lkml | Source column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Date | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | Internal auto date column |
| column | PayType.PayTypeID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/pay_type.view.lkml | Source column |
| column | PayType.PayType | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/pay_type.view.lkml | Source column |
| column | SeparationReason.SeparationTypeID | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/separation_reason.view.lkml | Source column |
| column | SeparationReason.SeparationReason | LookML dimension | IMPLEMENTED | IMPLEMENTED | views/separation_reason.view.lkml | Source column |
| measure | Employee.EmpCount | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.Seps | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.Actives | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.New Hires | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.AVG Tenure Days | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.AVG Tenure Months | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.AVG Age | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.Sum of BadHires | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.New Hires SPLY | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.Actives SPLY | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.Seps SPLY | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.EmpCount SPLY | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.Seps YoY Var | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Actives YoY Var | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.New Hires YoY Var | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Seps YoY % Change | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Actives YoY % Change | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.New Hires YoY % Change | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Bad Hires SPLY | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.Bad Hires YoY Var | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Bad Hires YoY % Change | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.TO % | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.TO % Norm | LookML measure | TODO | TODO | views/employee.view.lkml | COMPLEX DAX stubbed with NULL or partial; parity required |
| measure | Employee.TO % Var | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.Sep%ofActive | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.Sep%ofSMLYActives | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | Employee.BadHire%ofActives | LookML measure | IMPLEMENTED | IMPLEMENTED | views/employee.view.lkml | LookML measure present |
| measure | Employee.BadHire%ofActiveSPLY | LookML measure | PARTIAL | PARTIAL | views/employee.view.lkml | Implemented formula but depends on TODO parents or EmpCount nesting gap |
| measure | BU.Count of BU | LookML measure | IMPLEMENTED | IMPLEMENTED | views/bu.view.lkml | LookML measure present |
| measure | Date.Count of Date | LookML measure | IMPLEMENTED | IMPLEMENTED | views/date.view.lkml | LookML measure present |
| calculated_column | BU.Region | Warehouse + LookML | IMPLEMENTED | IMPLEMENTED | warehouse_sql/07_dim_bu.sql; views/bu.view.lkml | SUBSTR RegionSeq |
| calculated_column | Date.MonthIncrementNumber | Warehouse SQL | IMPLEMENTED | IMPLEMENTED | warehouse_sql/08_dim_date.sql; views/date.view.lkml | Materialized in date SQL |
| calculated_column | Employee.isNewHire | Warehouse column + LookML dim | IMPLEMENTED | IMPLEMENTED | warehouse_sql/09_fact_employee.sql; views/employee.view.lkml | Materialized on fact |
| calculated_column | Employee.AgeGroupID | Warehouse column + LookML dim | IMPLEMENTED | IMPLEMENTED | warehouse_sql/09_fact_employee.sql; views/employee.view.lkml | Materialized on fact |
| calculated_column | Employee.TenureDays | Warehouse column + LookML dim | IMPLEMENTED | IMPLEMENTED | warehouse_sql/09_fact_employee.sql; views/employee.view.lkml | Materialized on fact |
| calculated_column | Employee.TenureMonths | Warehouse column + LookML dim | IMPLEMENTED | IMPLEMENTED | warehouse_sql/09_fact_employee.sql; views/employee.view.lkml | Materialized on fact |
| calculated_column | Employee.BadHires | Warehouse column + LookML dim | IMPLEMENTED | IMPLEMENTED | warehouse_sql/09_fact_employee.sql; views/employee.view.lkml | Materialized on fact |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Year | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.MonthNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Month | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.QuarterNo | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Quarter | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_column | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Day | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §13 | On auto date table |
| calculated_table | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| calculated_table | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| calculated_table | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| calculated_table | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| calculated_table | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| calculated_table | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | SKIP_INTERNAL / no direct equivalent | SKIP_INTERNAL | SKIP_INTERNAL | §5/§13 | Auto date Calendar() table |
| relationship | Employee.date->Date.Date | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.FP->FP.FP | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.EthnicGroup->Ethnicity.Ethnic Group | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.Gender->Gender.ID | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.PayTypeID->PayType.PayTypeID | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.BU->BU.BU | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.AgeGroupID->AgeGroup.AgeGroupID | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| relationship | Employee.TermReason->SeparationReason.SeparationTypeID | LookML join | IMPLEMENTED | IMPLEMENTED | models/human_resources.model.lkml | M:1 Single |
| power_query | BU | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/07_dim_bu.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | FP | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/04_dim_fp.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | PayType | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/05_dim_pay_type.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | SeparationReason | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/06_dim_separation_reason.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | Date | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/08_dim_date.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | Employee | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/09_fact_employee.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | Ethnicity | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/03_seed_ethnicity.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | Gender | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/02_seed_gender.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| power_query | AgeGroup | Warehouse SQL/Seed | IMPLEMENTED | PARTIAL | warehouse_sql/01_seed_age_group.sql | Template SQL — SOURCE_DATASET placeholders; not executed/validated |
| hierarchy | Date.YQM | drill_fields / set | PARTIAL | PARTIAL | views/date.view.lkml (yqm_drill) | YQM approximated; not PBI UI |
| hierarchy | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| hierarchy | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| hierarchy | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| hierarchy | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| hierarchy | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| hierarchy | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29.Date Hierarchy | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | §8 | Auto date hierarchy |
| rls | None | N/A | NONE_IN_SOURCE | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §9 | No RLS in PBIX |
| partitions | 122 partitions | Warehouse refresh consideration | PARTIAL | PARTIAL | warehouse_sql/README.md | LookML has no partition object; documented in mapping §10 |
| auto_date_table | DateTableTemplate_92fd358c-bb4c-4d52-9f5b-e9a59dc2315d | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| auto_date_table | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| auto_date_table | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| auto_date_table | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| auto_date_table | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| auto_date_table | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | SKIP_INTERNAL | SKIP_INTERNAL | SKIP_INTERNAL | LOOKML_MAPPING_ASSESSMENT.md §13 | Captured Phase 1; not a LookML view |
| sort_by | None extracted | order_by_field if needed | NONE_IN_SOURCE | SKIP_INTERNAL | §11 | No sort-by in extraction |
| format | Date.Date | value_format_name | PARTIAL | PARTIAL | views/date.view.lkml | PBI format=General Date |
| format | Date.MonthStartDate | value_format_name | PARTIAL | PARTIAL | views/date.view.lkml | PBI format=General Date |
| format | Date.MonthEndDate | value_format_name | PARTIAL | PARTIAL | views/date.view.lkml | PBI format=General Date |
| format | Employee.date | value_format_name | PARTIAL | PARTIAL | views/employee.view.lkml | PBI format=General Date |
| format | Employee.TermDate | value_format_name | PARTIAL | PARTIAL | views/employee.view.lkml | PBI format=General Date |

## Status totals

- **IMPLEMENTED**: 73
- **PARTIAL**: 28
- **SKIP_INTERNAL**: 104
- **TODO**: 7

Total coverage rows: 212

## Coverage verdict

**PARTIAL** — All business objects are accounted for (view/SQL/TODO/SKIP). Warehouse SQL is template-only (placeholders). Complex measures stubbed. KPI parity not validated.
