# ExplainRx crawl daily summary

Latest rollup day: **2026-07-22**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-22T08:57:09+02:00` to `2026-07-22T18:05:41+02:00` local (`85` snapshots)
- Entities in KB: `804,739` (`+8,510` today)
- Relationships in KB: `16,562,101` (positive gain `+151,712`, net `+83,821`)
- Entity page crawls exhausted: `185` (`+3` today)
- Queue backlog: `processing 6 (-4)`, `pending 264,044 (+23,541)`, `errors 0 (+0)`
- Entity dedup backlog: `213,488` remaining of `217,768` candidate pairs (`4,280` covered; `1.965%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `10`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-22 | 16,562,101 | +151,712 | 804,739 | 185 | 264,044 | 10 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 157 | 150,020 |  |

Generated from `crawl_daily_progress.csv`.
