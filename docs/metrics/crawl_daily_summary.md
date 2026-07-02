# ExplainRx crawl daily summary

Latest rollup day: **2026-07-02**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-02T09:00:55+02:00` to `2026-07-02T10:43:53+02:00` local (`20` snapshots)
- Entities in KB: `750,721` (`+239` today)
- Relationships in KB: `15,391,636` (positive gain `+10,350`, net `+10,350`)
- Queue: `done 14 (+0)`, `processing 7 (+5)`, `pending 68,527 (+1,913)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Done | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-02 | 15,391,636 | +10,350 | 750,721 | 14 | 68,527 |  |
| 2026-07-01 | 15,359,199 | +58,491 | 749,858 | 14 | 60,849 |  |
| 2026-06-30 | 15,750,104 | +43,414 | 749,314 | 13 | 40,208 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 13 | 31,531 | 1 drop/reset day |
| 2026-06-25 | 15,143,451 | +373,394 | — | 13 | 28,119 | 19 drop/reset day |
| 2026-06-24 | 15,256,735 | +343,778 | — | 6 | 13,503 | 10 drop/reset day |

Generated from `scripts/crawl_daily_progress.csv`.
