# Measure dependencies (Power BI → LookML)

**Source:** `movie_rental_analysis.pbix`  
**Total measures:** 5  ·  **Mapped:** 3  ·  **TODO:** 2  ·  **With dependencies:** 1

When a measure depends on another, Looker requires `type: number` and `${measure}` references ([measure types](https://cloud.google.com/looker/docs/reference/param-measure-types)). Ratios use `1.0 * ${num} / NULLIF(${den}, 0)` ([division best practice](https://cloud.google.com/looker/docs/best-practices/how-to-troubleshoot-fields-with-division-displaying-0)). `filters:` is only valid on aggregate measures — never on `type: number` ([filters](https://cloud.google.com/looker/docs/reference/param-field-filters)).

## Dependent measures (implement bases first)

| LookML measure | Depends on (Power BI) | Strategy | Status |
|---|---|---|---|
| `inventory_turnover_rate` | Total Films Rented, Average Inventory Value | measure_ratio | mapped |

## All measures

| View | Power BI | LookML | Strategy | Depends on | Mapped |
|---|---|---|---|---|---|
| `actor` | FilmPopularity | `film_popularity` | complex_todo | — | TODO |
| `inventory` | Total Films Rented | `total_films_rented` | complex_todo | — | TODO |
| `inventory` | Average Inventory Value | `average_inventory_value` | direct_average | — | yes |
| `inventory` | Inventory Turnover Rate | `inventory_turnover_rate` | measure_ratio | Total Films Rented, Average Inventory Value | yes |
| `payment` | Revenue | `revenue` | direct_sum | — | yes |

## References

- https://cloud.google.com/looker/docs/reference/param-measure-types
- https://cloud.google.com/looker/docs/reference/param-field-filters
- https://cloud.google.com/looker/docs/best-practices/how-to-troubleshoot-fields-with-division-displaying-0
- https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-modeling-guidelines/SKILL.md
- https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md
