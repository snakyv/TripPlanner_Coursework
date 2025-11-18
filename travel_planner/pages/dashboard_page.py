from __future__ import annotations
from datetime import date as _Date
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt

from ..models import AppState
from ..utils import date_range_str, money, human_date, get_upcoming_activity


class DashboardPage(QWidget):

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        self.active_trip_card = QFrame()
        self.active_trip_card.setObjectName("Card")
        atc_layout = QVBoxLayout(self.active_trip_card)
        atc_layout.setContentsMargins(16, 16, 16, 16)
        atc_layout.setSpacing(8)

        self.trip_title_lbl = QLabel()
        self.trip_title_lbl.setProperty("role", "cardTitle")
        atc_layout.addWidget(self.trip_title_lbl)

        self.trip_info_lbl = QLabel()
        self.trip_info_lbl.setProperty("role", "cardSubtitle")
        self.trip_info_lbl.setWordWrap(True)
        atc_layout.addWidget(self.trip_info_lbl)

        self.budget_info_lbl = QLabel()
        self.budget_info_lbl.setProperty("role", "cardSubtitle")
        self.budget_info_lbl.setWordWrap(True)
        atc_layout.addWidget(self.budget_info_lbl)

        self.notes_lbl = QLabel()
        self.notes_lbl.setProperty("role", "cardSubtitle")
        self.notes_lbl.setWordWrap(True)
        atc_layout.addWidget(self.notes_lbl)

        self.layout.addWidget(self.active_trip_card)

        self.next_activity_card = QFrame()
        self.next_activity_card.setObjectName("Card")
        nac_layout = QVBoxLayout(self.next_activity_card)
        nac_layout.setContentsMargins(16, 16, 16, 16)
        nac_layout.setSpacing(8)

        self.next_activity_title_lbl = QLabel("Next activity")
        self.next_activity_title_lbl.setProperty("role", "cardTitle")
        nac_layout.addWidget(self.next_activity_title_lbl)

        self.next_activity_info_lbl = QLabel()
        self.next_activity_info_lbl.setProperty("role", "cardSubtitle")
        self.next_activity_info_lbl.setWordWrap(True)
        nac_layout.addWidget(self.next_activity_info_lbl)

        self.layout.addWidget(self.next_activity_card)

        self.refresh()

    def refresh(self):
        trip = self.state.get_active_trip()
        if trip is None:
            self.trip_title_lbl.setText("No active trip")
            self.trip_info_lbl.setText("Select or create a trip.")
            self.budget_info_lbl.setText("")
            self.notes_lbl.setText("")
            self.next_activity_info_lbl.setText("No activities scheduled.")
            return

        self.trip_title_lbl.setText(f"{trip.title} — {trip.destination}")
        self.trip_info_lbl.setText(
            f"{date_range_str(trip.start_date, trip.end_date)}"
            + (f" | Stay: {trip.accommodation}" if trip.accommodation else "")
        )

        self.budget_info_lbl.setText(
            f"Budget: {money(trip.total_budget())} | Paid: {money(trip.total_paid())} | Remaining: {money(trip.total_remaining())}"
        )

        if trip.notes:
            self.notes_lbl.setText(f"Notes: {trip.notes}")
        else:
            self.notes_lbl.setText("Notes: —")

        upcoming = get_upcoming_activity(trip, _Date.today())
        if upcoming:
            self.next_activity_info_lbl.setText(
                f"{human_date(upcoming.day)} {upcoming.time} — {upcoming.title} ({upcoming.location})"
                + (f". {upcoming.notes}" if upcoming.notes else "")
            )
        else:
            self.next_activity_info_lbl.setText("No upcoming activity.")
