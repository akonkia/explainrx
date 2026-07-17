# ExplainRx crawl daily summary

Latest rollup day: **2026-07-17**

Source: **shared Pi crawl via agnes@192.168.1.21**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-17T09:47:10+02:00` to `2026-07-17T14:24:46+02:00` local (`45` snapshots)
- Entities in KB: `776,199` (`+382` today)
- Relationships in KB: `16,229,865` (positive gain `+18,117`, net `+18,115`)
- Completed entities (all pages crawled): `152` (`+0` today)
- Queue: `done 21 (+0)`, `processing 0 (-16)`, `pending 153,508 (+1,029)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `1`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-17 | 16,229,865 | +18,117 | 776,199 | 152 | 153,508 | 1 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 152 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 152 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 152 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 152 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 152 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 151 | 132,685 |  |

Generated from `crawl_daily_progress.csv`.
