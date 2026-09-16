# Power BI page → Looker dashboard comparison

**Source:** `movie_rental_analysis.pbix`  
**Looker model/explore:** `movie_rental_analysis` / `film`  
**Weighted completion:** **75.1%** (target ≥ 70%: YES)

## Status summary

- Total visuals: 173 (decorative skips: 0)
- Status counts: {'gap': 4, 'partial': 99, 'mapped': 70}

## Visual type equivalence

| Power BI | Looker | Status | Notes |
|---|---|---|---|
| `card` | `single_value` | mapped | KPI card → single_value tile |
| `kpi` | `single_value` | partial | KPI with goal/trend → single_value (goal/trend not fully mirrored) |
| `columnChart` | `looker_column` | mapped | Column chart → looker_column |
| `clusteredColumnChart` | `looker_column` | mapped | Clustered columns → looker_column |
| `clusteredBarChart` | `looker_bar` | mapped | Bar chart → looker_bar |
| `barChart` | `looker_bar` | mapped | Bar chart → looker_bar |
| `lineChart` | `looker_line` | mapped | Line chart → looker_line |
| `areaChart` | `looker_area` | mapped | Area chart → looker_area |
| `stackedAreaChart` | `looker_area` | partial | Stacked area → looker_area (stacking may differ) |
| `pieChart` | `looker_pie` | mapped | Pie → looker_pie |
| `donutChart` | `looker_pie` | partial | Donut → looker_pie (donut style limited) |
| `pivotTable` | `looker_grid` | mapped | Matrix/pivot → looker_grid |
| `tableEx` | `looker_grid` | mapped | Table → looker_grid |
| `table` | `looker_grid` | mapped | Table → looker_grid |
| `slicer` | `dashboard filter` | mapped | Slicer → dashboard filter (not a tile) |
| `textbox` | `text` | partial | Text box → text tile (rich formatting limited) |
| `shape` | `skip` | skip | Decorative shape — no Looker equivalent (skip) |
| `image` | `manual` | gap | Image tile — not auto-ported; add manually or as text note |
| `actionButton` | `button/gap` | gap | Action button — Looker button needs explicit URL; stub as note |
| `map` | `looker_map` | partial | Map → looker_map if geo fields exist; else gap |
| `filledMap` | `looker_google_map` | partial | Filled map → google map / choropleth if supported |
| `treemap` | `looker_pie (substitute)` | partial | Treemap has no direct Looker twin → pie/column substitute |
| `lineStackedColumnComboChart` | `looker_column (partial)` | partial | Combo chart → looker_column or looker_line (combo not 1:1) |
| `waterfallChart` | `looker_waterfall` | mapped | Waterfall → looker_waterfall |
| `funnel` | `looker_funnel` | mapped | Funnel → looker_funnel |
| `scatterChart` | `looker_scatter` | mapped | Scatter → looker_scatter |

## Page: Overview

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| pageNavigator_0 | `pageNavigator` | `gap` | gap | - |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |
| textbox_3 | `textbox` | `text` | partial | - |
| textbox_4 | `textbox` | `text` | partial | - |
| textbox_5 | `textbox` | `text` | partial | - |
| textbox_6 | `textbox` | `text` | partial | - |
| textbox_7 | `textbox` | `text` | partial | - |

## Page: Geographic / Location Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| country | `map` | `looker_map` | partial | map may lack location dimension — verify geo fields |
| textbox_1 | `textbox` | `text` | partial | - |
| Location wise Customer Ratings | `columnChart` | `looker_column` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
|  Distribution of Customers across Countries | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| Revenue | `card` | `single_value` | mapped | - |
| rental_rate | `card` | `single_value` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| rental_duration | `card` | `single_value` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| city | `slicer` | `dashboard filter` | mapped | - |
| country | `slicer` | `dashboard filter` | mapped | - |
| Rental Frequency | `card` | `single_value` | mapped | PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| Rental Rate & Rental Duration By Country | `tableEx` | `looker_grid` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum; PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Rental Revenue by Country | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |

## Page: Revenue Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Rental Revenue by Country | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| Revenue by Month | `lineChart` | `looker_line` | mapped | unbound field payment_date Year; unbound field payment_date Month |
| name | `treemap` | `looker_pie (substitute)` | partial | - |
| Revenue & Inventory Distribution by Category | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | PBI aggregation on rentat.inventory_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| Revenue | `card` | `single_value` | mapped | - |
| Revenue by Rating | `donutChart` | `looker_pie` | partial | - |
| Revenue | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | - |
| Rental Frequency | `card` | `single_value` | mapped | PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| rental_rate | `card` | `single_value` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| rental_duration | `card` | `single_value` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| rental_id | `card` | `single_value` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| slicer_12 | `slicer` | `dashboard filter` | gap | unbound field payment_date Year; slicer has no bound field |

## Page: Customer Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| Active/Inactive Customer: | `donutChart` | `looker_pie` | partial | PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| Active/Inactive(1/0) Customer Details: | `tableEx` | `looker_grid` | mapped | PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| name | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| Customers by Country | `map` | `looker_map` | partial | PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum; map may lack location dimension — verify geo fields |
| customer_id | `card` | `single_value` | mapped | PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| Rental Rate by Customers | `columnChart` | `looker_column` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Distribution of Customers by Rating | `columnChart` | `looker_column` | mapped | PBI aggregation on payment.customer_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| Revenue | `card` | `single_value` | mapped | - |
| Rental Frequency | `card` | `single_value` | mapped | PBI aggregation on payment.payment_id mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |
| rental_rate | `card` | `single_value` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| category_id | `slicer` | `dashboard filter` | mapped | - |

## Page: Rental Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| Films Distribution by Rental Duration (In Months) | `clusteredColumnChart` | `looker_column` | mapped | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Average of rental_duration by Film-category | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Rental Rates of Films | `treemap` | `looker_pie (substitute)` | partial | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Total Rentals | `card` | `single_value` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| rental_duration | `card` | `single_value` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| rental_rate | `card` | `single_value` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Rental Distribution  by Year | `pieChart` | `looker_pie` | mapped | unbound field rental_date Year; unbound field rental_date Month |
| Rentals by Customer  | `pivotTable` | `looker_grid` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| Rentals by Film Title | `pivotTable` | `looker_grid` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| Revenue | `card` | `single_value` | mapped | - |
| slicer_11 | `slicer` | `dashboard filter` | gap | unbound field rental_date Year; slicer has no bound field |

## Page: Film Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| Film Distribution by Language | `card` | `single_value` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Film-Category breakdown in Inventory | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add type:sum |
| Inventory Variation by Film-Ratings | `donutChart` | `looker_pie` | partial | PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add type:sum |
| Rentals Distribution by Films | `lineClusteredColumnComboChart` | `gap` | gap | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |
| rating | `donutChart` | `looker_pie` | partial | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Revenue and Rental Rate by Film Category | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| film_id | `tableEx` | `looker_grid` | mapped | PBI aggregation on film.length mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Average of Rental Duration | `card` | `single_value` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Film Ratings | `slicer` | `dashboard filter` | mapped | - |
| actor_id | `card` | `single_value` | mapped | PBI aggregation on actor.actor_id mapped to field ref; confirm a measure exists on actor (Phase 2) or add type:sum |
| film_id | `card` | `single_value` | mapped | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| title | `slicer` | `dashboard filter` | mapped | - |
| Description | `card` | `single_value` | mapped | PBI aggregation on film.description mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Actor Analysis

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| DIstribution of Films by Actors | `barChart` | `looker_bar` | mapped | PBI aggregation on film_actor.film_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type:sum |
| Revenue Contribution by Actors | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | - |
| Actor wise Rental Rate Variation  | `lineChart` | `looker_line` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| Actor Details | `tableEx` | `looker_grid` | mapped | - |
| film_id | `card` | `single_value` | mapped | PBI aggregation on film_category.film_id mapped to field ref; confirm a measure exists on film_category (Phase 2) or add type:sum |
| actor_id | `card` | `single_value` | mapped | PBI aggregation on actor.actor_id mapped to field ref; confirm a measure exists on actor (Phase 2) or add type:sum |
| first_name | `slicer` | `dashboard filter` | mapped | - |
| Revenue | `card` | `single_value` | mapped | - |
| Genre Preferences of Actors | `donutChart` | `looker_pie` | partial | PBI aggregation on film_actor.actor_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type:sum |

## Page: Q1

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Revenue by Month | `lineChart` | `looker_line` | mapped | unbound field payment_date Year; unbound field payment_date Month |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page:  Q2

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Active/Inactive Customer: | `pieChart` | `looker_pie` | mapped | PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| Active/Inactive(1/0) Customer Details: | `tableEx` | `looker_grid` | mapped | PBI aggregation on customer.active mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |

## Page: Q3

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| name | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum |

## Page: Q4

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Distribution of Films by Rental-Duration. | `columnChart` | `looker_column` | mapped | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q5

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Inventory Variation by Film-Ratings | `donutChart` | `looker_pie` | partial | PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add type:sum |

## Page: Q6

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Film-Category breakdown in Inventory | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on inventory.inventory_id mapped to field ref; confirm a measure exists on inventory (Phase 2) or add type:sum |

## Page: Q7

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Staff Distribution by Employment Duration | `columnChart` | `looker_column` | mapped | PBI aggregation on staff.staff_id mapped to field ref; confirm a measure exists on staff (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |
| textbox_3 | `textbox` | `text` | partial | - |

## Page: Q8

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Store Performance Variation by Location | `map` | `looker_map` | partial | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum; map may lack location dimension — verify geo fields |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q9

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Average of rental_duration by staff member | `pieChart` | `looker_pie` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q10

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
|  Distribution of Customers across Cities | `columnChart` | `looker_column` | mapped | PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q11

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Rental Revenue by Country | `map` | `looker_map` | partial | PBI aggregation on payment.amount mapped to field ref; confirm a measure exists on payment (Phase 2) or add type:sum; map may lack location dimension — verify geo fields |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q12

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Location wise Customer Ratings | `columnChart` | `looker_column` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q13

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Distribution of Films by languages | `donutChart` | `looker_pie` | partial | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q14

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| Rental Rates of Films | `treemap` | `looker_pie (substitute)` | partial | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| textbox_1 | `textbox` | `text` | partial | - |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q15

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Average of rental_duration by Film-category | `lineChart` | `looker_line` | mapped | PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q16

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| Rental Rate & Rental Duration By Country | `lineChart` | `looker_line` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum; PBI aggregation on film.rental_duration mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |
| textbox_2 | `textbox` | `text` | partial | - |

## Page: Q17

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Location wise Customer Ratings | `columnChart` | `looker_column` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q18

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Revenue by Rating | `donutChart` | `looker_pie` | partial | - |

## Page: Q19

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Revenue & Inventory Distribution by Category | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | PBI aggregation on rentat.inventory_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |

## Page: Q20

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Rental Rate by Customers | `clusteredBarChart` | `looker_bar` | mapped | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q21

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| rental_id | `columnChart` | `looker_column` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |

## Page: Q22

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| DIstribution of Films by Actors | `barChart` | `looker_bar` | mapped | PBI aggregation on film_actor.film_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type:sum |

## Page: Q23

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Actor wise Rental Rate Variation  | `lineStackedColumnComboChart` | `looker_column (partial)` | partial | PBI aggregation on film.rental_rate mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q24

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Genre Preference of Actors | `donutChart` | `looker_pie` | partial | PBI aggregation on film_actor.actor_id mapped to field ref; confirm a measure exists on film_actor (Phase 2) or add type:sum |

## Page: Q25

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Revenue Contribution by Actors | `columnChart` | `looker_column` | mapped | - |

## Page: Q26

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| customer distribution by countries | `map` | `looker_map` | partial | PBI aggregation on customer.customer_id mapped to field ref; confirm a measure exists on customer (Phase 2) or add type:sum; map may lack location dimension — verify geo fields |

## Page: Q27

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Global Revenue Distribution | `map` | `looker_map` | partial | map may lack location dimension — verify geo fields |

## Page: Q28

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Film Distribution by Content Ratings: Understanding Viewer Preferences | `pieChart` | `looker_pie` | mapped | PBI aggregation on film.film_id mapped to field ref; confirm a measure exists on film (Phase 2) or add type:sum |

## Page: Q29

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Revenue Distribution by Film Category: Identifying Top Contributors | `treemap` | `looker_pie (substitute)` | partial | - |

## Page: Q30

| Power BI visual | PBI type | Looker equivalent | Status | Deficiencies |
|---|---|---|---|---|
| textbox_0 | `textbox` | `text` | partial | - |
| textbox_1 | `textbox` | `text` | partial | - |
| Customer Segment Rental Activity Analysis | `columnChart` | `looker_column` | mapped | PBI aggregation on rentat.rental_id mapped to field ref; confirm a measure exists on rentat (Phase 2) or add type:sum |

## Looker dashboard files

- `lookml_dashboards/dashboards/overview.dashboard.lookml`
- `lookml_dashboards/dashboards/geographic_location_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/revenue_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/customer_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/rental_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/film_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/actor_analysis.dashboard.lookml`
- `lookml_dashboards/dashboards/q1.dashboard.lookml`
- `lookml_dashboards/dashboards/q2.dashboard.lookml`
- `lookml_dashboards/dashboards/q3.dashboard.lookml`
- `lookml_dashboards/dashboards/q4.dashboard.lookml`
- `lookml_dashboards/dashboards/q5.dashboard.lookml`
- `lookml_dashboards/dashboards/q6.dashboard.lookml`
- `lookml_dashboards/dashboards/q7.dashboard.lookml`
- `lookml_dashboards/dashboards/q8.dashboard.lookml`
- `lookml_dashboards/dashboards/q9.dashboard.lookml`
- `lookml_dashboards/dashboards/q10.dashboard.lookml`
- `lookml_dashboards/dashboards/q11.dashboard.lookml`
- `lookml_dashboards/dashboards/q12.dashboard.lookml`
- `lookml_dashboards/dashboards/q13.dashboard.lookml`
- `lookml_dashboards/dashboards/q14.dashboard.lookml`
- `lookml_dashboards/dashboards/q15.dashboard.lookml`
- `lookml_dashboards/dashboards/q16.dashboard.lookml`
- `lookml_dashboards/dashboards/q17.dashboard.lookml`
- `lookml_dashboards/dashboards/q18.dashboard.lookml`
- `lookml_dashboards/dashboards/q19.dashboard.lookml`
- `lookml_dashboards/dashboards/q20.dashboard.lookml`
- `lookml_dashboards/dashboards/q21.dashboard.lookml`
- `lookml_dashboards/dashboards/q22.dashboard.lookml`
- `lookml_dashboards/dashboards/q23.dashboard.lookml`
- `lookml_dashboards/dashboards/q24.dashboard.lookml`
- `lookml_dashboards/dashboards/q25.dashboard.lookml`
- `lookml_dashboards/dashboards/q26.dashboard.lookml`
- `lookml_dashboards/dashboards/q27.dashboard.lookml`
- `lookml_dashboards/dashboards/q28.dashboard.lookml`
- `lookml_dashboards/dashboards/q29.dashboard.lookml`
- `lookml_dashboards/dashboards/q30.dashboard.lookml`
