# ExplainRx crawl daily summary

Latest rollup day: **2026-07-20**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-20T19:04:20+02:00` to `2026-07-20T19:04:20+02:00` local (`1` snapshots)
- Entities in KB: `787,674` (`+0` today)
- Relationships in KB: `16,438,999` (positive gain `+0`, net `+0`)
- Entity page crawls exhausted: `170` (`+0` today)
- Queue backlog: `processing 10 (+0)`, `pending 208,664 (+0)`, `errors 0 (+0)`
- Entity dedup backlog: `213,965` remaining of `214,255` candidate pairs (`0.14%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-20 | 16,438,999 | +0 | 787,674 | 170 | 208,664 |  |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 170 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 165 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 159 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 159 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 159 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 159 | 145,993 |  |

Generated from `crawl_daily_progress.csv`.
