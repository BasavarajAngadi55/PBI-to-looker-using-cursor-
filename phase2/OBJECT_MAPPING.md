# Power BI → Looker Object Mapping

**Source:** `movie_rental_analysis.pbix`  
**Model:** `movie_rental_analysis`  
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

- **measure** `payment.Revenue` → `measure:revenue` (mapped)
- **measure** `inventory.Total Films Rented` → `measure:total_films_rented` (todo)
- **measure** `inventory.Average Inventory Value` → `measure:average_inventory_value` (mapped)
- **measure** `inventory.Inventory Turnover Rate` → `measure:inventory_turnover_rate` (mapped)
- **measure** `actor.FilmPopularity` → `measure:filmpopularity` (todo)
- **view** `actor` → `views/actor.view.lkml` (mapped)
- **view** `address` → `views/address.view.lkml` (mapped)
- **view** `category` → `views/category.view.lkml` (mapped)
- **view** `city` → `views/city.view.lkml` (mapped)
- **view** `country` → `views/country.view.lkml` (mapped)
- **view** `customer` → `views/customer.view.lkml` (mapped)
- **view** `film` → `views/film.view.lkml` (mapped)
- **view** `film_actor` → `views/film_actor.view.lkml` (mapped)
- **view** `film_category` → `views/film_category.view.lkml` (mapped)
- **view** `film_text` → `views/film_text.view.lkml` (mapped)
- **view** `inventory` → `views/inventory.view.lkml` (mapped)
- **view** `language` → `views/language.view.lkml` (mapped)
- **view** `payment` → `views/payment.view.lkml` (mapped)
- **view** `rentat` → `views/rentat.view.lkml` (mapped)
- **view** `staff` → `views/staff.view.lkml` (mapped)
- **view** `store` → `views/store.view.lkml` (mapped)
- **join** `film_actor[actor_id] -> actor[actor_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `address[city_id] -> city[city_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `city[country_id] -> country[country_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `film[language_id] -> language[language_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `film_category[category_id] -> category[category_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `film[film_id] -> film_category[film_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `film[film_id] -> film_text[film_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `store[store_id] -> staff[store_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `film_actor[film_id] -> film[film_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `customer[address_id] -> address[address_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `payment[customer_id] -> customer[customer_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `customer[store_id] -> store[store_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `rentat[inventory_id] -> inventory[inventory_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `rentat[rental_id] -> payment[rental_id]` → `explore join relationship=many_to_one` (mapped)
- **join** `rentat[staff_id] -> staff[staff_id]` → `explore join relationship=many_to_one` (inactive_alias)
- **join** `inventory[film_id] -> film[film_id]` → `explore join relationship=many_to_one` (mapped)
