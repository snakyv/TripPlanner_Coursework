from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import pyqtSignal

from ..models import AppState
from ..widgets.trip_card import TripCardWidget


class TripsPage(QWidget):
    editTripRequested = pyqtSignal(str)
    deleteTripRequested = pyqtSignal(str)
    makeActiveTripRequested = pyqtSignal(str)

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self.card_widgets: list[TripCardWidget] = []

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(16)

        header_lbl = QLabel("Your trips")
        header_lbl.setProperty("role", "headerPrimary")
        page_layout.addWidget(header_lbl)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(12)

        page_layout.addWidget(self.scroll_area)

        page_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.refresh()

    def refresh(self):
        for cw in self.card_widgets:
            cw.setParent(None)
        self.card_widgets.clear()

        active_id = self.state.active_trip_id

        for trip in self.state.trips:
            card = TripCardWidget(trip, is_active=(trip.id == active_id), parent=self.scroll_content)
            card.editRequested.connect(self.editTripRequested.emit)
            card.deleteRequested.connect(self.deleteTripRequested.emit)
            card.selectRequested.connect(self.makeActiveTripRequested.emit)

            self.scroll_layout.addWidget(card)
            self.card_widgets.append(card)

        self.scroll_layout.addStretch(1)
