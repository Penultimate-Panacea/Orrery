# coding=utf-8
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QGridLayout, QSpinBox
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
        self.aristocracy = 0
        self.mercantilism = 0
        self.orthodoxy = 0
        self.piracy = 0
        self.rebellion = 0
        self.ergoism = 0
        self.monarchy = 24


class SetKingDialog(QDialog):
    def __init__(self, parent=None, king=King()):
        super().__init__(parent)
        self.setWindowTitle("The Crown of Isha")
        self.king = king
        self.name_edit = QLineEdit()
        self.sun_combo = QComboBox()
        self.moon_combo = QComboBox()
        self.rising_combo = QComboBox()
        self.aristocracy_box = QSpinBox(minimum=0, maximum=24, value=king.aristocracy)
        self.mercantilism_box = QSpinBox(minimum=0, maximum=24, value=king.mercantilism)
        self.orthodoxy_box = QSpinBox(minimum=0, maximum=24, value=king.orthodoxy)
        self.piracy_box = QSpinBox(minimum=0, maximum=24, value=king.piracy)
        self.rebellion_box = QSpinBox(minimum=0, maximum=24, value=king.rebellion)
        self.ergoism_box = QSpinBox(minimum=0, maximum=24, value=king.ergoism)
        self.monarchy = self.calc_monarchy()

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

        auth = QGridLayout()
        auth.addWidget(QLabel("Aristocracy"))
        auth.addWidget(self.aristocracy_box)
        auth.addWidget(QLabel("Mercantilism"))
        auth.addWidget(self.mercantilism_box)
        auth.addWidget(QLabel("Orthodoxy"))
        auth.addWidget(self.orthodoxy_box)
        auth.addWidget(QLabel("Piracy"))
        auth.addWidget(self.piracy_box)
        auth.addWidget(QLabel("Rebellion"))
        auth.addWidget(self.rebellion_box)
        auth.addWidget(QLabel("Ergoism"))
        auth.addWidget(self.ergoism_box)
        auth.addWidget(QLabel("Monarchy"))
        monarchy = self.monarchy
        auth.addWidget(QLabel(monarchy))
        form.addLayout(auth)
        buttons = QHBoxLayout()
        self.ok_btn = QPushButton("Update")
        self.cancel_btn = QPushButton("Cancel")
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)
        form.addLayout(buttons)


        self.setLayout(form)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_king_data(self) -> King:
        self.calc_monarchy()
        return King(self.name_edit.text().strip(),self.sun_combo.currentText(),self.moon_combo.currentText(),self.rising_combo.currentText(),self.aristocracy_box.value, self.mercantilism_box.value,self.orthodoxy_box.value,self.piracy_boxvalue,self.rebellion_box.value,self.ergoism_box.value,self.monarchy)

    def accept(self):
        data = self.get_king_data()
        if not data["name"]:
            self.name_edit.setFocus()
            return
        super().accept()

    def calc_monarchy(self):
        threats = (self.aristocracy_box.value + self.mercantilism_box.value + self.piracy_box.value + self.orthodoxy_box.value + self.rebellion_box.value + self.ergoism_box.value)
        return 24 - threats