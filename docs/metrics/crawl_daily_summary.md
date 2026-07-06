# ExplainRx crawl daily summary

Latest rollup day: **2026-07-06**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-06T00:25:20+02:00` to `2026-07-06T19:07:30+02:00` local (`179` snapshots)
- Entities in KB: `1,292,996` (`+98,128` today)
- Relationships in KB: `19,561,004` (positive gain `+1,728,465`, net `+1,252,614`)
- Completed entities (all pages crawled): `1,878` (`+478` today)
- Queue: `done 1,906 (+494)`, `processing 7 (-3)`, `pending 903,170 (+36,296)`, `errors 232 (+18)`
- Relationship drop/reset events recorded today: `15`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-06 | 19,561,004 | +1,728,465 | 1,292,996 | 1,878 | 903,170 | 15 drop/reset day, errors +18 |
| 2026-07-05 | 18,312,350 | +3,625,734 | 1,194,501 | 1,400 | 866,320 | 2 drop/reset day, errors +51 |
| 2026-07-04 | 14,697,037 | +2,735,677 | 1,047,113 | 817 | 655,906 | 2 drop/reset day, errors +73 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 459 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |

Generated from `crawl_daily_progress.csv`.
