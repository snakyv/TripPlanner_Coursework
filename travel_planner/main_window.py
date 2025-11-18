from __future__ import annotations
from pathlib import Path
from typing import Dict

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QMessageBox,
    QDialog,
    QApplication,
)
from PyQt6.QtCore import Qt

from .models import AppState, Trip, new_trip
from .utils import date_range_str
from .storage import save_state
from .style import apply_theme
from .dialogs import TripEditorDialog
from .widgets.sidebar import SidebarWidget
from .pages.dashboard_page import DashboardPage
from .pages.itinerary_page import ItineraryPage
from .pages.trips_page import TripsPage
from .pages.budget_page import BudgetPage
from .pages.packing_page import PackingPage
from .pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self, state: AppState, storage_path: Path, parent=None):
        super().__init__(parent)
        self.state = state
        self.storage_path = storage_path

        self.setWindowTitle("TripPlanner — Travel Planning Assistant")
        self.resize(1200, 800)

        central = QWidget()
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = SidebarWidget()
        self.sidebar.navigateRequested.connect(self.handle_navigation)
        self.sidebar.newTripRequested.connect(self.open_add_trip_dialog)
        root_layout.addWidget(self.sidebar)

        right_wrapper = QVBoxLayout()
        right_wrapper.setContentsMargins(0, 0, 0, 0)
        right_wrapper.setSpacing(0)

        self.header_bar = QFrame()
        self.header_bar.setObjectName("HeaderBar")
        header_layout = QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(12)

        self.header_text_col = QVBoxLayout()
        self.header_text_col.setSpacing(2)

        self.header_trip_title_lbl = QLabel("No trip selected")
        self.header_trip_title_lbl.setProperty("role", "headerPrimary")
        self.header_text_col.addWidget(self.header_trip_title_lbl)

        self.header_trip_info_lbl = QLabel("")
        self.header_trip_info_lbl.setProperty("role", "headerSecondary")
        self.header_trip_info_lbl.setWordWrap(True)
        self.header_text_col.addWidget(self.header_trip_info_lbl)

        header_layout.addLayout(self.header_text_col)

        header_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.edit_trip_btn = QPushButton("Edit Trip")
        self.edit_trip_btn.setProperty("role", "ghost")
        self.edit_trip_btn.clicked.connect(self.open_edit_current_trip)
        header_layout.addWidget(self.edit_trip_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.setProperty("role", "ghost")
        self.save_btn.clicked.connect(self.force_save)
        header_layout.addWidget(self.save_btn)

        self.open_budget_btn = QPushButton("Open Budget")
        self.open_budget_btn.setProperty("role", "ghost")
        self.open_budget_btn.clicked.connect(lambda: self.handle_navigation("budget"))
        header_layout.addWidget(self.open_budget_btn)

        self.open_packing_btn = QPushButton("Open Packing")
        self.open_packing_btn.setProperty("role", "ghost")
        self.open_packing_btn.clicked.connect(lambda: self.handle_navigation("packing"))
        header_layout.addWidget(self.open_packing_btn)

        right_wrapper.addWidget(self.header_bar)

        self.pages_stack = QStackedWidget()

        self.dashboard_page = DashboardPage(self.state)
        self.itinerary_page = ItineraryPage(self.state)
        self.trips_page = TripsPage(self.state)
        self.budget_page = BudgetPage(self.state)
        self.packing_page = PackingPage(self.state)
        self.settings_page = SettingsPage(self.state)

        self.pages_stack.addWidget(self.dashboard_page)
        self.pages_stack.addWidget(self.itinerary_page)
        self.pages_stack.addWidget(self.trips_page)
        self.pages_stack.addWidget(self.budget_page)
        self.pages_stack.addWidget(self.packing_page)
        self.pages_stack.addWidget(self.settings_page)

        right_wrapper.addWidget(self.pages_stack)
        root_layout.addLayout(right_wrapper)
        self.setCentralWidget(central)

        self.trips_page.editTripRequested.connect(self.open_edit_trip_dialog_by_id)
        self.trips_page.deleteTripRequested.connect(self.delete_trip_by_id)
        self.trips_page.makeActiveTripRequested.connect(self.make_active_trip)

        self.budget_page.dataChanged.connect(self.state_changed)
        self.packing_page.dataChanged.connect(self.state_changed)
        self.itinerary_page.dataChanged.connect(self.state_changed)

        self.settings_page.themeChanged.connect(self.on_theme_changed)
        self.settings_page.requestSave.connect(self.force_save)

        self.page_key_to_index: Dict[str, int] = {
            "dashboard": 0,
            "itinerary": 1,
            "trips": 2,
            "budget": 3,
            "packing": 4,
            "settings": 5,
        }

        self.handle_navigation("dashboard")
        self.refresh_all_pages()

        apply_theme(QApplication.instance(), self.state.theme)

    def handle_navigation(self, page_key: str) -> None:
        idx = self.page_key_to_index.get(page_key, 0)
        self.pages_stack.setCurrentIndex(idx)
        self.sidebar.set_active_page(page_key)

        self.update_header()

    def state_changed(self) -> None:
        self.refresh_all_pages()
        self.force_save()

    def force_save(self) -> None:
        save_state(self.state, self.storage_path)

    def refresh_all_pages(self) -> None:
        self.dashboard_page.refresh()
        self.itinerary_page.refresh()
        self.trips_page.refresh()
        self.budget_page.refresh()
        self.packing_page.refresh()

        idx = self.settings_page.theme_combo.findText(self.state.theme)
        if idx != -1:
            self.settings_page.theme_combo.setCurrentIndex(idx)

        self.update_header()

    def update_header(self) -> None:
        trip = self.state.get_active_trip()
        if trip is None:
            self.header_trip_title_lbl.setText("No trip selected")
            self.header_trip_info_lbl.setText("Create a new trip or activate one from the Trips page.")
            self.edit_trip_btn.setEnabled(False)
            self.open_budget_btn.setEnabled(False)
            self.open_packing_btn.setEnabled(False)
            return

        self.header_trip_title_lbl.setText(f"{trip.title} — {trip.destination}")
        self.header_trip_info_lbl.setText(
            f"{date_range_str(trip.start_date, trip.end_date)}"
            + (f" | Stay: {trip.accommodation}" if trip.accommodation else "")
        )
        self.edit_trip_btn.setEnabled(True)
        self.open_budget_btn.setEnabled(True)
        self.open_packing_btn.setEnabled(True)

    def open_add_trip_dialog(self) -> None:
        dlg = TripEditorDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if data:
                t = new_trip(
                    title=data["title"],
                    destination=data["destination"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    accommodation=data["accommodation"],
                    notes=data["notes"],
                )
                self.state.add_trip(t)
                self.state_changed()
                self.handle_navigation("trips")

    def open_edit_current_trip(self) -> None:
        trip = self.state.get_active_trip()
        if trip is None:
            return
        self._edit_trip_common(trip)

    def open_edit_trip_dialog_by_id(self, trip_id: str) -> None:
        trip = self.state.get_trip_by_id(trip_id)
        if trip is None:
            return
        self._edit_trip_common(trip)

    def _edit_trip_common(self, trip: Trip) -> None:
        dlg = TripEditorDialog(self, trip=trip)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if data:
                trip.title = data["title"]
                trip.destination = data["destination"]
                trip.accommodation = data["accommodation"]
                trip.start_date = data["start_date"]
                trip.end_date = data["end_date"]
                trip.notes = data["notes"]
                self.state_changed()

    def delete_trip_by_id(self, trip_id: str) -> None:
        trip = self.state.get_trip_by_id(trip_id)
        if trip is None:
            return
        reply = QMessageBox.question(
            self,
            "Delete trip",
            f"Are you sure you want to delete '{trip.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.state.delete_trip(trip_id)
            self.state_changed()

    def make_active_trip(self, trip_id: str) -> None:
        self.state.set_active_trip(trip_id)
        self.state_changed()

    def on_theme_changed(self, theme: str) -> None:
        apply_theme(QApplication.instance(), theme)
        self.state.theme = theme
        self.force_save()
