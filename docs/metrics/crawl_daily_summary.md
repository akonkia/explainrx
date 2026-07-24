# ExplainRx crawl daily summary

Latest rollup day: **2026-07-24**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-24T09:25:17+02:00` to `2026-07-24T10:06:45+02:00` local (`4` snapshots)
- Entities in KB: `812,048` (`+71` today)
- Relationships in KB: `16,705,113` (positive gain `+8,508`, net `-3,282`)
- Entity page crawls exhausted: `212` (`+13` today)
- Queue backlog: `processing 4 (-2)`, `pending 287,700 (+1,904)`, `errors 0 (+0)`
- Entity dedup backlog: `215,860` remaining of `220,140` candidate pairs (`4,280` covered; `1.944%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `2`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-24 | 16,705,113 | +8,508 | 812,048 | 212 | 287,700 | 2 drop/reset day |
| 2026-07-23 | 16,704,875 | +190,963 | 811,911 | 199 | 285,786 | 8 drop/reset day |
| 2026-07-22 | 16,608,021 | +234,579 | 807,190 | 185 | 272,862 | 14 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |

Generated from `crawl_daily_progress.csv`.
