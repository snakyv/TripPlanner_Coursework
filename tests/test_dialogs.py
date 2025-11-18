from datetime import date
from PyQt6.QtCore import QDate, QTime
from PyQt6.QtWidgets import QDialog

from travel_planner.dialogs import TripEditorDialog, PackingItemDialog, ActivityItemDialog


def test_trip_editor_dialog_valid(qtbot):
    dlg = TripEditorDialog()
    qtbot.addWidget(dlg)

    dlg.title_edit.setText("Berlin Weekend")
    dlg.dest_edit.setText("Berlin, Germany")
    dlg.accomm_edit.setText("Hotel Central")

    dlg.start_date_edit.setDate(QDate(2025, 5, 10))
    dlg.end_date_edit.setDate(QDate(2025, 5, 12))

    dlg.notes_edit.setPlainText("Check U-Bahn tickets")

    dlg._handle_accept()

    assert dlg.result() == QDialog.DialogCode.Accepted
    data = dlg.get_data()
    assert data is not None
    assert data["title"] == "Berlin Weekend"
    assert data["destination"] == "Berlin, Germany"
    assert data["start_date"] == date(2025, 5, 10)
    assert data["end_date"] == date(2025, 5, 12)
    assert "U-Bahn" in data["notes"]


def test_trip_editor_dialog_invalid_date(qtbot):
    dlg = TripEditorDialog()
    qtbot.addWidget(dlg)

    dlg.title_edit.setText("Bad Trip")
    dlg.dest_edit.setText("Somewhere")
    dlg.accomm_edit.setText("Hotel ???")

    dlg.start_date_edit.setDate(QDate(2025, 5, 10))
    dlg.end_date_edit.setDate(QDate(2025, 5, 9))

    dlg.notes_edit.setPlainText("Should fail")

    dlg._handle_accept()

    assert dlg.result() != QDialog.DialogCode.Accepted
    assert dlg.get_data() is None


def test_packing_item_dialog(qtbot):
    dlg = PackingItemDialog()
    qtbot.addWidget(dlg)

    dlg.item_edit.setText("T-shirt")
    dlg.cat_edit.setText("Clothes")
    dlg.quantity_spin.setValue(3)
    dlg.place_combo.setCurrentText("Checked")
    dlg.packed_check.setChecked(True)

    dlg.accept()

    data = dlg.get_data()
    assert data["item_name"] == "T-shirt"
    assert data["category"] == "Clothes"
    assert data["quantity"] == 3
    assert data["place"] == "Checked"
    assert data["packed"] is True


def test_activity_item_dialog(qtbot):
    dlg = ActivityItemDialog()
    qtbot.addWidget(dlg)

    dlg.day_edit.setDate(QDate(2025, 11, 14))
    dlg.time_edit.setTime(QTime(12, 30))
    dlg.title_edit.setText("Sagrada Familia entry")
    dlg.location_edit.setText("Sagrada Familia")
    dlg.notes_edit.setPlainText("QR code in email")

    dlg._handle_accept()

    assert dlg.result() == QDialog.DialogCode.Accepted
    data = dlg.get_data()
    assert data is not None
    assert data["day"] == date(2025, 11, 14)
    assert data["time"] == "12:30"
    assert data["title"] == "Sagrada Familia entry"
    assert data["location"] == "Sagrada Familia"
    assert "QR code" in data["notes"]
