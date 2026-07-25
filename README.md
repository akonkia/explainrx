# ExplainRx Crawl Growth

Minimal public snapshot of ExplainRx KB expansion progress.

[Open the full combined plot](docs/metrics/crawl_daily_growth.svg)

![ExplainRx crawl growth](docs/metrics/crawl_daily_growth.svg)

Panel files:
[Edges in KB](docs/metrics/crawl_panel_edges.png) ·
[Daily positive relationship gain](docs/metrics/crawl_panel_gain.png) ·
[End-of-day pending queue](docs/metrics/crawl_panel_pending.png) ·
[Entities completed](docs/metrics/crawl_panel_done.png) ·
[Entities in KB total](docs/metrics/crawl_panel_entities.png)

## Crawl progress


Latest daily summary: [docs/metrics/crawl_daily_summary.md](docs/metrics/crawl_daily_summary.md)

## Crawl Progress

![ExplainRx crawl progress](docs/metrics/crawl_daily_growth.svg)

<!-- CRAWL_PROGRESS:START -->
Latest daily summary: [docs/metrics/crawl_daily_summary.md](docs/metrics/crawl_daily_summary.md)

Latest rollup day: **2026-07-25**

Source: **shared Pi crawl via agnes@192.168.1.22**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-25T10:42:41+02:00` to `2026-07-25T12:32:29+02:00` local (`13` snapshots)
- Entities in KB: `822,093` (`+1,347` today)
- Relationships in KB: `16,658,703` (positive gain `+48,245`, net `+48,188`)
- Entity page crawls exhausted: `215` (`+0` today)
- Queue backlog: `processing 10 (+0)`, `pending 305,231 (+0)`, `errors 0 (+0)`
- Entity dedup backlog: `217,985` remaining of `222,265` candidate pairs (`4,280` covered; `1.926%` of current pool)
- Entity dedup review state: `open review 4,280` (needs_review `1,384`, proposed_llm `2,896`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `1`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-25 | 16,658,703 | +48,245 | 822,093 | 215 | 305,231 | 1 drop/reset day |
| 2026-07-24 | 16,663,830 | +208,534 | 820,746 | 215 | 305,232 | 24 drop/reset day |
| 2026-07-23 | 16,704,875 | +190,963 | 811,911 | 199 | 285,786 | 8 drop/reset day |
| 2026-07-22 | 16,608,021 | +234,579 | 807,190 | 185 | 272,862 | 14 drop/reset day |
| 2026-07-21 | 16,478,273 | +189,225 | 796,229 | 182 | 240,513 | 7 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
