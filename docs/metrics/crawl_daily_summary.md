# ExplainRx crawl daily summary

Latest rollup day: **2026-07-23**

Source: **shared Pi crawl via agnes@192.168.1.22**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-23T09:18:58+02:00` to `2026-07-23T09:18:58+02:00` local (`1` snapshots)
- Intraday coverage: only `1` snapshot was recorded for this day, so snapshot-based same-day deltas are unavailable.
- Entities in KB: `807,190` (intraday change unavailable: only `1` snapshot; vs prior day `+0`)
- Relationships in KB: `16,608,149` (intraday gain unavailable: only `1` snapshot; vs prior day `+128`)
- Entity page crawls exhausted: `185` (`+0` today)
- Queue backlog: `processing 6 (vs prior day +1)`, `pending 272,873 (vs prior day +11)`, `errors 0 (vs prior day +0)`
- Entity dedup backlog: `214,455` remaining of `218,735` candidate pairs (`4,280` covered; `1.957%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-23 | 16,608,149 | — | 807,190 | 185 | 272,873 | 1 snapshot only |
| 2026-07-22 | 16,608,021 | +234,579 | 807,190 | 185 | 272,862 | 14 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |

Generated from `crawl_daily_progress.csv`.
