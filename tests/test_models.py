from travel_planner.models import (
    AppState,
    Trip,
    PackingItem,
    BudgetItem,
    ActivityItem,
    create_sample_state,
    new_trip,
)
from datetime import date
from uuid import uuid4


def test_appstate_serialize_roundtrip(sample_state: AppState):
    d = sample_state.to_dict()
    restored = AppState.from_dict(d)
    assert restored.to_dict() == d
    assert restored.active_trip_id == sample_state.active_trip_id


def test_trip_budget_calculation():
    t = new_trip(
        "Test Trip",
        "Somewhere",
        date(2025, 1, 10),
        date(2025, 1, 12),
    )
    t.budget_items.append(
        BudgetItem(
            id=str(uuid4()),
            category="Transport",
            description="Train",
            cost=100.0,
            paid=True,
        )
    )
    t.budget_items.append(
        BudgetItem(
            id=str(uuid4()),
            category="Hotel",
            description="2 nights",
            cost=200.0,
            paid=False,
        )
    )

    assert t.total_budget() == 300.0
    assert t.total_paid() == 100.0
    assert t.total_remaining() == 200.0


def test_packingitem_fields():
    p = PackingItem(
        id="abc",
        item_name="T-shirt",
        category="Clothes",
        quantity=3,
        place="Checked",
        packed=False,
    )
    d = p.to_dict()
    assert d["quantity"] == 3
    assert d["place"] == "Checked"
    assert d["packed"] is False

    restored = PackingItem.from_dict(d)
    assert restored.quantity == 3
    assert restored.place == "Checked"
    assert restored.packed is False


def test_activityitem_roundtrip():
    act = ActivityItem(
        id="act1",
        day=date(2025, 11, 14),
        time="12:00",
        title="Museum",
        location="City Museum",
        notes="Tickets in email",
    )
    d = act.to_dict()
    restored = ActivityItem.from_dict(d)
    assert restored.id == "act1"
    assert restored.day == date(2025, 11, 14)
    assert restored.time == "12:00"
    assert restored.title == "Museum"
    assert restored.location == "City Museum"
    assert restored.notes == "Tickets in email"
