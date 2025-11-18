from __future__ import annotations
from datetime import date
from typing import List, Dict

from .models import ActivityItem, Trip

MONTHS_SHORT = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


def human_date(d: date) -> str:
    return f"{d.day:02d} {MONTHS_SHORT[d.month-1]} {d.year}"


def date_range_str(start: date, end: date) -> str:
    return f"{human_date(start)} – {human_date(end)}"


def money(value: float, currency: str = "€") -> str:
    return f"{value:.2f} {currency}"


def _parse_hhmm(t: str) -> tuple[int, int]:
    try:
        parts = t.strip().split(":")
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        return h, m
    except Exception:
        return (99, 99)


def activity_sort_key(act: ActivityItem) -> tuple[int, int, int]:
    h, m = _parse_hhmm(act.time)
    return (act.day.toordinal(), h, m)


def get_upcoming_activity(trip: Trip, today: date) -> ActivityItem | None:
    acts_sorted = sorted(trip.activities, key=activity_sort_key)
    if not acts_sorted:
        return None

    for a in acts_sorted:
        if a.day >= today:
            return a
    return acts_sorted[0]
