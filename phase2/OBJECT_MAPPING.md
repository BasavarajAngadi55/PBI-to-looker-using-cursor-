# Power BI → Looker Object Mapping

**Source:** `Human Resources Sample PBIX.pbix`  
**Model:** `human_resources_sample_pbix`  
**Approach:** deterministic (Phase 2 generator; no LLM)

## Object equivalence

| Power BI | Looker | How to create |
|---|---|---|
| Table (business) | view (.view.lkml) | Create views/<name>.view.lkml with `view: <name> { sql_table_name: ... }`. Every view needs a primary_key dimension (Looker skills / symmetric aggregates). |
| Column | dimension (or dimension_group for dates) | Add `dimension: field { type: ... sql: ${TABLE}.col ;; }`. Date/time columns → `dimension_group: ... { type: time timeframes: [raw, date, week, month, quarter, year] }`. |
| Measure (DAX) | measure | Map SUM/AVERAGE/COUNT/DISTINCTCOUNT to type: sum\|average\|count\|count_distinct. Ratios → type: number + SAFE_DIVIDE. CALCULATE/time-intel → filters, period patterns, or warehouse + TODO. |
| Relationship (M:1 From→To) | explore join (relationship: many_to_one) | In the model file, `explore: fact { join: dim { type: left_outer relationship: many_to_one sql_on: ${fact.fk} = ${dim.pk} ;; } }`. Always set relationship explicitly (looker-skills). |
| Calculated column (DAX) | dimension (prefer warehouse column) | Prefer materializing in warehouse SQL, then expose as dimension. Simple row expressions may use LookML sql:; complex DAX stays as migration TODO. |
| Calculated table | view (sql_table_name or derived_table) | If the table is seeded/small, warehouse seed + standard view. Otherwise SQL derived table / NDT per lookml-view derived_table guidance. |
| Power Query M | Warehouse / ETL (not LookML) | Rebuild M transforms in the warehouse (dbt/Dataform/SQL). LookML only points sql_table_name at the finished table. |
| Hierarchy | drill_fields / sets / dimension_group timeframes | Date hierarchies → dimension_group timeframes. Attribute hierarchies → drill_fields: [year, quarter, month, day] or sets. |
| RLS / OLS | access_grant / access_filter / required_access_grants | Map roles to Looker user attributes + access_filter on explores, or access_grant on fields. |
| LocalDateTable_* / DateTableTemplate_* | Skip (use business date + dimension_group) | Do not migrate auto-date tables. Use the business date column with Looker timeframes. |
| Model / Dataset | model (.model.lkml) + connection | One model file: connection, includes, datagroup, explore(s). Prefer granular includes over wildcards (lookml-modeling-guidelines). |

## Generated objects

- **measure** `Employee.EmpCount` → `measure:empcount` (todo)
- **measure** `Employee.Seps` → `measure:seps` (todo)
- **measure** `Employee.Actives` → `measure:actives` (todo)
- **measure** `Employee.New Hires` → `measure:new_hires` (todo)
- **measure** `Employee.AVG Tenure Days` → `measure:avg_tenure_days` (todo)
- **measure** `Employee.AVG Tenure Months` → `measure:avg_tenure_months` (todo)
- **measure** `Employee.AVG Age` → `measure:avg_age` (todo)
- **measure** `Employee.Sum of BadHires` → `measure:sum_of_badhires` (todo)
- **measure** `Employee.New Hires SPLY` → `measure:new_hires_sply` (todo)
- **measure** `Employee.Actives SPLY` → `measure:actives_sply` (todo)
- **measure** `Employee.Seps SPLY` → `measure:seps_sply` (todo)
- **measure** `Employee.EmpCount SPLY` → `measure:empcount_sply` (todo)
- **measure** `Employee.Seps YoY Var` → `measure:seps_yoy_var` (todo)
- **measure** `Employee.Actives YoY Var` → `measure:actives_yoy_var` (todo)
- **measure** `Employee.New Hires YoY Var` → `measure:new_hires_yoy_var` (todo)
- **measure** `Employee.Seps YoY % Change` → `measure:seps_yoy_pct_change` (mapped)
- **measure** `Employee.Actives YoY % Change` → `measure:actives_yoy_pct_change` (mapped)
- **measure** `Employee.New Hires YoY % Change` → `measure:new_hires_yoy_pct_change` (mapped)
- **measure** `Employee.Bad Hires SPLY` → `measure:bad_hires_sply` (todo)
- **measure** `Employee.Bad Hires YoY Var` → `measure:bad_hires_yoy_var` (todo)
- **measure** `Employee.Bad Hires YoY % Change` → `measure:bad_hires_yoy_pct_change` (mapped)
- **measure** `Employee.TO %` → `measure:to_pct` (mapped)
- **measure** `Employee.TO % Norm` → `measure:to_pct_norm` (todo)
- **measure** `Employee.TO % Var` → `measure:to_pct_var` (todo)
- **measure** `Employee.Sep%ofActive` → `measure:seppctofactive` (mapped)
- **measure** `Employee.Sep%ofSMLYActives` → `measure:seppctofsmlyactives` (mapped)
- **measure** `Employee.BadHire%ofActives` → `measure:badhirepctofactives` (mapped)
- **measure** `Employee.BadHire%ofActiveSPLY` → `measure:badhirepctofactivesply` (mapped)
- **measure** `BU.Count of BU` → `measure:count_of_bu` (todo)
- **measure** `Date.Count of Date` → `measure:count_of_date` (todo)
- **view** `AgeGroup` → `views/agegroup.view.lkml` (mapped)
- **view** `BU` → `views/bu.view.lkml` (mapped)
- **view** `Date` → `views/date.view.lkml` (mapped)
- **view** `Employee` → `views/employee.view.lkml` (mapped)
- **view** `Ethnicity` → `views/ethnicity.view.lkml` (mapped)
- **view** `FP` → `views/fp.view.lkml` (mapped)
- **view** `Gender` → `views/gender.view.lkml` (mapped)
- **view** `PayType` → `views/paytype.view.lkml` (mapped)
- **view** `SeparationReason` → `views/separationreason.view.lkml` (mapped)
- **join** `Employee[date] -> Date[Date]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[FP] -> FP[FP]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[EthnicGroup] -> Ethnicity[Ethnic Group]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[Gender] -> Gender[ID]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[PayTypeID] -> PayType[PayTypeID]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[BU] -> BU[BU]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[AgeGroupID] -> AgeGroup[AgeGroupID]` → `explore join relationship=many_to_one` (mapped)
- **join** `Employee[TermReason] -> SeparationReason[SeparationTypeID]` → `explore join relationship=many_to_one` (mapped)
