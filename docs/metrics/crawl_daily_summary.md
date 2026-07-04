# ExplainRx crawl daily summary

Latest rollup day: **2026-07-04**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-04T00:05:05+02:00` to `2026-07-04T10:34:38+02:00` local (`8` snapshots)
- Entities in KB: `927,665` (`+5,810` today)
- Relationships in KB: `12,101,972` (positive gain `+139,826`, net `+139,826`)
- Completed entities (all pages crawled): `471` (`+12` today)
- Queue: `done 382 (+17)`, `processing 2 (+1)`, `pending 466,251 (+10,468)`, `errors 92 (+2)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-04 | 12,101,972 | +139,826 | 927,665 | 471 | 466,251 | errors +2 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 459 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 147 | 28,119 | 19 drop/reset day |
| 2026-06-24 | 15,256,735 | +343,778 | — | 145 | 13,503 | 10 drop/reset day |

Generated from `crawl_daily_progress.csv`.
