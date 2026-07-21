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

Latest rollup day: **2026-07-21**

Source: **shared Pi crawl via agnes@192.168.1.22**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-21T09:58:15+02:00` to `2026-07-21T16:37:44+02:00` local (`85` snapshots)
- Entities in KB: `793,574` (`+4,028` today)
- Relationships in KB: `16,471,295` (positive gain `+118,138`, net `+53,910`)
- Entity page crawls exhausted: `182` (`+10` today)
- Queue backlog: `processing 5 (-5)`, `pending 229,151 (+12,376)`, `errors 0 (+0)`
- Entity dedup backlog: `214,515` remaining of `214,805` candidate pairs (`0.14%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `3`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-21 | 16,471,295 | +118,138 | 793,574 | 182 | 229,151 | 3 drop/reset day |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 168 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 163 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 157 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 157 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 157 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 157 | 145,993 |  |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
