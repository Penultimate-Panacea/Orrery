# coding=utf-8
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
import qdarkstyle
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    latin = "./resources/fonts/NotoSans-VariableFont_wdth,wght.ttf"
    sym1 = "./resources/fonts/NotoSansSymbols2-Regular.ttf"
    sym2 = "./resources/fonts/NotoSansSymbols-VariableFont_wght.ttf"  #


    def load_font(path):
        fid = QFontDatabase.addApplicationFont(path)
        fams = QFontDatabase.applicationFontFamilies(fid)
        if not fams:
            raise RuntimeError(f"Failed to load {path}")
        return fams[0]


    latin_family = load_font(latin)
    sym1_family = load_font(sym1)
    sym2_family = load_font(sym2)
    font = QFont(latin_family, 12)
    font.setFamilies([latin_family, sym1_family, sym2_family])
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    w = MainWindow()
    w.resize(1600, 900)
    w.show()
    sys.exit(app.exec())
