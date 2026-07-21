# ExplainRx crawl daily summary

Latest rollup day: **2026-07-21**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-21T09:58:15+02:00` to `2026-07-21T23:50:07+02:00` local (`157` snapshots)
- Entities in KB: `796,229` (`+6,683` today)
- Relationships in KB: `16,478,280` (positive gain `+189,232`, net `+60,895`)
- Entity page crawls exhausted: `182` (`+10` today)
- Queue backlog: `processing 0 (-10)`, `pending 240,508 (+23,733)`, `errors 0 (+0)`
- Entity dedup backlog: `213,580` remaining of `214,958` candidate pairs (`1,378` covered; `0.641%` of current pool)
- Entity dedup review state: `open review 1,378` (needs_review `410`, proposed_llm `968`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `7`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-21 | 16,478,280 | +189,232 | 796,229 | 182 | 240,508 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 157 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 157 | 145,993 |  |

Generated from `crawl_daily_progress.csv`.
