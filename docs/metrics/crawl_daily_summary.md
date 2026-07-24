# ExplainRx crawl daily summary

Latest rollup day: **2026-07-24**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-24T09:25:17+02:00` to `2026-07-24T17:49:16+02:00` local (`49` snapshots)
- Entities in KB: `818,713` (`+6,736` today)
- Relationships in KB: `16,635,538` (positive gain `+137,251`, net `-72,857`)
- Entity page crawls exhausted: `215` (`+16` today)
- Queue backlog: `processing 22 (+16)`, `pending 300,007 (+14,211)`, `errors 0 (+0)`
- Entity dedup backlog: `217,201` remaining of `221,481` candidate pairs (`4,280` covered; `1.932%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `15`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-24 | 16,635,538 | +137,251 | 818,713 | 215 | 300,007 | 15 drop/reset day |
| 2026-07-23 | 16,704,875 | +190,963 | 811,911 | 199 | 285,786 | 8 drop/reset day |
| 2026-07-22 | 16,608,021 | +234,579 | 807,190 | 185 | 272,862 | 14 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |

Generated from `crawl_daily_progress.csv`.
