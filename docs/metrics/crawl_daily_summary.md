# ExplainRx crawl daily summary

Latest rollup day: **2026-07-05**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-05T00:01:48+02:00` to `2026-07-05T21:40:17+02:00` local (`205` snapshots)
- Entities in KB: `1,188,148` (`+140,275` today)
- Relationships in KB: `18,169,525` (positive gain `+3,482,909`, net `+3,458,431`)
- Completed entities (all pages crawled): `1,374` (`+557` today)
- Queue: `done 1,385 (+629)`, `processing 10 (+4)`, `pending 857,221 (+200,195)`, `errors 212 (+49)`
- Relationship drop/reset events recorded today: `2`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-05 | 18,169,525 | +3,482,909 | 1,188,148 | 1,374 | 857,221 | 2 drop/reset day, errors +49 |
| 2026-07-04 | 14,697,037 | +2,735,677 | 1,047,113 | 817 | 655,906 | 2 drop/reset day, errors +73 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 459 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 147 | 28,119 | 19 drop/reset day |

Generated from `crawl_daily_progress.csv`.
