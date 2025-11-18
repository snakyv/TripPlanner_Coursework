from pathlib import Path
from PyQt6.QtWidgets import QMainWindow

from travel_planner.main_window import MainWindow
from travel_planner.models import AppState
from travel_planner.pages.dashboard_page import DashboardPage
from travel_planner.pages.itinerary_page import ItineraryPage
from travel_planner.pages.trips_page import TripsPage
from travel_planner.pages.budget_page import BudgetPage
from travel_planner.pages.packing_page import PackingPage
from travel_planner.pages.settings_page import SettingsPage


def test_mainwindow_smoke(qtbot, sample_state: AppState, tmp_storage_path: Path):

    win = MainWindow(sample_state, tmp_storage_path)
    qtbot.addWidget(win)

    assert isinstance(win, QMainWindow)

    assert win.pages_stack.count() == 6

    assert isinstance(win.pages_stack.widget(0), DashboardPage)
    assert isinstance(win.pages_stack.widget(1), ItineraryPage)
    assert isinstance(win.pages_stack.widget(2), TripsPage)
    assert isinstance(win.pages_stack.widget(3), BudgetPage)
    assert isinstance(win.pages_stack.widget(4), PackingPage)
    assert isinstance(win.pages_stack.widget(5), SettingsPage)

    assert win.sidebar is not None

    active_trip = sample_state.get_active_trip()
    if active_trip is not None:
        assert active_trip.title in win.header_trip_title_lbl.text()
        assert active_trip.destination in win.header_trip_title_lbl.text()

        assert win.open_budget_btn.isEnabled()
        assert win.open_packing_btn.isEnabled()
    else:
        assert "No trip selected" in win.header_trip_title_lbl.text()
