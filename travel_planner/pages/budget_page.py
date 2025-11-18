from __future__ import annotations
from uuid import uuid4
from typing import List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QAbstractItemView,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..models import AppState, BudgetItem
from ..utils import money, date_range_str
from ..dialogs import BudgetItemDialog


class BudgetPage(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self._loading = False
        self.row_to_id: List[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_lbl = QLabel("Budget")
        header_lbl.setProperty("role", "headerPrimary")
        layout.addWidget(header_lbl)

        self.trip_info_lbl = QLabel("")
        self.trip_info_lbl.setProperty("role", "headerSecondary")
        layout.addWidget(self.trip_info_lbl)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Category", "Description", "Cost (€)", "Paid"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, self.table.horizontalHeader().ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, self.table.horizontalHeader().ResizeMode.Stretch)
        self.table.setMinimumHeight(240)
        self.table.itemChanged.connect(self.on_item_changed)

        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.add_btn = QPushButton("Add item")
        self.add_btn.setProperty("role", "primary")
        self.add_btn.clicked.connect(self.on_add_item)
        btn_row.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Remove selected")
        self.remove_btn.setProperty("role", "ghost")
        self.remove_btn.clicked.connect(self.on_remove_selected)
        btn_row.addWidget(self.remove_btn)

        btn_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(btn_row)

        self.summary_lbl = QLabel("")
        self.summary_lbl.setProperty("role", "headerSecondary")
        layout.addWidget(self.summary_lbl)

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.refresh()

    def _current_trip(self):
        return self.state.get_active_trip()

    def refresh(self):
        trip = self._current_trip()
        self._loading = True

        if trip is None:
            self.trip_info_lbl.setText("No active trip selected")
        else:
            self.trip_info_lbl.setText(
                f"{trip.title} — {trip.destination} | {date_range_str(trip.start_date, trip.end_date)}"
            )

        # Содержимое таблицы
        self.table.clearContents()
        self.row_to_id.clear()

        if trip is None:
            self.table.setRowCount(0)
        else:
            self.table.setRowCount(len(trip.budget_items))
            for row, bi in enumerate(trip.budget_items):
                self.row_to_id.append(bi.id)

                it_cat = QTableWidgetItem(bi.category)
                it_desc = QTableWidgetItem(bi.description)
                it_cost = QTableWidgetItem(f"{bi.cost:.2f}")
                it_cost.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                it_paid = QTableWidgetItem("Paid" if bi.paid else "")
                it_paid.setFlags(it_paid.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                it_paid.setCheckState(Qt.CheckState.Checked if bi.paid else Qt.CheckState.Unchecked)
                it_paid.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row, 0, it_cat)
                self.table.setItem(row, 1, it_desc)
                self.table.setItem(row, 2, it_cost)
                self.table.setItem(row, 3, it_paid)

        self._loading = False
        self.update_summary_labels()
        self.update_enabled_state()

    def update_enabled_state(self):
        has_trip = self._current_trip() is not None
        self.table.setEnabled(has_trip)
        self.add_btn.setEnabled(has_trip)
        self.remove_btn.setEnabled(has_trip)

    def update_summary_labels(self):
        trip = self._current_trip()
        if trip is None:
            self.summary_lbl.setText("")
            return
        self.summary_lbl.setText(
            f"Total: {money(trip.total_budget())} | Paid: {money(trip.total_paid())} | Remaining: {money(trip.total_remaining())}"
        )

    def on_add_item(self):
        trip = self._current_trip()
        if trip is None:
            return
        dlg = BudgetItemDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            new_item = BudgetItem(
                id=str(uuid4()),
                category=data["category"],
                description=data["description"],
                cost=float(data["cost"]),
                paid=bool(data["paid"]),
            )
            trip.budget_items.append(new_item)
            self.dataChanged.emit()
            self.refresh()

    def on_remove_selected(self):
        trip = self._current_trip()
        if trip is None:
            return
        sel_ranges = self.table.selectedRanges()
        if not sel_ranges:
            return
        row_to_remove = sel_ranges[0].topRow()
        if 0 <= row_to_remove < len(self.row_to_id):
            bid = self.row_to_id[row_to_remove]
            trip.budget_items = [bi for bi in trip.budget_items if bi.id != bid]
            self.dataChanged.emit()
            self.refresh()

    def on_item_changed(self, item: QTableWidgetItem):
        if self._loading:
            return
        trip = self._current_trip()
        if trip is None:
            return
        row = item.row()
        col = item.column()
        if row < 0 or row >= len(self.row_to_id):
            return
        bid = self.row_to_id[row]
        bi = next((x for x in trip.budget_items if x.id == bid), None)
        if bi is None:
            return

        if col == 0:
            bi.category = item.text().strip()
        elif col == 1:
            bi.description = item.text().strip()
        elif col == 2:
            try:
                bi.cost = float(item.text())
            except ValueError:
                pass
        elif col == 3:
            bi.paid = (item.checkState() == Qt.CheckState.Checked)

        self.update_summary_labels()
        self.dataChanged.emit()
