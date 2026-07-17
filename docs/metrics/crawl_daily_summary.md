# ExplainRx crawl daily summary

Latest rollup day: **2026-07-17**

Source: **shared Pi crawl via agnes@192.168.1.21**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-17T09:47:10+02:00` to `2026-07-17T19:30:19+02:00` local (`90` snapshots)
- Entities in KB: `776,215` (`+398` today)
- Relationships in KB: `16,225,738` (positive gain `+20,360`, net `+13,988`)
- Completed entities (all pages crawled): `151` (`+0` today)
- Active queue: `processing 0 (-16)`, `pending 154,085 (+1,606)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `4`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-17 | 16,225,738 | +20,360 | 776,215 | 151 | 154,085 | 4 drop/reset day |
| 2026-07-16 | 16,209,048 | +58,517 | 775,770 | 151 | 152,351 |  |
| 2026-07-15 | 16,150,082 | +50,931 | 774,619 | 151 | 150,020 |  |
| 2026-07-14 | 16,098,404 | +8,986 | 773,474 | 151 | 145,993 |  |
| 2026-07-10 | 16,089,418 | +55,652 | 773,225 | 151 | 145,262 |  |
| 2026-07-09 | 16,033,766 | +103,603 | 771,900 | 151 | 140,976 |  |
| 2026-07-08 | 15,927,736 | +68,785 | 768,515 | 150 | 132,685 |  |

Generated from `crawl_daily_progress.csv`.
