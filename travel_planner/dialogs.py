from __future__ import annotations
from datetime import date
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QTimeEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QCheckBox,
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, QDate, QTime

from .models import Trip


class TripEditorDialog(QDialog):

    def __init__(self, parent=None, trip: Trip | None = None):
        super().__init__(parent)
        self.setWindowTitle("Trip details")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_edit = QLineEdit()
        self.dest_edit = QLineEdit()
        self.accomm_edit = QLineEdit()

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes (visa, tickets, ideas...)")

        form.addRow("Title:", self.title_edit)
        form.addRow("Destination:", self.dest_edit)
        form.addRow("Accommodation:", self.accomm_edit)
        form.addRow("Start date:", self.start_date_edit)
        form.addRow("End date:", self.end_date_edit)
        form.addRow("Notes:", self.notes_edit)

        layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self._handle_accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

        if trip:
            self.title_edit.setText(trip.title)
            self.dest_edit.setText(trip.destination)
            self.accomm_edit.setText(trip.accommodation)

            self.start_date_edit.setDate(QDate(trip.start_date.year, trip.start_date.month, trip.start_date.day))
            self.end_date_edit.setDate(QDate(trip.end_date.year, trip.end_date.month, trip.end_date.day))

            self.notes_edit.setText(trip.notes)
        else:
            today_qd = QDate.currentDate()
            self.start_date_edit.setDate(today_qd)
            self.end_date_edit.setDate(today_qd.addDays(2))

        self._accepted = False

    def _handle_accept(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
            return
        if not self.dest_edit.text().strip():
            self.dest_edit.setFocus()
            return

        sd_qd = self.start_date_edit.date()
        ed_qd = self.end_date_edit.date()
        sd = date(sd_qd.year(), sd_qd.month(), sd_qd.day())
        ed = date(ed_qd.year(), ed_qd.month(), ed_qd.day())
        if ed < sd:
            self.end_date_edit.setFocus()
            return

        self._accepted = True
        self.accept()

    def get_data(self) -> dict | None:
        if not self._accepted:
            return None
        sd_qd = self.start_date_edit.date()
        ed_qd = self.end_date_edit.date()
        return {
            "title": self.title_edit.text().strip(),
            "destination": self.dest_edit.text().strip(),
            "accommodation": self.accomm_edit.text().strip(),
            "start_date": date(sd_qd.year(), sd_qd.month(), sd_qd.day()),
            "end_date": date(ed_qd.year(), ed_qd.month(), ed_qd.day()),
            "notes": self.notes_edit.toPlainText().strip(),
        }


class BudgetItemDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add budget item")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.category_edit = QLineEdit()
        self.desc_edit = QLineEdit()

        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setDecimals(2)
        self.cost_spin.setRange(0.0, 1_000_000.0)
        self.cost_spin.setSingleStep(1.0)

        self.paid_check = QCheckBox("Already paid")

        form.addRow("Category:", self.category_edit)
        form.addRow("Description:", self.desc_edit)
        form.addRow("Cost (€):", self.cost_spin)
        form.addRow("", self.paid_check)

        layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_data(self) -> dict:
        return {
            "category": self.category_edit.text().strip(),
            "description": self.desc_edit.text().strip(),
            "cost": float(self.cost_spin.value()),
            "paid": bool(self.paid_check.isChecked()),
        }


class PackingItemDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add packing item")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.item_edit = QLineEdit()
        self.cat_edit = QLineEdit()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 999)
        self.quantity_spin.setValue(1)

        self.place_combo = QComboBox()
        self.place_combo.addItems(["Carry-on", "Checked"])

        self.packed_check = QCheckBox("Already packed")

        form.addRow("Item:", self.item_edit)
        form.addRow("Category:", self.cat_edit)
        form.addRow("Quantity:", self.quantity_spin)
        form.addRow("Place:", self.place_combo)
        form.addRow("", self.packed_check)

        layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_data(self) -> dict:
        return {
            "item_name": self.item_edit.text().strip(),
            "category": self.cat_edit.text().strip(),
            "quantity": int(self.quantity_spin.value()),
            "place": self.place_combo.currentText(),
            "packed": bool(self.packed_check.isChecked()),
        }


class ActivityItemDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add activity / itinerary item")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.day_edit = QDateEdit()
        self.day_edit.setCalendarPopup(True)
        self.day_edit.setDate(QDate.currentDate())

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())

        self.title_edit = QLineEdit()
        self.location_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes, tickets, meeting point...")

        form.addRow("Day:", self.day_edit)
        form.addRow("Time:", self.time_edit)
        form.addRow("Title:", self.title_edit)
        form.addRow("Location:", self.location_edit)
        form.addRow("Notes:", self.notes_edit)

        layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self._handle_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self._accepted = False

    def _handle_accept(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
            return
        self._accepted = True
        self.accept()

    def get_data(self) -> dict | None:
        if not self._accepted:
            return None
        qd = self.day_edit.date()
        qt = self.time_edit.time()
        return {
            "day": date(qd.year(), qd.month(), qd.day()),
            "time": f"{qt.hour():02d}:{qt.minute():02d}",
            "title": self.title_edit.text().strip(),
            "location": self.location_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip(),
        }
