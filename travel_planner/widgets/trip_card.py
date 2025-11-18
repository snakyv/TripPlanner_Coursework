from __future__ import annotations
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import pyqtSignal

from ..models import Trip
from ..utils import date_range_str, money


class TripCardWidget(QFrame):
    editRequested = pyqtSignal(str)
    deleteRequested = pyqtSignal(str)
    selectRequested = pyqtSignal(str)

    def __init__(self, trip: Trip, is_active: bool = False, parent=None):
        super().__init__(parent)

        self.setObjectName("CardActive" if is_active else "Card")
        self._trip_id = trip.id

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(8)

        self.title_label = QLabel()
        self.title_label.setProperty("role", "cardTitle")
        self.main_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel()
        self.subtitle_label.setProperty("role", "cardSubtitle")
        self.subtitle_label.setWordWrap(True)
        self.main_layout.addWidget(self.subtitle_label)

        self.budget_label = QLabel()
        self.budget_label.setProperty("role", "cardSubtitle")
        self.main_layout.addWidget(self.budget_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.active_btn = QPushButton("Set Active")
        self.active_btn.setProperty("role", "ghost")
        self.active_btn.clicked.connect(lambda: self.selectRequested.emit(self._trip_id))
        btn_row.addWidget(self.active_btn)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setProperty("role", "ghost")
        self.edit_btn.clicked.connect(lambda: self.editRequested.emit(self._trip_id))
        btn_row.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setProperty("role", "ghost")
        self.delete_btn.clicked.connect(lambda: self.deleteRequested.emit(self._trip_id))
        btn_row.addWidget(self.delete_btn)

        btn_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.main_layout.addLayout(btn_row)

        self.set_trip(trip, is_active)

    def set_trip(self, trip: Trip, is_active: bool = False) -> None:
        self._trip_id = trip.id

        active_marker = " (Active)" if is_active else ""
        self.title_label.setText(f"{trip.title}{active_marker} — {trip.destination}")

        self.subtitle_label.setText(
            f"{date_range_str(trip.start_date, trip.end_date)}"
            + (f" | Stay: {trip.accommodation}" if trip.accommodation else "")
        )

        self.budget_label.setText(
            f"Budget: {money(trip.total_budget())} | Paid: {money(trip.total_paid())} | Remaining: {money(trip.total_remaining())}"
        )

        self.active_btn.setText("Active" if is_active else "Set Active")
        self.active_btn.setEnabled(not is_active)

        self.setObjectName("CardActive" if is_active else "Card")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
