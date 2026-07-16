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

Latest rollup day: **2026-07-16**

Source: **shared Pi crawl via agnes@192.168.1.21**


Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

### Latest day

- Snapshot window: `2026-07-16T08:14:35+02:00` to `2026-07-16T22:07:47+02:00` local (`202` snapshots)
- Entities in KB: `775,665` (`+1,035` today)
- Relationships in KB: `16,204,700` (positive gain `+54,169`, net `+54,169`)
- Completed entities (all pages crawled): `152` (`+0` today)
- Queue: `done 21 (+0)`, `processing 10 (+4)`, `pending 151,928 (+1,829)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `0`

### Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-16 | 16,204,700 | +54,169 | 775,665 | 152 | 151,928 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 152 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 152 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 152 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 152 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 151 | 132,685 |  |
| 2026-07-07 | 15,858,951 | +69,822 | 766,113 | 151 | 125,817 |  |

Generated from `crawl_daily_progress.csv`.
<!-- CRAWL_PROGRESS:END -->
