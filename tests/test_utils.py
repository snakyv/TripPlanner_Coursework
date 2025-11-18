from datetime import date
from uuid import uuid4

from travel_planner.models import Trip, ActivityItem, new_trip
from travel_planner.utils import (
    human_date,
    date_range_str,
    money,
    get_upcoming_activity,
    activity_sort_key,
)


def test_human_date():
    d = date(2025, 11, 14)
    assert human_date(d) == "14 Nov 2025"


def test_date_range_str():
    s = date(2025, 11, 14)
    e = date(2025, 11, 17)
    assert date_range_str(s, e) == "14 Nov 2025 – 17 Nov 2025"


def test_money():
    assert money(12.5) == "12.50 €"
    assert money(100, "$") == "100.00 $"


def _make_trip_with_activities():
    t = new_trip(
        "Mock Trip",
        "Test City",
        date(2025, 1, 10),
        date(2025, 1, 12),
    )

    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 1, 10),
            time="09:00",
            title="Breakfast",
            location="Hotel Lobby",
            notes="Buffet",
        )
    )

    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 1, 11),
            time="12:00",
            title="City Tour",
            location="Main Square",
            notes="Bring water",
        )
    )

    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 1, 11),
            time="08:30",
            title="Museum Visit",
            location="History Museum",
            notes="Ticket QR in email",
        )
    )

    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 1, 12),
            time="16:00",
            title="Dinner",
            location="Old Town",
            notes="Seafood",
        )
    )

    return t


def test_activity_sort_key_orders_by_day_then_time():
    t = _make_trip_with_activities()
    acts_sorted = sorted(t.activities, key=activity_sort_key)

    titles_in_order = [a.title for a in acts_sorted]
    assert titles_in_order == [
        "Breakfast",
        "Museum Visit",
        "City Tour",
        "Dinner",
    ]


def test_get_upcoming_activity_prefers_today_or_future():
    t = _make_trip_with_activities()

    upcoming = get_upcoming_activity(t, today=date(2025, 1, 11))
    assert upcoming is not None
    assert upcoming.title in ("Museum Visit", "City Tour")
    assert upcoming.day == date(2025, 1, 11)

    future_pick = get_upcoming_activity(t, today=date(2030, 1, 1))
    assert future_pick is not None
    assert future_pick.title == "Breakfast"
    assert future_pick.day == date(2025, 1, 10)
