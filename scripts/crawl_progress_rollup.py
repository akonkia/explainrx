#!/usr/bin/env python3
"""
crawl_progress_rollup.py — aggregate minute-level crawl snapshots into
plot-friendly daily progress rows.

Reads `crawl_health_history.log` and writes one CSV row per local calendar day.
The output is meant for simple plotting in R, Python, Numbers, or Excel.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from io_targets import copy_target_to_local, write_bytes_atomic

DEFAULT_DIR = Path(__file__).resolve().parent
DEFAULT_HISTORY = os.environ.get(
    "EXPLAINRX_HISTORY_FILE",
    str(DEFAULT_DIR / "crawl_health_history.log"),
)
DEFAULT_OUT = os.environ.get(
    "EXPLAINRX_DAILY_PROGRESS_FILE",
    str(DEFAULT_DIR / "crawl_daily_progress.csv"),
)
DEFAULT_SVG = os.environ.get(
    "EXPLAINRX_DAILY_GROWTH_SVG",
    str(DEFAULT_DIR.parent / "docs" / "metrics" / "crawl_daily_growth.svg"),
)
DEFAULT_SUMMARY_MD = os.environ.get(
    "EXPLAINRX_DAILY_SUMMARY_MD",
    str(DEFAULT_DIR.parent / "docs" / "metrics" / "crawl_daily_summary.md"),
)
DEFAULT_PLOT_START_DATE = os.environ.get(
    "EXPLAINRX_DAILY_PLOT_START_DATE",
    "2026-06-24",
)
DEFAULT_SOURCE_LABEL = os.environ.get(
    "EXPLAINRX_CRAWL_SOURCE_LABEL",
    "crawl history",
)
DEFAULT_DB = os.environ.get(
    "EXPLAINRX_DB",
    "",
).strip()
DEFAULT_COMPLETION_TIMELINE_FILE = os.environ.get(
    "EXPLAINRX_COMPLETION_TIMELINE_FILE",
    "",
).strip()


def _as_int(value: str):
    try:
        return int(value)
    except ValueError:
        return value


def parse_history(path: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    if not path.exists():
        return rows

    for raw in path.read_text().splitlines():
        parts = raw.split("\t")
        if len(parts) < 2:
            continue
        try:
            ts = int(parts[0])
        except ValueError:
            continue

        row: Dict[str, object] = {"ts": ts, "verdict": parts[1]}
        for token in parts[2:]:
            if "=" not in token:
                continue
            key, value = token.split("=", 1)
            row[key] = _as_int(value)
        rows.append(row)

    rows.sort(key=lambda r: int(r["ts"]))
    return rows


def load_completion_timeline_from_psql(db: str) -> Dict[str, Dict[str, int]]:
    db_name = str(db or "").strip()
    if not db_name:
        return {}

    psql_bin = shutil.which("psql")
    if not psql_bin:
        for candidate in ("/opt/homebrew/bin/psql", "/usr/local/bin/psql", "/usr/bin/psql"):
            if Path(candidate).exists():
                psql_bin = candidate
                break
    if not psql_bin:
        return {}

    query = """
        SELECT finished_at::date AS date, count(*) AS completed_that_day
        FROM kb_crawl_progress
        WHERE is_complete
          AND finished_at IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """
    try:
        proc = subprocess.run(
            [psql_bin, "-d", db_name, "-X", "--csv", "-v", "ON_ERROR_STOP=1", "-c", query],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except OSError:
        return {}
    if proc.returncode != 0:
        return {}

    out: Dict[str, Dict[str, int]] = {}
    cumulative = 0
    reader = csv.DictReader(proc.stdout.splitlines())
    for row in reader:
        day = str(row.get("date", "")).strip()
        if not day:
            continue
        try:
            completed_that_day = int(row.get("completed_that_day") or 0)
        except ValueError:
            continue
        cumulative += completed_that_day
        out[day] = {
            "completed_entities_that_day": completed_that_day,
            "completed_entities_current": cumulative,
        }
    return out


def load_completion_timeline_from_csv(path: Path) -> Dict[str, Dict[str, int]]:
    if not path.exists():
        return {}

    out: Dict[str, Dict[str, int]] = {}
    cumulative = 0
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            day = str(row.get("date", "")).strip()
            if not day:
                continue
            raw = row.get("completed_entities_that_day", row.get("completed_that_day", 0))
            try:
                completed_that_day = int(raw or 0)
            except ValueError:
                continue
            cumulative += completed_that_day
            out[day] = {
                "completed_entities_that_day": completed_that_day,
                "completed_entities_current": cumulative,
            }
    return out


def _first_metric(rows: List[Dict[str, object]], key: str):
    for row in rows:
        value = row.get(key)
        if isinstance(value, int):
            return value
    return ""


def _last_metric(rows: List[Dict[str, object]], key: str):
    for row in reversed(rows):
        value = row.get(key)
        if isinstance(value, int):
            return value
    return ""


def _relationship_stats(day_rows: List[Dict[str, object]]):
    rels = [r.get("rel") for r in day_rows if isinstance(r.get("rel"), int)]
    if not rels:
        return {
            "start_relationships": "",
            "end_relationships": "",
            "net_relationship_change": "",
            "positive_relationship_gain": "",
            "relationship_drop_events": "",
            "largest_relationship_drop": "",
            "min_relationships": "",
            "max_relationships": "",
        }

    positive_gain = 0
    drop_events = 0
    largest_drop = 0
    prev = rels[0]
    for rel in rels[1:]:
        delta = rel - prev
        if delta >= 0:
            positive_gain += delta
        else:
            drop_events += 1
            largest_drop = min(largest_drop, delta)
        prev = rel

    return {
        "start_relationships": rels[0],
        "end_relationships": rels[-1],
        "net_relationship_change": rels[-1] - rels[0],
        "positive_relationship_gain": positive_gain,
        "relationship_drop_events": drop_events,
        "largest_relationship_drop": largest_drop,
        "min_relationships": min(rels),
        "max_relationships": max(rels),
    }


def build_daily_rows(
    records: Iterable[Dict[str, object]],
    completion_timeline: Optional[Dict[str, Dict[str, int]]] = None,
) -> List[Dict[str, object]]:
    groups: Dict[str, List[Dict[str, object]]] = {}
    for row in records:
        local_dt = dt.datetime.fromtimestamp(int(row["ts"])).astimezone()
        groups.setdefault(local_dt.date().isoformat(), []).append(row)

    out: List[Dict[str, object]] = []
    completion_map = completion_timeline or {}
    completion_days = sorted(completion_map)
    completion_idx = 0
    last_completion_cumulative = 0
    for day in sorted(groups):
        day_rows = groups[day]
        first = day_rows[0]
        last = day_rows[-1]
        first_dt = dt.datetime.fromtimestamp(int(first["ts"])).astimezone()
        last_dt = dt.datetime.fromtimestamp(int(last["ts"])).astimezone()
        start_ent = _first_metric(day_rows, "ent")
        end_ent = _last_metric(day_rows, "ent")
        start_done = _first_metric(day_rows, "done")
        end_done = _last_metric(day_rows, "done")
        start_proc = _first_metric(day_rows, "proc")
        end_proc = _last_metric(day_rows, "proc")
        start_pending = _first_metric(day_rows, "pending")
        end_pending = _last_metric(day_rows, "pending")
        start_err = _first_metric(day_rows, "err")
        end_err = _last_metric(day_rows, "err")
        start_complete = _first_metric(day_rows, "complete")
        end_complete = _last_metric(day_rows, "complete")

        completed_today: object = ""
        completed_cumulative: object = ""
        if completion_map:
            while completion_idx < len(completion_days) and completion_days[completion_idx] <= day:
                day_key = completion_days[completion_idx]
                last_completion_cumulative = int(
                    completion_map[day_key]["completed_entities_current"]
                )
                completion_idx += 1
            completed_cumulative = last_completion_cumulative
            completed_today = int(
                completion_map.get(day, {}).get("completed_entities_that_day", 0)
            )
        elif isinstance(end_complete, int):
            completed_cumulative = end_complete
            if isinstance(start_complete, int):
                completed_today = end_complete - start_complete
            else:
                completed_today = end_complete

        row = {
            "date": day,
            "first_snapshot_at": first_dt.isoformat(),
            "last_snapshot_at": last_dt.isoformat(),
            "snapshot_count": len(day_rows),
            "start_entities": start_ent,
            "end_entities": end_ent,
            "entities_added": (end_ent - start_ent
                               if isinstance(start_ent, int) and isinstance(end_ent, int)
                               else ""),
            "start_done": start_done,
            "end_done": end_done,
            "done_change": (end_done - start_done
                            if isinstance(start_done, int) and isinstance(end_done, int)
                            else ""),
            "start_processing": start_proc,
            "end_processing": end_proc,
            "processing_change": (end_proc - start_proc
                                  if isinstance(start_proc, int) and isinstance(end_proc, int)
                                  else ""),
            "start_pending": start_pending,
            "end_pending": end_pending,
            "pending_change": (end_pending - start_pending
                               if isinstance(start_pending, int) and isinstance(end_pending, int)
                               else ""),
            "start_errors": start_err,
            "end_errors": end_err,
            "error_change": (end_err - start_err
                             if isinstance(start_err, int) and isinstance(end_err, int)
                             else ""),
            "completed_entities_that_day": completed_today,
            "completed_entities_current": completed_cumulative,
        }
        row.update(_relationship_stats(day_rows))
        out.append(row)

    return out


def _compact_int(value: int) -> str:
    abs_val = abs(value)
    if abs_val >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if abs_val >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs_val >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{value}"


def _nice_step(span: float, target_ticks: int = 5) -> float:
    if span <= 0:
        return 1.0
    rough = span / max(target_ticks, 1)
    magnitude = 10 ** math.floor(math.log10(rough))
    for mult in (1, 2, 5, 10):
        step = magnitude * mult
        if step >= rough:
            return step
    return magnitude * 10


def _ticks(min_val: float, max_val: float, target_ticks: int = 5) -> List[float]:
    if min_val == max_val:
        return [min_val]
    step = _nice_step(max_val - min_val, target_ticks)
    start = math.floor(min_val / step) * step
    end = math.ceil(max_val / step) * step
    ticks = []
    cur = start
    # small epsilon avoids floating-point drift on exact end values
    while cur <= end + step * 0.001:
        ticks.append(cur)
        cur += step
    return ticks


def _scale(value: float, min_val: float, max_val: float, start_px: float, end_px: float) -> float:
    if max_val == min_val:
        return (start_px + end_px) / 2
    frac = (value - min_val) / (max_val - min_val)
    return start_px + frac * (end_px - start_px)


def _fmt_int(value: object) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    return "—"


def _fmt_delta(value: object) -> str:
    if isinstance(value, int):
        return f"{value:+,}"
    return "—"


def _filter_display_rows(rows: List[Dict[str, object]], start_date: Optional[str]) -> List[Dict[str, object]]:
    start_raw = str(start_date or "").strip()
    if not start_raw:
        return rows
    try:
        start = dt.date.fromisoformat(start_raw)
    except ValueError:
        return rows
    out: List[Dict[str, object]] = []
    for row in rows:
        try:
            row_day = dt.date.fromisoformat(str(row["date"]))
        except ValueError:
            continue
        if row_day >= start:
            out.append(row)
    return out


def write_summary_md(
    rows: List[Dict[str, object]],
    out_path: Path,
    recent_days: int = 7,
    start_date: Optional[str] = DEFAULT_PLOT_START_DATE,
    source_label: str = DEFAULT_SOURCE_LABEL,
    svg_ref: str = "crawl_daily_growth.svg",
    csv_ref: str = "crawl_daily_progress.csv",
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    display_rows = _filter_display_rows(rows, start_date)
    if not display_rows:
        out_path.write_text(
            "# ExplainRx crawl daily summary\n\n"
            f"Source: **{source_label}**\n\n"
            f"No daily crawl history is available on or after `{start_date}`.\n"
        )
        return

    latest = display_rows[-1]
    latest_date = str(latest["date"])
    first_at = str(latest.get("first_snapshot_at", "—"))
    last_at = str(latest.get("last_snapshot_at", "—"))
    snapshot_count = latest.get("snapshot_count")
    drop_events = int(latest.get("relationship_drop_events", 0) or 0)
    has_completed = any(
        isinstance(row.get("completed_entities_current"), int)
        for row in display_rows
    )
    completed_col = "Completed" if has_completed else "Queue done"

    recent = display_rows[-recent_days:]
    table_lines = [
        f"| Date | Edges in KB | Positive gain | Entities in KB | {completed_col} | Pending | Notes |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in reversed(recent):
        notes = []
        drops = int(row.get("relationship_drop_events", 0) or 0)
        if drops:
            notes.append(f"{drops} drop/reset day")
        if isinstance(row.get("error_change"), int) and int(row["error_change"]) > 0:
            notes.append(f"errors {int(row['error_change']):+,}")
        table_lines.append(
            "| {date} | {edges} | {gain} | {entities} | {done} | {pending} | {notes} |".format(
                date=row["date"],
                edges=_fmt_int(row.get("end_relationships")),
                gain=_fmt_delta(row.get("positive_relationship_gain")),
                entities=_fmt_int(row.get("end_entities")),
                done=_fmt_int(
                    row.get("completed_entities_current")
                    if has_completed
                    else row.get("end_done")
                ),
                pending=_fmt_int(row.get("end_pending")),
                notes=", ".join(notes) if notes else "",
            )
        )

    latest_completed_line = (
        f"- Completed entities (all pages crawled): `{_fmt_int(latest.get('completed_entities_current'))}` "
        f"(`{_fmt_delta(latest.get('completed_entities_that_day'))}` today)"
        if has_completed
        else f"- Queue rows currently `done`: `{_fmt_int(latest.get('end_done'))}` (`{_fmt_delta(latest.get('done_change'))}` today)"
    )

    md = "\n".join(
        [
            "# ExplainRx crawl daily summary",
            "",
            f"Latest rollup day: **{latest_date}**",
            "",
            f"Source: **{source_label}**",
            "",
            f"![ExplainRx crawl growth]({svg_ref})",
            "",
            f"Display baseline: **{start_date} onward**. Earlier days are excluded because they used older ingestion rules.",
            "",
            "## Latest day",
            "",
            f"- Snapshot window: `{first_at}` to `{last_at}` local (`{snapshot_count}` snapshots)",
            f"- Entities in KB: `{_fmt_int(latest.get('end_entities'))}` (`{_fmt_delta(latest.get('entities_added'))}` today)",
            f"- Relationships in KB: `{_fmt_int(latest.get('end_relationships'))}` (positive gain `{_fmt_delta(latest.get('positive_relationship_gain'))}`, net `{_fmt_delta(latest.get('net_relationship_change'))}`)",
            latest_completed_line,
            f"- Queue: `done {_fmt_int(latest.get('end_done'))} ({_fmt_delta(latest.get('done_change'))})`, `processing {_fmt_int(latest.get('end_processing'))} ({_fmt_delta(latest.get('processing_change'))})`, `pending {_fmt_int(latest.get('end_pending'))} ({_fmt_delta(latest.get('pending_change'))})`, `errors {_fmt_int(latest.get('end_errors'))} ({_fmt_delta(latest.get('error_change'))})`",
            f"- Relationship drop/reset events recorded today: `{drop_events}`",
            "",
            "## Recent days",
            "",
            *table_lines,
            "",
            f"Generated from `{csv_ref}`.",
            "",
        ]
    )
    out_path.write_text(md)


def write_growth_svg(
    rows: List[Dict[str, object]],
    out_path: Path,
    start_date: Optional[str] = DEFAULT_PLOT_START_DATE,
    source_label: str = DEFAULT_SOURCE_LABEL,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    width = 1200
    height = 1756
    left = 88
    right = 42
    top_title = 54
    summary_top = 118
    summary_bottom = 174
    line_top = 208
    line_bottom = 422
    bar_top = 514
    bar_bottom = 742
    pending_top = 834
    pending_bottom = 1048
    ent_top = 1140
    ent_bottom = 1354
    tot_top = 1446
    tot_bottom = 1660
    plot_width = width - left - right
    bg = "#f7f7f2"
    ink = "#202126"
    muted = "#70757a"
    grid = "#d8ddd2"
    count_color = "#1f4e79"
    gain_color = "#2a9d8f"
    warn_color = "#b3472c"
    pending_color = "#6f5499"
    ent_color = "#a6611a"
    tot_color = "#2f6b3c"

    display_rows = _filter_display_rows(rows, start_date)

    if not display_rows:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <text x="60" y="90" font-family="Helvetica, Arial, sans-serif" font-size="28" fill="{ink}">ExplainRx crawl growth</text>
  <text x="60" y="126" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="{muted}">Source: {html.escape(source_label)}</text>
  <text x="60" y="152" font-family="Helvetica, Arial, sans-serif" font-size="18" fill="{muted}">No daily crawl history is available on or after {html.escape(str(start_date))}.</text>
</svg>
"""
        out_path.write_text(svg)
        return

    labels = [str(r["date"])[5:] for r in display_rows]
    counts = [int(r["end_relationships"]) for r in display_rows if isinstance(r.get("end_relationships"), int)]
    gains = [int(r["positive_relationship_gain"]) for r in display_rows if isinstance(r.get("positive_relationship_gain"), int)]
    line_values = [int(r.get("end_relationships", 0) or 0) for r in display_rows]
    gain_values = [int(r.get("positive_relationship_gain", 0) or 0) for r in display_rows]
    latest = display_rows[-1]
    latest_day = html.escape(str(latest["date"]))
    latest_rel = html.escape(f"{int(latest.get('end_relationships', 0) or 0):,}")
    latest_gain = html.escape(f"{int(latest.get('positive_relationship_gain', 0) or 0):,}")
    latest_pending = html.escape(f"{int(latest.get('end_pending', 0) or 0):,}")
    latest_ent = (
        f"{int(latest['end_entities']):,}"
        if isinstance(latest.get("end_entities"), int) else "—"
    )

    line_min = min(line_values)
    line_max = max(line_values)
    if line_min == line_max:
        line_min = max(0, line_min - 1)
        line_max = line_max + 1

    gain_max = max(gain_values) if gain_values else 0
    gain_min = 0
    if gain_max == 0:
        gain_max = 1

    pending_values = [int(r.get("end_pending", 0) or 0) for r in display_rows]
    pending_min = min(pending_values) if pending_values else 0
    pending_max = max(pending_values) if pending_values else 1
    if pending_min == pending_max:
        pending_min = max(0, pending_min - 1)
        pending_max = pending_max + 1

    has_completed = any(
        isinstance(r.get("completed_entities_current"), int)
        for r in display_rows
    )
    ent_label = (
        "Entities fully crawled (all pages)"
        if has_completed
        else "Queue items currently done"
    )
    ent_legend = (
        "Fully crawled entities"
        if has_completed
        else "Current done count"
    )
    ent_fallback = (
        "No fully crawled-entity counts available yet."
        if has_completed
        else "No done-queue counts logged yet."
    )

    ent_indexed = [
        (
            i,
            int(
                r["completed_entities_current"]
                if has_completed
                else r["end_done"]
            ),
        )
        for i, r in enumerate(display_rows)
        if isinstance(
            r.get("completed_entities_current")
            if has_completed
            else r.get("end_done"),
            int,
        )
    ]
    ent_vals = [v for _, v in ent_indexed]
    ent_min = min(ent_vals) if ent_vals else 0
    ent_max = max(ent_vals) if ent_vals else 1
    if ent_min == ent_max:
        ent_min = max(0, ent_min - 1)
        ent_max = ent_max + 1

    # Total entities in the KB (ent=). Only logged on recent days, so keep just
    # the days that have it; the panel fills in as more days are recorded.
    tot_indexed = [(i, int(r["end_entities"]))
                   for i, r in enumerate(display_rows)
                   if isinstance(r.get("end_entities"), int)]
    tot_vals = [v for _, v in tot_indexed]
    tot_min = min(tot_vals) if tot_vals else 0
    tot_max = max(tot_vals) if tot_vals else 1
    if tot_min == tot_max:
        tot_min = max(0, tot_min - 1)
        tot_max = tot_max + 1

    xs = []
    if len(display_rows) == 1:
        xs = [left + plot_width / 2]
    else:
        for idx in range(len(display_rows)):
            xs.append(left + (plot_width * idx / (len(display_rows) - 1)))

    line_points = []
    for x, value in zip(xs, line_values):
        y = _scale(value, line_min, line_max, line_bottom, line_top)
        line_points.append((x, y))

    bar_width = min(34, max(10, int(plot_width / max(len(display_rows) * 1.8, 1))))
    line_tick_vals = _ticks(line_min, line_max, 5)
    gain_tick_vals = _ticks(gain_min, gain_max, 4)
    pending_tick_vals = _ticks(pending_min, pending_max, 5)

    pending_points = []
    for x, value in zip(xs, pending_values):
        y = _scale(value, pending_min, pending_max, pending_bottom, pending_top)
        pending_points.append((x, y))

    ent_tick_vals = _ticks(ent_min, ent_max, 5) if ent_vals else []
    ent_points = [(xs[i], _scale(v, ent_min, ent_max, ent_bottom, ent_top))
                  for i, v in ent_indexed]

    tot_tick_vals = _ticks(tot_min, tot_max, 5) if tot_vals else []
    tot_points = [(xs[i], _scale(v, tot_min, tot_max, tot_bottom, tot_top))
                  for i, v in tot_indexed]
    latest_completed = (
        f"{int(latest['completed_entities_current']):,}"
        if isinstance(latest.get("completed_entities_current"), int) else None
    )
    latest_status_label = "Fully crawled" if latest_completed is not None else "Pending queue"
    latest_status_value = html.escape(latest_completed) if latest_completed is not None else latest_pending
    summary_cells = [
        ("Latest day", latest_day),
        ("Entities in KB", html.escape(latest_ent)),
        ("Edges in KB", latest_rel),
        ("Positive gain", latest_gain),
        (latest_status_label, latest_status_value),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{bg}"/>',
        f'<text x="60" y="{top_title}" font-family="Helvetica, Arial, sans-serif" font-size="28" font-weight="700" fill="{ink}">ExplainRx crawl growth</text>',
        f'<text x="60" y="{top_title + 24}" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="{muted}">Source: {html.escape(source_label)}</text>',
        f'<text x="60" y="{top_title + 46}" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="{muted}">Daily relationship count and daily positive relationship gain, starting {html.escape(str(start_date))} because earlier days used older ingestion rules</text>',
        f'<rect x="{left}" y="{summary_top}" width="{plot_width}" height="{summary_bottom - summary_top}" fill="#ffffff" rx="10"/>',
        f'<rect x="{left}" y="{line_top}" width="{plot_width}" height="{line_bottom - line_top}" fill="#ffffff" rx="10"/>',
        f'<rect x="{left}" y="{bar_top}" width="{plot_width}" height="{bar_bottom - bar_top}" fill="#ffffff" rx="10"/>',
        f'<rect x="{left}" y="{pending_top}" width="{plot_width}" height="{pending_bottom - pending_top}" fill="#ffffff" rx="10"/>',
        f'<rect x="{left}" y="{ent_top}" width="{plot_width}" height="{ent_bottom - ent_top}" fill="#ffffff" rx="10"/>',
        f'<rect x="{left}" y="{tot_top}" width="{plot_width}" height="{tot_bottom - tot_top}" fill="#ffffff" rx="10"/>',
        f'<text x="{left}" y="{line_top - 18}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">Edges in KB (relationships, end-of-day total)</text>',
        f'<text x="{left}" y="{bar_top - 18}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">Daily positive relationship gain</text>',
        f'<text x="{left}" y="{pending_top - 18}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">End-of-day pending queue</text>',
        f'<text x="{left}" y="{ent_top - 18}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">{html.escape(ent_label)}</text>',
        f'<text x="{left}" y="{tot_top - 18}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">Entities in KB (total)</text>',
    ]

    cell_width = plot_width / len(summary_cells)
    for idx, (label, value) in enumerate(summary_cells):
        cell_x = left + idx * cell_width
        if idx > 0:
            parts.append(
                f'<line x1="{cell_x:.1f}" y1="{summary_top + 10}" x2="{cell_x:.1f}" y2="{summary_bottom - 10}" stroke="{grid}" stroke-width="1"/>'
            )
        parts.append(
            f'<text x="{cell_x + 18:.1f}" y="{summary_top + 22}" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="700" fill="{muted}">{html.escape(label)}</text>'
        )
        parts.append(
            f'<text x="{cell_x + 18:.1f}" y="{summary_top + 45}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="{ink}">{value}</text>'
        )

    for tick in line_tick_vals:
        y = _scale(tick, line_min, line_max, line_bottom, line_top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="{grid}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(_compact_int(int(tick)))}</text>')

    for tick in gain_tick_vals:
        y = _scale(tick, gain_min, gain_max, bar_bottom, bar_top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="{grid}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(_compact_int(int(tick)))}</text>')

    for tick in pending_tick_vals:
        y = _scale(tick, pending_min, pending_max, pending_bottom, pending_top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="{grid}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(_compact_int(int(tick)))}</text>')

    for tick in ent_tick_vals:
        y = _scale(tick, ent_min, ent_max, ent_bottom, ent_top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="{grid}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(_compact_int(int(tick)))}</text>')

    for tick in tot_tick_vals:
        y = _scale(tick, tot_min, tot_max, tot_bottom, tot_top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="{grid}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(_compact_int(int(tick)))}</text>')

    # Line plot
    line_path = " ".join(
        [f"M {line_points[0][0]:.1f} {line_points[0][1]:.1f}"] +
        [f"L {x:.1f} {y:.1f}" for x, y in line_points[1:]]
    )
    parts.append(f'<path d="{line_path}" fill="none" stroke="{count_color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    for idx, ((x, y), value) in enumerate(zip(line_points, line_values)):
        radius = 5 if idx < len(line_points) - 1 else 7
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{count_color}"/>')
        if idx == len(line_points) - 1:
            parts.append(f'<text x="{x + 10:.1f}" y="{y - 10:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="{count_color}">{html.escape(f"{value:,}")}</text>')

    # Bar plot
    for x, value, row in zip(xs, gain_values, display_rows):
        y = _scale(value, gain_min, gain_max, bar_bottom, bar_top)
        height_px = max(0, bar_bottom - y)
        bar_x = x - bar_width / 2
        parts.append(f'<rect x="{bar_x:.1f}" y="{y:.1f}" width="{bar_width}" height="{height_px:.1f}" rx="4" fill="{gain_color}"/>')
        drops = int(row.get("relationship_drop_events", 0) or 0)
        if drops > 0:
            parts.append(f'<circle cx="{x:.1f}" cy="{max(bar_top + 12, y - 10):.1f}" r="5" fill="{warn_color}"/>')

    # Pending-queue line plot
    pending_path = " ".join(
        [f"M {pending_points[0][0]:.1f} {pending_points[0][1]:.1f}"] +
        [f"L {x:.1f} {y:.1f}" for x, y in pending_points[1:]]
    )
    parts.append(f'<path d="{pending_path}" fill="none" stroke="{pending_color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    for idx, ((x, y), value) in enumerate(zip(pending_points, pending_values)):
        radius = 5 if idx < len(pending_points) - 1 else 7
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{pending_color}"/>')
        if idx == len(pending_points) - 1:
            parts.append(f'<text x="{x + 10:.1f}" y="{y - 10:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="{pending_color}">{html.escape(f"{value:,}")}</text>')

    # Entities line plot (only days that logged ent=)
    if ent_points:
        if len(ent_points) > 1:
            ent_path = " ".join(
                [f"M {ent_points[0][0]:.1f} {ent_points[0][1]:.1f}"] +
                [f"L {x:.1f} {y:.1f}" for x, y in ent_points[1:]]
            )
            parts.append(f'<path d="{ent_path}" fill="none" stroke="{ent_color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        for idx, ((x, y), value) in enumerate(zip(ent_points, ent_vals)):
            radius = 5 if idx < len(ent_points) - 1 else 7
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{ent_color}"/>')
            if idx == len(ent_points) - 1:
                parts.append(f'<text x="{x + 10:.1f}" y="{y - 10:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="{ent_color}">{html.escape(f"{value:,}")}</text>')
    else:
        parts.append(f'<text x="{left + plot_width / 2:.1f}" y="{(ent_top + ent_bottom) / 2:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="{muted}">{html.escape(ent_fallback)}</text>')

    # Total entities-in-KB line plot (only days that logged ent=)
    if tot_points:
        if len(tot_points) > 1:
            tot_path = " ".join(
                [f"M {tot_points[0][0]:.1f} {tot_points[0][1]:.1f}"] +
                [f"L {x:.1f} {y:.1f}" for x, y in tot_points[1:]]
            )
            parts.append(f'<path d="{tot_path}" fill="none" stroke="{tot_color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        for idx, ((x, y), value) in enumerate(zip(tot_points, tot_vals)):
            radius = 5 if idx < len(tot_points) - 1 else 7
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{tot_color}"/>')
            if idx == len(tot_points) - 1:
                parts.append(f'<text x="{x + 10:.1f}" y="{y - 10:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="{tot_color}">{html.escape(f"{value:,}")}</text>')
    else:
        parts.append(f'<text x="{left + plot_width / 2:.1f}" y="{(tot_top + tot_bottom) / 2:.1f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="{muted}">No entity counts logged yet — fills in as the monitor records ent=.</text>')

    # Shared x labels
    for x, label in zip(xs, labels):
        parts.append(f'<text x="{x:.1f}" y="{tot_bottom + 24}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{muted}">{html.escape(label)}</text>')

    # Legend — two rows so nothing clips the canvas edge.
    legend_y1 = height - 52
    legend_y2 = height - 24
    parts += [
        f'<line x1="60" y1="{legend_y1}" x2="84" y2="{legend_y1}" stroke="{count_color}" stroke-width="4"/>',
        f'<text x="94" y="{legend_y1 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">Edges in KB</text>',
        f'<line x1="280" y1="{legend_y1}" x2="304" y2="{legend_y1}" stroke="{pending_color}" stroke-width="4"/>',
        f'<text x="314" y="{legend_y1 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">Pending queue</text>',
        f'<line x1="520" y1="{legend_y1}" x2="544" y2="{legend_y1}" stroke="{ent_color}" stroke-width="4"/>',
        f'<text x="554" y="{legend_y1 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">{html.escape(ent_legend)}</text>',
        f'<line x1="800" y1="{legend_y1}" x2="824" y2="{legend_y1}" stroke="{tot_color}" stroke-width="4"/>',
        f'<text x="834" y="{legend_y1 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">Entities in KB (total)</text>',
        f'<rect x="60" y="{legend_y2 - 11}" width="20" height="20" rx="4" fill="{gain_color}"/>',
        f'<text x="90" y="{legend_y2 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">Daily positive relationship gain</text>',
        f'<circle cx="400" cy="{legend_y2 - 1}" r="5" fill="{warn_color}"/>',
        f'<text x="414" y="{legend_y2 + 5}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="{ink}">Day includes edge-count drops/resets</text>',
    ]

    parts.append("</svg>")
    out_path.write_text("\n".join(parts) + "\n")


def write_daily_rollup(
    history_path: Path,
    out_path: Path,
    svg_path: Optional[Path] = DEFAULT_SVG,
    summary_md_path: Optional[Path] = DEFAULT_SUMMARY_MD,
    plot_start_date: Optional[str] = DEFAULT_PLOT_START_DATE,
    source_label: str = DEFAULT_SOURCE_LABEL,
    completion_db: str = DEFAULT_DB,
    completion_timeline_file: Optional[str] = DEFAULT_COMPLETION_TIMELINE_FILE,
) -> None:
    completion_timeline = {}
    completion_file_raw = str(completion_timeline_file or "").strip()
    if completion_file_raw:
        completion_timeline = load_completion_timeline_from_csv(Path(completion_file_raw))
    if not completion_timeline:
        completion_timeline = load_completion_timeline_from_psql(completion_db)
    rows = build_daily_rows(parse_history(history_path), completion_timeline)
    for row in rows:
        row["source_label"] = source_label
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")

    fieldnames = [
        "date",
        "first_snapshot_at",
        "last_snapshot_at",
        "snapshot_count",
        "start_entities",
        "end_entities",
        "entities_added",
        "start_relationships",
        "end_relationships",
        "net_relationship_change",
        "positive_relationship_gain",
        "relationship_drop_events",
        "largest_relationship_drop",
        "min_relationships",
        "max_relationships",
        "start_done",
        "end_done",
        "done_change",
        "start_processing",
        "end_processing",
        "processing_change",
        "start_pending",
        "end_pending",
        "pending_change",
        "start_errors",
        "end_errors",
        "error_change",
        "completed_entities_that_day",
        "completed_entities_current",
        "source_label",
    ]

    with tmp_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    tmp_path.replace(out_path)
    if svg_path is not None:
        write_growth_svg(rows, svg_path, plot_start_date, source_label)
    if summary_md_path is not None:
        svg_ref = Path(svg_path).name if svg_path is not None else "crawl_daily_growth.svg"
        csv_ref = Path(out_path).name
        write_summary_md(
            rows,
            summary_md_path,
            start_date=plot_start_date,
            source_label=source_label,
            svg_ref=svg_ref,
            csv_ref=csv_ref,
        )


def write_daily_rollup_target(
    history_target: str,
    out_target: str,
    svg_target: Optional[str] = None,
    summary_md_target: Optional[str] = None,
    plot_start_date: Optional[str] = DEFAULT_PLOT_START_DATE,
    source_label: str = DEFAULT_SOURCE_LABEL,
    completion_db: str = DEFAULT_DB,
    completion_timeline_file: Optional[str] = DEFAULT_COMPLETION_TIMELINE_FILE,
) -> None:
    history_raw = str(history_target)
    out_raw = str(out_target)
    svg_raw = None if svg_target is None else str(svg_target)
    summary_raw = None if summary_md_target is None else str(summary_md_target)

    if (
        not history_raw.startswith("ssh://")
        and not out_raw.startswith("ssh://")
        and (svg_raw is None or not svg_raw.startswith("ssh://"))
        and (summary_raw is None or not summary_raw.startswith("ssh://"))
    ):
        svg_path = None if svg_raw is None else Path(svg_raw)
        summary_path = None if summary_raw is None else Path(summary_raw)
        write_daily_rollup(
            Path(history_raw),
            Path(out_raw),
            svg_path,
            summary_path,
            plot_start_date,
            source_label,
            completion_db,
            completion_timeline_file,
        )
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        local_history = tmpdir_path / "crawl_health_history.log"
        local_out = tmpdir_path / "crawl_daily_progress.csv"
        local_svg = None if svg_raw is None else (tmpdir_path / "crawl_daily_growth.svg")
        local_summary = None if summary_raw is None else (tmpdir_path / "crawl_daily_summary.md")
        copy_target_to_local(history_raw, local_history)
        write_daily_rollup(
            local_history,
            local_out,
            local_svg,
            local_summary,
            plot_start_date,
            source_label,
            completion_db,
            completion_timeline_file,
        )
        write_bytes_atomic(out_raw, local_out.read_bytes())
        if local_svg is not None and svg_raw is not None:
            write_bytes_atomic(svg_raw, local_svg.read_bytes())
        if local_summary is not None and summary_raw is not None:
            write_bytes_atomic(summary_raw, local_summary.read_bytes())


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Roll up crawl_health_history.log into one CSV row per day."
    )
    ap.add_argument("--history", default=str(DEFAULT_HISTORY),
                    help=f"Input history log (default: {DEFAULT_HISTORY})")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help=f"Output CSV path (default: {DEFAULT_OUT})")
    ap.add_argument("--svg", default=str(DEFAULT_SVG),
                    help=f"Output SVG plot path (default: {DEFAULT_SVG})")
    ap.add_argument("--summary-md", default=str(DEFAULT_SUMMARY_MD),
                    help=f"Output markdown summary path (default: {DEFAULT_SUMMARY_MD})")
    ap.add_argument("--plot-start-date", default=str(DEFAULT_PLOT_START_DATE),
                    help=f"Only show dates on/after this ISO date in the plot/summary (default: {DEFAULT_PLOT_START_DATE})")
    ap.add_argument("--source-label", default=str(DEFAULT_SOURCE_LABEL),
                    help=f"Human-readable source label stamped into the CSV/plot/summary (default: {DEFAULT_SOURCE_LABEL})")
    ap.add_argument("--db", default=str(DEFAULT_DB),
                    help="Database name used to derive cumulative all-pages-crawled entity counts via psql")
    ap.add_argument("--completion-timeline-file", default=str(DEFAULT_COMPLETION_TIMELINE_FILE),
                    help="Optional CSV file with date,completed_that_day rows for durable crawl completions")
    args = ap.parse_args()
    svg_target = None if str(args.svg).strip().lower() in {"", "none", "off"} else str(args.svg)
    summary_target = None if str(args.summary_md).strip().lower() in {"", "none", "off"} else str(args.summary_md)
    plot_start_date = None if str(args.plot_start_date).strip().lower() in {"", "none", "off"} else str(args.plot_start_date)
    write_daily_rollup_target(
        str(args.history),
        str(args.out),
        svg_target,
        summary_target,
        plot_start_date,
        str(args.source_label),
        str(args.db),
        str(args.completion_timeline_file),
    )


if __name__ == "__main__":
    main()
