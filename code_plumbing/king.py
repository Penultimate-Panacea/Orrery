# coding=utf-8
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton
)
from dataclasses import dataclass

SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
    "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

@dataclass
class King:
    def __init__(self):
        self.sun_sign = 4
        self.moon_sign = 3
        self.rise_sign = 10

class AddKingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add King")

        self.name_edit = QLineEdit()
        self.sun_combo = QComboBox()
        self.moon_combo = QComboBox()
        self.rising_combo = QComboBox()

        for combo in (self.sun_combo, self.moon_combo, self.rising_combo):
            combo.addItems(SIGNS)

        form = QVBoxLayout()
        form.addWidget(QLabel("King's name:"))
        form.addWidget(self.name_edit)

        form.addWidget(QLabel("Sun sign:"))
        form.addWidget(self.sun_combo)

        form.addWidget(QLabel("Moon sign:"))
        form.addWidget(self.moon_combo)

        form.addWidget(QLabel("Rising sign:"))
        form.addWidget(self.rising_combo)

        buttons = QHBoxLayout()
        self.ok_btn = QPushButton("Add")
        self.cancel_btn = QPushButton("Cancel")
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)
        form.addLayout(buttons)

        self.setLayout(form)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_king_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "sun": self.sun_combo.currentText(),
            "moon": self.moon_combo.currentText(),
            "rising": self.rising_combo.currentText(),
        }

    def accept(self):
        data = self.get_king_data()
        if not data["name"]:
            self.name_edit.setFocus()
            return
        super().accept()