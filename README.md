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

Latest rollup day: **2026-07-18**

Source: **shared Pi crawl via agnes@192.168.1.21**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-18T00:13:49+02:00` to `2026-07-18T15:45:21+02:00` local (`61` snapshots)
- Entities in KB: `779,091` (`+2,852` today)
- Relationships in KB: `16,287,106` (positive gain `+64,852`, net `+64,852`)
- Entity page crawls exhausted: `163` (`+4` today)
- Queue backlog: `processing 0 (+0)`, `pending 171,114 (+17,005)`, `errors 0 (+0)`
- Entity dedup backlog: `210,836` remaining of `211,126` candidate pairs (`0.14%` covered)
- Entity dedup review state: `open review 290` (needs_review `87`, proposed_llm `203`); `human-reviewed 0` (accepted `0`, rejected `0`)
- Relationship drop/reset events recorded today: `0`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-18 | 16,287,106 | +64,852 | 779,091 | 163 | 171,114 |  |
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 159 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 159 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 159 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 159 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 159 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 159 | 140,976 |  |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
