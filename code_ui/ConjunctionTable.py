# coding=utf-8
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFontMetrics

from code_plumbing import lib


class ConjunctionTable:
    def __init__(self, planets, planet_conjunction_dict):
        self.planets = planets
        self.pcd = planet_conjunction_dict
        self.table = self.make_table()

    def update(self, new_planets, new_pcd):
        self.pcd = new_pcd
        self.planets = new_planets
        self.table = self.make_table()

    def make_table(self):
        pcd_keys = list(self.pcd)
        key_count = len(pcd_keys)

        table = QTableWidget(key_count, key_count)
        table.setHorizontalHeaderLabels(pcd_keys)
        table.setVerticalHeaderLabels(pcd_keys)

        symbol_true = lib.CONJ_MARK
        symbol_false = ""

        fm = QFontMetrics(table.font())
        two_char_width = fm.horizontalAdvance("0") * 2
        row_height = fm.height()

        table.verticalHeader().setDefaultSectionSize(row_height)

        n = len(self.planets)

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
                if value:
                    table.setItem(r, c, QTableWidgetItem(symbol_true))
                else:
                    table.setItem(r, c, QTableWidgetItem(symbol_false))

        for r in range(table.rowCount()):
            table.setRowHeight(r, row_height)

        for c in range(table.columnCount()):
            table.setColumnWidth(c, two_char_width)

        return table