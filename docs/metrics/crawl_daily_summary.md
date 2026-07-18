# ExplainRx crawl daily summary

Latest rollup day: **2026-07-18**

Source: **shared Pi crawl via agnes@192.168.1.21**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-18T00:13:49+02:00` to `2026-07-18T10:05:58+02:00` local (`60` snapshots)
- Entities in KB: `776,245` (`+6` today)
- Relationships in KB: `16,224,316` (positive gain `+2,062`, net `+2,062`)
- Entity page crawls exhausted: `163` (`+4` today)
- Queue backlog: `processing 0 (+0)`, `pending 154,859 (+750)`, `errors 0 (+0)`
- Entity dedup backlog: `211,517` remaining of `211,807` candidate pairs (`0.14%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-18 | 16,224,316 | +2,062 | 776,245 | 163 | 154,859 |  |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 159 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 159 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 159 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 159 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 159 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 159 | 140,976 |  |

Generated from `crawl_daily_progress.csv`.
