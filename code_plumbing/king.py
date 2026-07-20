# coding=utf-8
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout,
                             QSpinBox)
from code_plumbing import lib


class King:
    def __init__(
            self,
            name='Default King',
            sun_sign='Gemini',
            moon_sign='Taurus',
            rise_sign='Cancer',
            aristocracy=0,
            mercantilism=0,
            orthodoxy=0,
            piracy=0,
            rebellion=0,
            ergoism=0,
            monarchy = 0
    ):
        """Create a King model.

        Stores a king's identity (name and three astrological signs) and six
        integer trait values. Computes and stores the derived monarchy authority
        score immediately via `calc_monarchy()`.

        Args:
            name: The king's display name.
            sun_sign: Sun sign label.
            moon_sign: Moon sign label.
            rise_sign: Rising sign label.
            aristocracy: Integer authority component.
            mercantilism: Integer authority component.
            orthodoxy: Integer authority component.
            piracy: Integer authority component.
            rebellion: Integer authority component.
            ergoism: Integer authority component.
        """
        self.name = name
        self.sun_sign = sun_sign
        self.moon_sign = moon_sign
        self.rise_sign = rise_sign
        self.aristocracy = aristocracy
        self.mercantilism = mercantilism
        self.orthodoxy = orthodoxy
        self.piracy = piracy
        self.rebellion = rebellion
        self.ergoism = ergoism
        self.monarchy = monarchy


class SetKingDialog(QDialog):
    def __init__(self, parent=None, king=King()):
        """Create the king-edit dialog.

        Builds a Qt widget dialog as a popup window that lets the user view and update properties
        of a `King`, including name, sun/moon/rising signs, and trait scores
        (aristocracy, mercantilism, orthodoxy, piracy, rebellion, ergoism).
        Also shows the computed `king.monarchy` value.

        Args:
            parent: Optional Qt parent widget.
            king: Initial `King` instance whose values populate the dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("The Crown of Isha")

        self.king = king
        self.name_edit = QLineEdit()

        self.sun_combo = QComboBox()

        self.moon_combo = QComboBox()

        self.rising_combo = QComboBox()

        self.aristocracy_box = QSpinBox(minimum=0, maximum=24, value=self.king.aristocracy)
        self.mercantilism_box = QSpinBox(minimum=0, maximum=24, value=self.king.mercantilism)
        self.orthodoxy_box = QSpinBox(minimum=0, maximum=24, value=self.king.orthodoxy)
        self.piracy_box = QSpinBox(minimum=0, maximum=24, value=self.king.piracy)
        self.rebellion_box = QSpinBox(minimum=0, maximum=24, value=self.king.rebellion)
        self.ergoism_box = QSpinBox(minimum=0, maximum=24, value=self.king.ergoism)
        self.monarchy_box = QSpinBox(minimum=0, maximum=24, value=self.king.monarchy)
        for combo in (self.sun_combo, self.moon_combo, self.rising_combo):
            combo.addItems(lib.SIGNS)
        form = QVBoxLayout()
        rise_index = lib.SIGNS.index(self.king.rise_sign)
        self.rising_combo.setCurrentIndex(rise_index)

        sun_index = lib.SIGNS.index(self.king.sun_sign)
        self.sun_combo.setCurrentIndex(sun_index)
        self.name_edit.setText(self.king.name)
        moon_index = lib.SIGNS.index(self.king.moon_sign)
        self.moon_combo.setCurrentIndex(moon_index)
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
        auth.addWidget(self.monarchy_box)
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
        """Extract the edited king data from the dialog.

        Recomputes authorities for the internally stored `self.king`,
        then returns a new `King` instance populated from the current UI
        values.

        Returns:
            King: A new `King` object based on the dialog inputs.
        """
        return King(
            self.name_edit.text().strip(),
            self.sun_combo.currentText(),
            self.moon_combo.currentText(),
            self.rising_combo.currentText(),
            self.aristocracy_box.value(),
            self.mercantilism_box.value(),
            self.orthodoxy_box.value(),
            self.piracy_box.value(),
            self.rebellion_box.value(),
            self.ergoism_box.value(),
            self.monarchy_box.value()
        )

    def accept(self):
        """Handle the dialog 'accept' action.

        Calls the base class implementation to close the dialog and mark it as
        accepted. This function used to have further functionality that was depreciated with a rule change.
        """
        super().accept()
