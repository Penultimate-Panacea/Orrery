# coding=utf-8
import pickle
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
)


class SaveLoadWidget(QWidget):
    def __init__(self, get_planets, set_planets_steps, parent=None):
        super().__init__(parent)
        self.get_planets = get_planets
        self.set_planets_steps = set_planets_steps

        self.btn_save = QPushButton("Save")
        self.btn_load = QPushButton("Load")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_load)
        layout.addStretch(1)
        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_to_file)
        self.btn_load.clicked.connect(self.load_from_file)

    def save_to_file(self):
        planets = list(self.get_planets())
        steps = [p.current_step for p in planets]

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Orrery",
            "",
            "Orrery Files (*.orrery)"
        )
        if not file_path:
            return

        if not file_path.lower().endswith(".orrery"):
            file_path += ".orrery"

        data = {
            "version": 1,
            "current_steps": steps
        }

        try:
            Path(file_path).write_bytes(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
        except OSError as e:
            QMessageBox.critical(self, "Save failed", str(e))

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Orrery",
            "",
            "Orrery Files (*.orrery)"
        )
        if not file_path:
            return

        try:
            raw = Path(file_path).read_bytes()
            data = pickle.loads(raw)

            steps = data.get("current_steps", None)
            if not isinstance(steps, list):
                raise ValueError("Invalid file contents: current_steps must be a list")

            self.set_planets_steps(steps)

        except Exception as e:
            QMessageBox.critical(self, "Load failed", str(e))
