# coding=utf-8
import pickle
from pathlib import Path
from code_plumbing import lib

from PyQt6.QtWidgets import (
    QWidget, QFileDialog, QMessageBox
)


class SaveLoadWidget(QWidget):
    def __init__(self, get_planets, set_planets_steps, get_kings, set_kings, get_dreaming, set_dreaming,
                 conjunction_update, parent=None):
        super().__init__(parent)
        self.get_planets = get_planets
        self.set_planets_steps = set_planets_steps
        self.get_kings = get_kings
        self.set_kings = set_kings
        self.get_dreaming = get_dreaming
        self.set_dreaming = set_dreaming
        self.update_conjunction_table = conjunction_update

    def save_to_file(self, planets, kings, dreaming):
        print("launching save to file")
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
            "version": 2,
            "current_steps": steps,
            "kings": kings,
            "dreaming": dreaming,
            "cycle": lib.current_cycle
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
            kings = data.get("kings", None)
            dreaming = data.get("dreaming", None)
            cycle = data.get("cycle", None)
            if not isinstance(steps, list):
                raise ValueError("Invalid file contents: current_steps must be a list")

            self.set_planets_steps(steps)
            self.set_kings(kings)
            self.set_dreaming(dreaming)
            self.update_conjunction_table()
            lib.current_cycle = cycle

        except Exception as e:
            QMessageBox.critical(self, "Load failed", str(e))
