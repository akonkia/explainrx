# ExplainRx crawl daily summary

Latest rollup day: **2026-07-09**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-09T00:03:18+02:00` to `2026-07-09T18:27:24+02:00` local (`291` snapshots)
- Entities in KB: `763,286` (`-5,262` today)
- Relationships in KB: `15,786,051` (positive gain `+86,950`, net `-144,112`)
- Completed entities (all pages crawled): `19` (`+0` today)
- Queue: `done 19 (+0)`, `processing 2 (-4)`, `pending 117,532 (-15,153)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `1`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-09 | 15,786,051 | +86,950 | 763,286 | 19 | 117,532 | 1 drop/reset day |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 19 | 132,685 |  |
| 2026-07-07 | 15,858,951 | +69,822 | 766,113 | 19 | 125,817 |  |
| 2026-07-06 | 15,789,129 | +60,178 | 763,482 | 19 | 117,995 |  |
| 2026-07-05 | 15,719,565 | +77,945 | 760,170 | 18 | 110,827 |  |
| 2026-07-04 | 15,639,121 | +56,043 | 756,650 | 18 | 100,618 |  |
| 2026-07-03 | 15,562,897 | +81,945 | 754,547 | 18 | 89,021 |  |

Generated from `crawl_daily_progress.csv`.
