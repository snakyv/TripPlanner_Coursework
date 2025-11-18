from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import pyqtSignal


class SidebarWidget(QFrame):
    navigateRequested = pyqtSignal(str)
    newTripRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setMinimumWidth(200)
        self.setMaximumWidth(220)

        self.nav_buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_label = QLabel("TripPlanner")
        title_label.setProperty("role", "title")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        self._add_nav_button(layout, "Dashboard", "dashboard")
        self._add_nav_button(layout, "Itinerary", "itinerary")
        self._add_nav_button(layout, "Trips", "trips")
        self._add_nav_button(layout, "Budget", "budget")
        self._add_nav_button(layout, "Packing", "packing")
        self._add_nav_button(layout, "Settings", "settings")

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        new_trip_btn = QPushButton("+ New trip")
        new_trip_btn.setProperty("role", "primary")
        new_trip_btn.clicked.connect(self.newTripRequested.emit)
        layout.addWidget(new_trip_btn)

    def _add_nav_button(self, parent_layout: QVBoxLayout, text: str, page_key: str):
        btn = QPushButton(text)
        btn.setProperty("role", "nav")
        btn.setProperty("page_key", page_key)
        btn.setCheckable(False)
        btn.clicked.connect(lambda _, k=page_key: self.navigateRequested.emit(k))
        parent_layout.addWidget(btn)
        self.nav_buttons[page_key] = btn

    def set_active_page(self, page_key: str):
        for key, btn in self.nav_buttons.items():
            btn.setProperty("active", "true" if key == page_key else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
