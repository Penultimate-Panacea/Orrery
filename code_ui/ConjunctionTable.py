# coding=utf-8
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFontMetrics

from code_plumbing import lib


class ConjunctionTable:
    def __init__(self, planets, planet_conjunction_dict):
        self.planets = planets
        self.pcd = planet_conjunction_dict
        self.table = QTableWidget()
        self.rebuild_table()

    def update(self, new_planets, new_pcd):
        self.pcd = new_pcd
        self.planets = new_planets
        self.rebuild_table()

    def rebuild_table(self):
        # Keys define the size + headers
        pcd_keys = list(self.pcd)
        key_count = len(pcd_keys)

        n = len(self.planets)

        # Resize the existing table
        self.table.clearContents()  # clear old items (keeps the widget)
        self.table.setRowCount(key_count)
        self.table.setColumnCount(key_count)

        self.table.setHorizontalHeaderLabels(pcd_keys)
        self.table.setVerticalHeaderLabels(pcd_keys)

        symbol_true = lib.CONJ_MARK
        symbol_false = ""

        fm = QFontMetrics(self.table.font())
        two_char_width = fm.horizontalAdvance("0") * 2
        row_height = fm.height()
        self.table.verticalHeader().setDefaultSectionSize(row_height)

        current_sets = [
            planet.conjunction_table[planet.current_step]
            for planet in self.planets
        ]

        bool_array = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                bool_array[i][j] = len(current_sets[i].intersection(current_sets[j])) > 0

        for r, row in enumerate(bool_array):
            for c, value in enumerate(row):
                item_text = symbol_true if value else symbol_false
                self.table.setItem(r, c, QTableWidgetItem(item_text))

        for r in range(self.table.rowCount()):
            self.table.setRowHeight(r, row_height)

        for c in range(self.table.columnCount()):
            self.table.setColumnWidth(c, two_char_width)
