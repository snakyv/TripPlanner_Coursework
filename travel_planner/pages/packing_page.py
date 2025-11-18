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

from ..models import AppState, PackingItem
from ..dialogs import PackingItemDialog
from ..utils import date_range_str


class PackingPage(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self._loading = False
        self.row_to_id: List[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_lbl = QLabel("Packing checklist")
        header_lbl.setProperty("role", "headerPrimary")
        layout.addWidget(header_lbl)

        self.trip_info_lbl = QLabel("")
        self.trip_info_lbl.setProperty("role", "headerSecondary")
        layout.addWidget(self.trip_info_lbl)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Item", "Category", "Qty", "Place", "Packed"])
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

        self.table.clearContents()
        self.row_to_id.clear()

        if trip is None:
            self.table.setRowCount(0)
        else:
            self.table.setRowCount(len(trip.packing_items))
            for row, pi in enumerate(trip.packing_items):
                self.row_to_id.append(pi.id)

                it_item = QTableWidgetItem(pi.item_name)
                it_cat = QTableWidgetItem(pi.category)

                it_qty = QTableWidgetItem(str(pi.quantity))
                it_qty.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                it_place = QTableWidgetItem(pi.place)
                it_place.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                it_packed = QTableWidgetItem("Packed" if pi.packed else "")
                it_packed.setFlags(it_packed.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                it_packed.setCheckState(Qt.CheckState.Checked if pi.packed else Qt.CheckState.Unchecked)
                it_packed.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row, 0, it_item)
                self.table.setItem(row, 1, it_cat)
                self.table.setItem(row, 2, it_qty)
                self.table.setItem(row, 3, it_place)
                self.table.setItem(row, 4, it_packed)

        self._loading = False
        self.update_enabled_state()

    def update_enabled_state(self):
        has_trip = self._current_trip() is not None
        self.table.setEnabled(has_trip)
        self.add_btn.setEnabled(has_trip)
        self.remove_btn.setEnabled(has_trip)

    def on_add_item(self):
        trip = self._current_trip()
        if trip is None:
            return
        dlg = PackingItemDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            new_item = PackingItem(
                id=str(uuid4()),
                item_name=data["item_name"],
                category=data["category"],
                quantity=int(data["quantity"]),
                place=data["place"],
                packed=bool(data["packed"]),
            )
            trip.packing_items.append(new_item)
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
            pid = self.row_to_id[row_to_remove]
            trip.packing_items = [pi for pi in trip.packing_items if pi.id != pid]
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
        pid = self.row_to_id[row]
        pi = next((x for x in trip.packing_items if x.id == pid), None)
        if pi is None:
            return

        if col == 0:
            pi.item_name = item.text().strip()
        elif col == 1:
            pi.category = item.text().strip()
        elif col == 2:
            try:
                pi.quantity = int(item.text())
            except ValueError:
                pass
        elif col == 3:
            pi.place = item.text().strip()
        elif col == 4:
            pi.packed = (item.checkState() == Qt.CheckState.Checked)

        self.dataChanged.emit()
