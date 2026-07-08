# ExplainRx crawl daily summary

Latest rollup day: **2026-07-08**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-08T11:25:02+02:00` to `2026-07-08T16:05:39+02:00` local (`2` snapshots)
- Entities in KB: `763,286` (`+0` today)
- Relationships in KB: `15,786,051` (positive gain `+0`, net `+0`)
- Completed entities (all pages crawled): `151` (`+0` today)
- Queue: `done 19 (+0)`, `processing 2 (+0)`, `pending 117,532 (+0)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-08 | 15,786,051 | +0 | 763,286 | 151 | 117,532 |  |
| 2026-07-07 | 15,786,051 | +0 | 763,286 | 151 | 117,532 |  |
| 2026-07-06 | 20,091,695 | +2,260,159 | 1,313,667 | 151 | 919,963 | 17 drop/reset day, errors +20 |
| 2026-07-05 | 18,312,350 | +3,625,734 | 1,194,501 | 151 | 866,320 | 2 drop/reset day, errors +51 |
| 2026-07-04 | 14,697,037 | +2,735,677 | 1,047,113 | 150 | 655,906 | 2 drop/reset day, errors +73 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 150 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 149 | 293,953 | 75 drop/reset day, errors +63 |

Generated from `crawl_daily_progress.csv`.
