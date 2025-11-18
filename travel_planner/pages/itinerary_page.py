from __future__ import annotations
from uuid import uuid4
from typing import Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QDialog,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette

from ..models import AppState, ActivityItem
from ..utils import date_range_str, human_date, activity_sort_key
from ..dialogs import ActivityItemDialog


class ItineraryPage(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self.day_cards: List[QFrame] = []

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(20, 20, 20, 20)
        page_layout.setSpacing(12)

        header_lbl = QLabel("Itinerary")
        header_lbl.setProperty("role", "headerPrimary")
        page_layout.addWidget(header_lbl)

        self.trip_info_lbl = QLabel("")
        self.trip_info_lbl.setProperty("role", "headerSecondary")
        self.trip_info_lbl.setWordWrap(True)
        page_layout.addWidget(self.trip_info_lbl)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(14)

        page_layout.addWidget(self.scroll_area)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.add_btn = QPushButton("Add activity")
        self.add_btn.setProperty("role", "primary")
        self.add_btn.clicked.connect(self.on_add_activity)
        btn_row.addWidget(self.add_btn)

        btn_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        page_layout.addLayout(btn_row)

        page_layout.addStretch(1)

        self.apply_theme_styles()

        self.refresh()

    def _current_trip(self):
        return self.state.get_active_trip()

    def apply_theme_styles(self):
        app = QApplication.instance()
        palette = app.palette() if app else QPalette()
        window_color = palette.color(QPalette.ColorRole.Window)
        is_dark = window_color.lightness() < 128

        if is_dark:
            self.setStyleSheet("""
                QFrame#DayCard {
                    border: 1px solid #3a3f45;
                    border-radius: 6px;
                    background: #1e1f22;
                }
                QFrame#ActivityCard {
                    border: 1px solid #2b2f33;
                    border-radius: 6px;
                    background: #252627;
                }
                QLabel[role="cardTitle"] { font-weight: 600; font-size: 13px; color: #e6eefc; }
                QLabel[role="activityTime"] { color: #7fb4ff; font-weight: 600; }
                QLabel[role="activityTitle"] { font-size: 12px; color: #ffffff; }
                QLabel[role="activityMeta"] { color: #aab3c0; font-size: 11px; }
                QLabel[role="headerPrimary"] { font-size: 18px; font-weight: 700; color: #ffffff; }
                QLabel[role="headerSecondary"] { font-size: 13px; color: #d0d6dd; }
            """)
        else:
            self.setStyleSheet("""
                QFrame#DayCard {
                    border: 1px solid #d0d7e6;
                    border-radius: 6px;
                    background: #ffffff;
                }
                QFrame#ActivityCard {
                    border: 1px solid #e6eefc;
                    border-radius: 6px;
                    background: #f8fbff;
                }
                QLabel[role="cardTitle"] { font-weight: 600; font-size: 13px; color: #1b2a4a; }
                QLabel[role="activityTime"] { color: #2a5cb6; font-weight: 600; }
                QLabel[role="activityTitle"] { font-size: 12px; color: #0b1b33; }
                QLabel[role="activityMeta"] { color: #5b6b82; font-size: 11px; }
                QLabel[role="headerPrimary"] { font-size: 18px; font-weight: 700; color: #0b1b33; }
                QLabel[role="headerSecondary"] { font-size: 13px; color: #334155; }
            """)

    def refresh(self):
        trip = self._current_trip()

        if trip is None:
            self.trip_info_lbl.setText("No active trip selected")
        else:
            self.trip_info_lbl.setText(
                f"{trip.title} — {trip.destination} | {date_range_str(trip.start_date, trip.end_date)}"
            )

        for card in self.day_cards:
            card.setParent(None)
        self.day_cards.clear()

        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(None)

        if trip is None:
            placeholder = QLabel("No activities to show")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setContentsMargins(8, 8, 8, 8)
            self.scroll_layout.addWidget(placeholder)
            self.update_enabled_state()
            return

        day_map: Dict[object, List[ActivityItem]] = {}
        for act in trip.activities:
            day_map.setdefault(act.day, []).append(act)

        for d in sorted(day_map.keys(), key=lambda dt: dt.toordinal()):
            acts = sorted(day_map[d], key=activity_sort_key)

            day_card = QFrame()
            day_card.setObjectName("DayCard")
            day_card.setProperty("role", "dayCard")
            dc_layout = QVBoxLayout(day_card)
            dc_layout.setContentsMargins(12, 12, 12, 12)
            dc_layout.setSpacing(10)

            day_label = QLabel(human_date(d))
            day_label.setProperty("role", "cardTitle")
            day_label.setMinimumHeight(20)
            dc_layout.addWidget(day_label)

            for a in acts:
                activity_frame = QFrame()
                activity_frame.setObjectName("ActivityCard")
                activity_layout = QVBoxLayout(activity_frame)
                activity_layout.setContentsMargins(10, 8, 10, 8)
                activity_layout.setSpacing(6)

                top_row = QHBoxLayout()
                top_row.setSpacing(8)

                time_lbl = QLabel(str(a.time))
                time_lbl.setProperty("role", "activityTime")
                time_lbl.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
                top_row.addWidget(time_lbl, 0, Qt.AlignmentFlag.AlignLeft)

                title_lbl = QLabel(a.title)
                title_lbl.setProperty("role", "activityTitle")
                title_lbl.setWordWrap(True)
                title_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                top_row.addWidget(title_lbl, 1)

                activity_layout.addLayout(top_row)

                meta_texts = []
                if a.location:
                    meta_texts.append(a.location)
                if a.notes:
                    meta_texts.append(a.notes)

                if meta_texts:
                    meta_lbl = QLabel(" · ".join(meta_texts))
                    meta_lbl.setProperty("role", "activityMeta")
                    meta_lbl.setWordWrap(True)
                    meta_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    activity_layout.addWidget(meta_lbl)

                activity_frame.setMinimumHeight(48)
                activity_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                dc_layout.addWidget(activity_frame)

            self.scroll_layout.addWidget(day_card)
            self.day_cards.append(day_card)

        self.scroll_layout.addStretch(1)

        self.update_enabled_state()

    def update_enabled_state(self):
        has_trip = self._current_trip() is not None
        self.add_btn.setEnabled(has_trip)

    def on_add_activity(self):
        trip = self._current_trip()
        if trip is None:
            return
        dlg = ActivityItemDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if data:
                new_act = ActivityItem(
                    id=str(uuid4()),
                    day=data["day"],
                    time=data["time"],
                    title=data["title"],
                    location=data["location"],
                    notes=data["notes"],
                )
                trip.activities.append(new_act)
                self.dataChanged.emit()
                self.refresh()