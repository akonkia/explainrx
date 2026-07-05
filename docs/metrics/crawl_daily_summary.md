# ExplainRx crawl daily summary

Latest rollup day: **2026-07-05**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-05T00:01:48+02:00` to `2026-07-05T22:19:36+02:00` local (`213` snapshots)
- Entities in KB: `1,192,241` (`+144,368` today)
- Relationships in KB: `18,255,534` (positive gain `+3,568,918`, net `+3,544,440`)
- Completed entities (all pages crawled): `1,389` (`+572` today)
- Queue: `done 1,401 (+645)`, `processing 7 (+1)`, `pending 850,779 (+193,753)`, `errors 214 (+51)`
- Relationship drop/reset events recorded today: `2`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-05 | 18,255,534 | +3,568,918 | 1,192,241 | 1,389 | 850,779 | 2 drop/reset day, errors +51 |
| 2026-07-04 | 14,697,037 | +2,735,677 | 1,047,113 | 817 | 655,906 | 2 drop/reset day, errors +73 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 459 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 147 | 28,119 | 19 drop/reset day |

Generated from `crawl_daily_progress.csv`.
