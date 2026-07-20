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

Latest rollup day: **2026-07-20**

Source: **shared Pi crawl via agnes@192.168.1.22**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-20T20:27:19+02:00` to `2026-07-20T20:27:19+02:00` local (`1` snapshots)
- Entities in KB: `787,719` (`+0` today)
- Relationships in KB: `16,382,352` (positive gain `+0`, net `+0`)
- Entity page crawls exhausted: `173` (`+4` today)
- Queue backlog: `processing 9 (+0)`, `pending 210,619 (+0)`, `errors 0 (+0)`
- Entity dedup backlog: `214,555` remaining of `214,845` candidate pairs (`0.13%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `0`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-20 | 16,382,352 | +0 | 787,719 | 173 | 210,619 |  |
| 2026-07-19 | 16,453,466 | +46,156 | 787,462 | 169 | 208,578 | 1 drop/reset day |
| 2026-07-18 | 16,403,798 | +253,232 | 785,719 | 164 | 200,514 | 4 drop/reset day |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 158 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 158 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 158 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 158 | 145,993 |  |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
