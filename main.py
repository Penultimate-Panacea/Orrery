# coding=utf-8
import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
import qdarkstyle
from code_ui.MainWindow import MainWindow


def resource_path(relative_path: str) -> str:
    # PyInstaller --onefile extracts files to a temp dir at runtime.
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_font(relative_path: str) -> str:
    abs_path = resource_path(relative_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Font not found (bundled path mismatch): {abs_path}")

    fid = QFontDatabase.addApplicationFont(abs_path)
    fams = QFontDatabase.applicationFontFamilies(fid)
    if not fams:
        raise RuntimeError(f"Failed to load font: {abs_path}")
    return fams[0]


if __name__ == "__main__":
    app = QApplication(sys.argv)

    latin = "resources/fonts/NotoSans-VariableFont_wdth_wght.ttf"
    sym1 = "resources/fonts/NotoSansSymbols2-Regular.ttf"
    sym2 = "resources/fonts/NotoSansSymbols-VariableFont_wght.ttf"
    serif = "resources/fonts/NotoSerif-VariableFont_wdth_wght.ttf"

    latin_family = load_font(latin)
    sym1_family = load_font(sym1)
    sym2_family = load_font(sym2)
    serif_family = load_font(serif)

    font = QFont(latin_family, 12)
    font.setFamilies([latin_family, sym1_family, sym2_family, serif_family])

    app.setStyleSheet(qdarkstyle.load_stylesheet())

    w = MainWindow()
    w.resize(1600, 900)
    w.show()
    sys.exit(app.exec())
