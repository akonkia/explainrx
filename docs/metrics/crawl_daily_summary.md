# ExplainRx crawl daily summary

Latest rollup day: **2026-07-05**

Source: **shared Pi crawl via agnes@192.168.1.21**

![ExplainRx crawl growth](crawl_daily_growth.svg)

Display baseline: **2026-06-24 onward**. Earlier days are excluded because they used older ingestion rules.

## Latest day

- Snapshot window: `2026-07-05T09:16:02+02:00` to `2026-07-05T21:08:13+02:00` local (`104` snapshots)
- Entities in KB: `760,170` (`+3,462` today)
- Relationships in KB: `15,719,565` (positive gain `+77,945`, net `+77,945`)
- Completed entities (all pages crawled): `1,400` (`+583` today)
- Queue: `done 18 (+0)`, `processing 2 (-4)`, `pending 110,827 (+9,770)`, `errors 0 (+0)`
- Relationship drop/reset events recorded today: `0`

## Recent days

| Date | Edges in KB | Positive gain | Entities in KB | Completed | Pending | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2026-07-05 | 15,719,565 | +77,945 | 760,170 | 1,400 | 110,827 |  |
| 2026-07-04 | 15,639,121 | +56,043 | 756,650 | 817 | 100,618 |  |
| 2026-07-03 | 15,562,897 | +81,945 | 754,547 | 459 | 89,021 |  |
| 2026-07-02 | 15,468,872 | +87,586 | 752,911 | 285 | 79,922 |  |
| 2026-07-01 | 15,359,199 | +58,491 | 749,858 | 147 | 60,849 |  |
| 2026-06-30 | 15,750,104 | +43,414 | 749,314 | 147 | 40,208 | 2 drop/reset day |
| 2026-06-29 | 15,703,847 | +42,802 | — | 147 | 31,531 | 1 drop/reset day |

Generated from `crawl_daily_progress.csv`.
