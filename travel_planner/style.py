DARK_STYLE = """
QWidget {
    background-color: #1e1f22;
    color: #f5f6f8;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QFrame#Sidebar {
    background-color: #2b2d31;
    border-right: 1px solid #3a3d42;
}

QLabel[role="title"] {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
}

QLabel[role="headerPrimary"] {
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
}

QLabel[role="headerSecondary"] {
    color: #b5b8bf;
    font-size: 13px;
}

QFrame#HeaderBar {
    background-color: #2b2d31;
    border-bottom: 1px solid #3a3d42;
}

QPushButton {
    border: none;
    background-color: transparent;
    color: #f5f6f8;
}

QPushButton[role="nav"] {
    text-align: left;
    background-color: transparent;
    color: #b5b8bf;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}
QPushButton[role="nav"]:hover {
    background-color: #3a3d42;
    color: #ffffff;
}
QPushButton[role="nav"][active="true"] {
    background-color: #3a3d42;
    color: #ffffff;
}

QPushButton[role="primary"] {
    background-color: #FF8A3D;
    color: #ffffff;
    padding: 10px 12px;
    border-radius: 8px;
    font-weight: 600;
}
QPushButton[role="primary"]:hover {
    background-color: #ff9a5a;
}

QPushButton[role="ghost"] {
    background-color: #3a3d42;
    color: #ffffff;
    padding: 6px 10px;
    border-radius: 6px;
    font-weight: 500;
}
QPushButton[role="ghost"]:hover {
    background-color: #4a4e56;
}

QLineEdit,
QTextEdit,
QDateEdit,
QTimeEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 6px;
    padding: 6px 8px;
    color: #f5f6f8;
    selection-background-color: #FF8A3D;
}

QTextEdit {
    min-height: 60px;
}

QTableWidget {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 12px;
    gridline-color: #3a3d42;
    color: #f5f6f8;
    selection-background-color: #4a4e56;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #2b2d31;
    color: #b5b8bf;
    font-weight: 500;
    padding: 6px 8px;
    border: none;
    border-bottom: 1px solid #3a3d42;
}

QScrollArea {
    background-color: transparent;
    border: none;
}

QFrame#Card {
    background-color: #2b2d31;
    border: 1px solid #3a3d42;
    border-radius: 12px;
}

QFrame#CardActive {
    background-color: #2f3035;
    border: 1px solid #FF8A3D;
    border-radius: 12px;
}

QLabel[role="cardTitle"] {
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
}

QLabel[role="cardSubtitle"] {
    color: #b5b8bf;
    font-size: 13px;
}
"""

LIGHT_STYLE = """
QWidget {
    background-color: #f5f5f7;
    color: #1e1f22;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QFrame#Sidebar {
    background-color: #ffffff;
    border-right: 1px solid #d8d9de;
}

QLabel[role="title"] {
    color: #1e1f22;
    font-size: 18px;
    font-weight: 600;
}

QLabel[role="headerPrimary"] {
    color: #1e1f22;
    font-size: 16px;
    font-weight: 600;
}

QLabel[role="headerSecondary"] {
    color: #5a5d6a;
    font-size: 13px;
}

QFrame#HeaderBar {
    background-color: #ffffff;
    border-bottom: 1px solid #d8d9de;
}

QPushButton {
    border: none;
    background-color: transparent;
    color: #1e1f22;
}

QPushButton[role="nav"] {
    text-align: left;
    background-color: transparent;
    color: #5a5d6a;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}
QPushButton[role="nav"]:hover {
    background-color: #e7e8ec;
    color: #1e1f22;
}
QPushButton[role="nav"][active="true"] {
    background-color: #e7e8ec;
    color: #1e1f22;
}

QPushButton[role="primary"] {
    background-color: #FF8A3D;
    color: #ffffff;
    padding: 10px 12px;
    border-radius: 8px;
    font-weight: 600;
}
QPushButton[role="primary"]:hover {
    background-color: #ff9a5a;
}

QPushButton[role="ghost"] {
    background-color: #e7e8ec;
    color: #1e1f22;
    padding: 6px 10px;
    border-radius: 6px;
    font-weight: 500;
}
QPushButton[role="ghost"]:hover {
    background-color: #d8d9de;
}

QLineEdit,
QTextEdit,
QDateEdit,
QTimeEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #d8d9de;
    border-radius: 6px;
    padding: 6px 8px;
    color: #1e1f22;
    selection-background-color: #FF8A3D;
}

QTextEdit {
    min-height: 60px;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d8d9de;
    border-radius: 12px;
    gridline-color: #d8d9de;
    color: #1e1f22;
    selection-background-color: #e7e8ec;
    selection-color: #1e1f22;
}

QHeaderView::section {
    background-color: #ffffff;
    color: #5a5d6a;
    font-weight: 500;
    padding: 6px 8px;
    border: none;
    border-bottom: 1px solid #d8d9de;
}

QScrollArea {
    background-color: transparent;
    border: none;
}

QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #d8d9de;
    border-radius: 12px;
}

QFrame#CardActive {
    background-color: #fff8f2;
    border: 1px solid #FF8A3D;
    border-radius: 12px;
}

QLabel[role="cardTitle"] {
    color: #1e1f22;
    font-size: 16px;
    font-weight: 600;
}

QLabel[role="cardSubtitle"] {
    color: #5a5d6a;
    font-size: 13px;
}
"""


def apply_theme(qapp, theme: str) -> None:
    if theme.lower() == "light":
        qapp.setStyleSheet(LIGHT_STYLE)
    else:
        qapp.setStyleSheet(DARK_STYLE)


def available_themes() -> list[str]:
    return ["dark", "light"]
