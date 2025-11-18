from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4
from typing import List, Optional, Dict, Any


@dataclass
class ActivityItem:
    id: str
    day: date
    time: str
    title: str
    location: str
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "day": self.day.isoformat(),
            "time": self.time,
            "title": self.title,
            "location": self.location,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActivityItem":
        return cls(
            id=data["id"],
            day=date.fromisoformat(data["day"]),
            time=data.get("time", ""),
            title=data.get("title", ""),
            location=data.get("location", ""),
            notes=data.get("notes", ""),
        )


@dataclass
class BudgetItem:
    id: str
    category: str
    description: str
    cost: float
    paid: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "description": self.description,
            "cost": self.cost,
            "paid": self.paid,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BudgetItem":
        return cls(
            id=data["id"],
            category=data.get("category", ""),
            description=data.get("description", ""),
            cost=float(data.get("cost", 0.0)),
            paid=bool(data.get("paid", False)),
        )


@dataclass
class PackingItem:
    id: str
    item_name: str
    category: str
    quantity: int = 1
    place: str = "Carry-on"
    packed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "item_name": self.item_name,
            "category": self.category,
            "quantity": self.quantity,
            "place": self.place,
            "packed": self.packed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PackingItem":
        return cls(
            id=data["id"],
            item_name=data.get("item_name", ""),
            category=data.get("category", ""),
            quantity=int(data.get("quantity", 1)),
            place=data.get("place", "Carry-on"),
            packed=bool(data.get("packed", False)),
        )


@dataclass
class Trip:
    id: str
    title: str
    destination: str
    start_date: date
    end_date: date
    accommodation: str = ""
    notes: str = ""
    activities: List[ActivityItem] = field(default_factory=list)
    budget_items: List[BudgetItem] = field(default_factory=list)
    packing_items: List[PackingItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "destination": self.destination,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "accommodation": self.accommodation,
            "notes": self.notes,
            "activities": [a.to_dict() for a in self.activities],
            "budget_items": [b.to_dict() for b in self.budget_items],
            "packing_items": [p.to_dict() for p in self.packing_items],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trip":
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            destination=data.get("destination", ""),
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            accommodation=data.get("accommodation", ""),
            notes=data.get("notes", ""),
            activities=[ActivityItem.from_dict(x) for x in data.get("activities", [])],
            budget_items=[BudgetItem.from_dict(x) for x in data.get("budget_items", [])],
            packing_items=[PackingItem.from_dict(x) for x in data.get("packing_items", [])],
        )

    def total_budget(self) -> float:
        return sum(item.cost for item in self.budget_items)

    def total_paid(self) -> float:
        return sum(item.cost for item in self.budget_items if item.paid)

    def total_remaining(self) -> float:
        return self.total_budget() - self.total_paid()


@dataclass
class AppState:
    trips: List[Trip] = field(default_factory=list)
    active_trip_id: Optional[str] = None
    theme: str = "dark"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trips": [t.to_dict() for t in self.trips],
            "active_trip_id": self.active_trip_id,
            "theme": self.theme,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppState":
        return cls(
            trips=[Trip.from_dict(x) for x in data.get("trips", [])],
            active_trip_id=data.get("active_trip_id"),
            theme=data.get("theme", "dark"),
        )

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        for t in self.trips:
            if t.id == trip_id:
                return t
        return None

    def get_active_trip(self) -> Optional[Trip]:
        if self.active_trip_id is None:
            return None
        return self.get_trip_by_id(self.active_trip_id)

    def set_active_trip(self, trip_id: Optional[str]) -> None:
        self.active_trip_id = trip_id

    def add_trip(self, trip: Trip) -> None:
        self.trips.append(trip)
        self.active_trip_id = trip.id

    def delete_trip(self, trip_id: str) -> None:
        self.trips = [t for t in self.trips if t.id != trip_id]
        if self.active_trip_id == trip_id:
            self.active_trip_id = self.trips[0].id if self.trips else None


def new_trip(
    title: str,
    destination: str,
    start_date: date,
    end_date: date,
    accommodation: str = "",
    notes: str = "",
) -> Trip:
    return Trip(
        id=str(uuid4()),
        title=title,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        accommodation=accommodation,
        notes=notes,
    )


def create_sample_state() -> AppState:
    t = new_trip(
        "Weekend in Barcelona",
        "Barcelona, Spain",
        date(2025, 11, 14),
        date(2025, 11, 17),
        accommodation="Hotel Mediterraneo",
        notes="Tapas tour, Sagrada Familia tickets booked.",
    )

    t.budget_items.append(
        BudgetItem(
            id=str(uuid4()),
            category="Transport",
            description="Flights",
            cost=220.0,
            paid=True,
        )
    )
    t.budget_items.append(
        BudgetItem(
            id=str(uuid4()),
            category="Hotel",
            description="Hotel Mediterraneo (3 nights)",
            cost=300.0,
            paid=False,
        )
    )

    t.packing_items.append(
        PackingItem(
            id=str(uuid4()),
            item_name="Passport",
            category="Documents",
            quantity=1,
            place="Carry-on",
            packed=False,
        )
    )
    t.packing_items.append(
        PackingItem(
            id=str(uuid4()),
            item_name="Phone charger",
            category="Electronics",
            quantity=1,
            place="Carry-on",
            packed=False,
        )
    )
    t.packing_items.append(
        PackingItem(
            id=str(uuid4()),
            item_name="T-shirts",
            category="Clothes",
            quantity=3,
            place="Checked",
            packed=False,
        )
    )

    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 11, 14),
            time="12:00",
            title="Sagrada Familia entry",
            location="Sagrada Familia",
            notes="QR ticket in email",
        )
    )
    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 11, 14),
            time="18:00",
            title="Tapas walking tour",
            location="Gothic Quarter",
            notes="Meet guide near the cathedral",
        )
    )
    t.activities.append(
        ActivityItem(
            id=str(uuid4()),
            day=date(2025, 11, 15),
            time="10:30",
            title="Park Güell visit",
            location="Park Güell",
            notes="Buy water before climb",
        )
    )

    return AppState(trips=[t], active_trip_id=t.id, theme="dark")
