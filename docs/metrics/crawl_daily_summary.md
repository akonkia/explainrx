# ExplainRx crawl daily summary

Latest rollup day: **2026-07-23**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-23T09:18:10+02:00` to `2026-07-23T18:20:52+02:00` local (`101` snapshots)
- Entities in KB: `810,124` (`+2,934` today)
- Relationships in KB: `16,636,124` (positive gain `+111,857`, net `+27,975`)
- Entity page crawls exhausted: `199` (`+14` today)
- Queue backlog: `processing 2 (-4)`, `pending 281,687 (+8,814)`, `errors 0 (+0)`
- Entity dedup backlog: `215,673` remaining of `219,953` candidate pairs (`4,280` covered; `1.946%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `6`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-23 | 16,636,124 | +111,857 | 810,124 | 199 | 281,687 | 6 drop/reset day |
| 2026-07-22 | 16,608,021 | +234,579 | 807,190 | 185 | 272,862 | 14 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |

Generated from `crawl_daily_progress.csv`.
