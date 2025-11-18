from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import pyqtSignal

from ..models import AppState
from ..style import available_themes


class SettingsPage(QWidget):
    themeChanged = pyqtSignal(str)
    requestSave = pyqtSignal()

    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_lbl = QLabel("Settings")
        header_lbl.setProperty("role", "headerPrimary")
        layout.addWidget(header_lbl)

        subtitle_lbl = QLabel("Customize how the app looks and behaves.")
        subtitle_lbl.setProperty("role", "headerSecondary")
        subtitle_lbl.setWordWrap(True)
        layout.addWidget(subtitle_lbl)

        theme_lbl = QLabel("Theme:")
        theme_lbl.setProperty("role", "headerSecondary")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(available_themes())
        idx = self.theme_combo.findText(self.state.theme)
        if idx != -1:
            self.theme_combo.setCurrentIndex(idx)

        theme_row = QHBoxLayout()
        theme_row.addWidget(theme_lbl)
        theme_row.addWidget(self.theme_combo)
        theme_row.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addLayout(theme_row)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.apply_theme_btn = QPushButton("Apply Theme")
        self.apply_theme_btn.setProperty("role", "primary")
        self.apply_theme_btn.clicked.connect(self._emit_theme_change)
        btn_row.addWidget(self.apply_theme_btn)

        self.save_btn = QPushButton("Save All")
        self.save_btn.setProperty("role", "ghost")
        self.save_btn.clicked.connect(self.requestSave.emit)
        btn_row.addWidget(self.save_btn)

        layout.addLayout(btn_row)

        layout.addStretch(1)

    def _emit_theme_change(self):
        chosen = self.theme_combo.currentText()
        self.state.theme = chosen
        self.themeChanged.emit(chosen)
