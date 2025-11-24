# TripPlanner — desktop trip planner built with PyQt6

> Educational desktop tool for planning trips created as part of the course **“User Interface and Software Development & Prototyping”** (Odesa Polytechnic National University, 2025).

![Status](https://img.shields.io/badge/status-coursework-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyQt](https://img.shields.io/badge/PyQt-6.5-green)

---

## 📌 Project overview

**TripPlanner** is a desktop application for trip planning, built in **Python** using **PyQt6**.

The goal of the app is to bring all key aspects of trip preparation together in one place:

- day-by-day itinerary;
- packing list;
- budget and expenses.

The app works completely **offline**, stores all data in a local **JSON file**, supports **light and dark themes**, and focuses on simplicity and intuitive use.

---

## ✨ Key features

- **Multiple trips in one app**
  - create, edit, and delete trips;
  - store trip name, destination, start and end dates.

- **Detailed itinerary**
  - plan activities by day;
  - each item has date, time, description, location, and notes;
  - automatic sorting by date and time.

- **Packing list**
  - checklist of items with “packed” status;
  - individual packing list for each trip.

- **Trip budget**
  - add expense items with categories and amounts;
  - calculate total spending.

- **Themes**
  - light and dark theme;
  - theme switcher in Settings;
  - selected theme is saved between app runs.

- **Autosave and state restore**
  - all data is stored in `travel_data.json`;
  - on startup the app loads the last saved state;
  - if the file is missing, a demo trip can be created.

---

## 🧭 Interface and navigation

The main window consists of:

- **sidebar** — navigation between sections:
  - `Trips` — list of trips;
  - `Itinerary` — itinerary for the selected trip;
  - `Packing List` — packing checklist;
  - `Budget` — trip budget;
  - `Settings` — settings (including theme);
- **content area**, which displays the active page.

Main pages:

- **TripsPage**
  - list of all trips as cards (`TripCard`);
  - “Add trip” button;
  - edit and delete actions via buttons on each card.

- **ItineraryPage**
  - activities grouped by date;
  - activity widget with time, title, and edit/delete buttons;
  - dialog window for adding/editing an activity.

- **PackingPage**
  - list of items with checkboxes;
  - add/remove items.

- **BudgetPage**
  - table / list of budget entries;
  - amount input with validation (minimum 0);
  - automatic calculation of total amount.

- **SettingsPage**
  - theme switch (Light/Dark);
  - other basic settings.

---

## 🏗 Architecture and technologies

**Stack:**

- language: **Python 3.x**
- GUI framework: **PyQt6 (≈ 6.5)**
- storage format: **JSON**
- paradigms:
  - object-oriented programming;
  - event-driven model (Qt signals/slots).

**Core model classes:**

- `AppState` — global application state (list of trips, active theme, etc.);
- `Trip` — single trip (id, name, destination, start/end dates, collections of activities, packing items, budget items);
- `ActivityItem` — itinerary item (date, time, description, location, notes);
- `PackingItem` — packing list item (name + “packed” flag);
- `BudgetItem` — budget entry (category, description, amount).

Serialization is implemented via `to_dict()` / `from_dict()` for each class; dates and times are stored in **ISO 8601** format (`YYYY-MM-DD`, `HH:MM`).

**Logical project structure:**

```text
TripPlanner_Coursework/
├── main.py                # Entry point, creates QApplication and MainWindow
├── travel_data.json       # State file with trip data
├── travel_planner/
│   ├── __init__.py
│   ├── models.py          # AppState, Trip, ActivityItem, PackingItem, BudgetItem
│   ├── storage.py         # load_state() / save_state(), create_sample_state()
│   ├── style.py           # theme palettes and switching logic
│   ├── dialogs.py         # TripEditorDialog, ActivityItemDialog, other dialogs
│   ├── pages/
│   │   ├── dashboard_page.py
│   │   ├── trips_page.py
│   │   ├── itinerary_page.py
│   │   ├── packing_page.py
│   │   ├── budget_page.py
│   │   └── settings_page.py
│   └── widgets/
│       ├── sidebar.py     # Sidebar navigation menu
│       └── trip_card.py   # Trip card in the list
└── tests/
    ├── test_models.py
    ├── test_storage.py
    └── ...
