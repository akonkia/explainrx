# ExplainRx crawl daily summary

Latest rollup day: **2026-07-15**

Source: **shared Pi crawl via agnes@192.168.1.21**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-15T08:58:02+02:00` to `2026-07-15T16:35:06+02:00` local (`117` snapshots)
- Entities in KB: `774,159` (`+683` today)
- Relationships in KB: `16,125,911` (positive gain `+26,760`, net `+26,760`)
- Completed entities (all pages crawled): `152` (`+0` today)
- Queue: `done 21 (+0)`, `processing 6 (-4)`, `pending 147,936 (+1,939)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-15 | 16,125,911 | +26,760 | 774,159 | 152 | 147,936 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 152 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 152 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 152 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 151 | 132,685 |  |
| 2026-07-07 | 15,858,951 | +69,822 | 766,113 | 151 | 125,817 |  |
| 2026-07-06 | 15,789,129 | +60,178 | 763,482 | 151 | 117,995 |  |

Generated from `crawl_daily_progress.csv`.
