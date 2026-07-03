# ExplainRx crawl daily summary

Latest rollup day: **2026-07-03**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-03T15:45:49+02:00` to `2026-07-03T20:59:49+02:00` local (`62` snapshots)
- Entities in KB: `888,339` (`+52,998` today)
- Relationships in KB: `11,344,422` (positive gain `+822,177`, net `+673,017`)
- Completed entities (all pages crawled): `374` (`+89` today)
- Queue: `done 278 (+104)`, `processing 6 (+0)`, `pending 397,542 (+100,194)`, `errors 74 (+11)`
- Relationship drop/reset events recorded today: `11`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-03 | 11,344,422 | +822,177 | 888,339 | 374 | 397,542 | 11 drop/reset day, errors +11 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 147 | 28,119 | 19 drop/reset day |
| 2026-06-24 | 15,256,735 | +343,778 | — | 145 | 13,503 | 10 drop/reset day |

Generated from `crawl_daily_progress.csv`.
