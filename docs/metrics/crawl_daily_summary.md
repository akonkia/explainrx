# ExplainRx crawl daily summary

Latest rollup day: **2026-07-21**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-21T09:58:15+02:00` to `2026-07-21T21:36:10+02:00` local (`141` snapshots)
- Entities in KB: `796,076` (`+6,530` today)
- Relationships in KB: `16,476,838` (positive gain `+183,201`, net `+59,453`)
- Entity page crawls exhausted: `182` (`+10` today)
- Queue backlog: `processing 6 (-4)`, `pending 237,313 (+20,538)`, `errors 0 (+0)`
- Entity dedup backlog: `214,937` remaining of `215,227` candidate pairs (`0.13%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `5`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-21 | 16,476,838 | +183,201 | 796,076 | 182 | 237,313 | 5 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 157 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 157 | 145,993 |  |

Generated from `crawl_daily_progress.csv`.
