# ExplainRx crawl daily summary

Latest rollup day: **2026-07-04**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-04T00:05:05+02:00` to `2026-07-04T12:13:12+02:00` local (`27` snapshots)
- Entities in KB: `943,935` (`+22,080` today)
- Relationships in KB: `12,462,817` (positive gain `+500,671`, net `+500,671`)
- Completed entities (all pages crawled): `531` (`+72` today)
- Queue: `done 443 (+78)`, `processing 6 (+5)`, `pending 494,139 (+38,356)`, `errors 105 (+15)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-04 | 12,462,817 | +500,671 | 943,935 | 531 | 494,139 | errors +15 |
| 2026-07-03 | 11,947,931 | +1,444,814 | 921,243 | 459 | 454,772 | 13 drop/reset day, errors +27 |
| 2026-07-02 | 10,671,405 | +426,624 | 835,341 | 285 | 293,953 | 75 drop/reset day, errors +63 |
| 2026-06-30 | 15,739,422 | +32,732 | 749,106 | 147 | 38,380 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 147 | 28,119 | 19 drop/reset day |
| 2026-06-24 | 15,256,735 | +343,778 | — | 145 | 13,503 | 10 drop/reset day |

Generated from `crawl_daily_progress.csv`.
