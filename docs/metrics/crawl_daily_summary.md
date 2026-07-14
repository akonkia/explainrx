# ExplainRx crawl daily summary

Latest rollup day: **2026-07-14**

Source: **local DB explainrx_dev**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-14T18:30:12+02:00` to `2026-07-14T18:57:11+02:00` local (`7` snapshots)
- Entities in KB: `763,286` (`-9,939` today)
- Relationships in KB: `15,786,051` (positive gain `+628`, net `-303,367`)
- Completed entities (all pages crawled): `19` (`+0` today)
- Queue: `done 19 (-2)`, `processing 2 (-8)`, `pending 117,532 (-27,736)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `1`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-14 | 15,786,051 | +628 | 763,286 | 19 | 117,532 | 1 drop/reset day |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 21 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 20 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 19 | 132,685 |  |
| 2026-07-07 | 15,858,951 | +69,822 | 766,113 | 19 | 125,817 |  |
| 2026-07-06 | 15,789,129 | +60,178 | 763,482 | 19 | 117,995 |  |
| 2026-07-05 | 15,719,565 | +77,945 | 760,170 | 18 | 110,827 |  |

Generated from `crawl_daily_progress.csv`.
