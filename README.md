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

Latest rollup day: **2026-07-17**

Source: **shared Pi crawl via agnes@192.168.1.21**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-17T09:47:10+02:00` to `2026-07-17T21:19:16+02:00` local (`104` snapshots)
- Entities in KB: `776,239` (`+422` today)
- Relationships in KB: `16,226,247` (positive gain `+21,204`, net `+14,497`)
- Entity page crawls exhausted: `160` (`+0` today)
- Queue backlog: `processing 0 (-16)`, `pending 154,125 (+1,646)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `5`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-17 | 16,226,247 | +21,204 | 776,239 | 160 | 154,125 | 5 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 160 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 160 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 160 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 160 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 160 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 158 | 132,685 |  |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
