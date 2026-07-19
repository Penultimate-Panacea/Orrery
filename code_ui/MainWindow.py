# coding=utf-8
from code_plumbing import lib
import time
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFontMetrics
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGraphicsView, QPushButton, QLabel, QTableWidget,
                             QTableWidgetItem, QGroupBox, QRadioButton, QButtonGroup, QSizePolicy, QComboBox
                             )
from code_plumbing.house import House
from code_plumbing.planet import Planet
from code_ui.ArcScene import ArcScene
from code_ui.MoonPhaseWidget import MoonPhaseWidget
from code_wizards.necromancer import Necromancer
from code_wizards.hierophant import Hierophant
from code_wizards.mariner import Mariner
from code_wizards.warlock import Warlock
from code_wizards.faustian import Faustian
# from code_wizards.sorcerer import Sorcerer
from code_wizards.sage import Sage
from code_wizards.wizard import Wizard
from code_plumbing.king import SetKingDialog, King
from code_ui.SaveLoad import SaveLoadWidget
from code_plumbing.PrinterOfTheStars import PrinterOfTheStars

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Orrery \u260C")
        self.color_dicts = {
            "estate": lib.estate_color_dict,
            "season": lib.season_color_dict,
            "element": lib.element_color_dict,
        }
        lib.current_cycle = 0

        self.houses: List[House] = [
            House("Aries", 0, lib.estate_color_dict['terrestrial'], lib.season_color_dict['spring'], lib.element_color_dict['fire']),
            House("Taurus", 1, lib.estate_color_dict['terrestrial'], lib.season_color_dict['spring'], lib.element_color_dict['earth']),
            House("Gemini", 2, lib.estate_color_dict['terrestrial'], lib.season_color_dict['spring'], lib.element_color_dict['air']),
            House("Cancer", 3, lib.estate_color_dict['terrestrial'], lib.season_color_dict['summer'], lib.element_color_dict['water']),
            House("Leo", 4, lib.estate_color_dict['spiritual'], lib.season_color_dict['summer'], lib.element_color_dict['fire']),
            House("Virgo", 5, lib.estate_color_dict['spiritual'], lib.season_color_dict['summer'], lib.element_color_dict['earth']),
            House("Libra ", 6, lib.estate_color_dict['spiritual'], lib.season_color_dict['autumn'], lib.element_color_dict['air']),
            House("Scorpio", 7, lib.estate_color_dict['spiritual'], lib.season_color_dict['autumn'], lib.element_color_dict['water']),
            House("Sagittarius", 8, lib.estate_color_dict['cosmic'], lib.season_color_dict['autumn'], lib.element_color_dict['fire']),
            House("Capricorn", 9, lib.estate_color_dict['cosmic'], lib.season_color_dict['winter'], lib.element_color_dict['earth']),
            House("Aquarius", 10, lib.estate_color_dict['cosmic'], lib.season_color_dict['winter'], lib.element_color_dict['air']),
            House("Pisces", 11, lib.estate_color_dict['cosmic'], lib.season_color_dict['winter'], lib.element_color_dict['water'])
        ]

        self.planets: List[Planet] = [
            Planet(lib.MERCURY, QColor("Blue"), span_steps=13, step_count_circle=48, current_step=0, ring_radius=100, ring_thickness=16, conjunction_table=lib.CONJ_MERCURY),
            Planet(lib.VENUS, QColor("Green"), span_steps=9, step_count_circle=48, current_step=1, ring_radius=140, ring_thickness=16, conjunction_table=lib.CONJ_VENUS),
            Planet(lib.MARS, QColor("Red"), span_steps=5, step_count_circle=48, current_step=2, ring_radius=180, ring_thickness=16, conjunction_table=lib.CONJ_MARS),
            Planet(lib.JUPITER, QColor("Orange"), span_steps=3, step_count_circle=48, current_step=3, ring_radius=220, ring_thickness=16, conjunction_table=lib.CONJ_JUPITER),
            Planet(lib.SATURN, QColor("Gray"), span_steps=1, step_count_circle=36, current_step=0, ring_radius=280, ring_thickness=16,
                   grid_offset_half_step=True, conjunction_table=lib.CONJ_SATURN),
            Planet(lib.SOL, QColor("Yellow"), span_steps=1, step_count_circle=12, current_step=0, ring_radius=240,
                   ring_thickness=16, conjunction_table=lib.CONJ_SOL)
        ]
        self.house_color_mode = ["estate"] * 12

        self.king = King() # placeholder king

        self.wizards: List[Wizard] = [
            Necromancer(self.planet_conjunction_dict()),
            Hierophant(self.planet_conjunction_dict()),
            Warlock(self.planet_conjunction_dict(),self.planets,self.king),
            Mariner(self.planet_conjunction_dict(), self.planets),
            Faustian(self.planet_conjunction_dict(), self.planets),
            # Sorcerer(self.planet_conjunction_dict()),
            Sage(self.planet_conjunction_dict, self.planets, "Calm")
        ]





        self.scene = ArcScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        self.view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dreaming_combo = QComboBox()
        self.save_load = SaveLoadWidget(get_planets=self.planets, get_kings=self.king,
                                        get_pendulum=self.dreaming_combo.currentText(),
                                        set_planets_steps=self.load_planet_steps,
                                        set_kings=self.load_king, set_pendulum=self.load_pendulum,
                                        conjunction_update=self.update_conjunction_table)
        self.printer = PrinterOfTheStars(self.wizards, self.planets)

        self.ppc_table = None

        # Left panel: swatches + per-house color radio
        left = QVBoxLayout()
        color_box = QGroupBox("Orrery Key")
        cb_layout = QGridLayout()
        color_box.setLayout(cb_layout)

        bg = QButtonGroup(self)
        bg.setExclusive(True)

        rb_est = QRadioButton("Estate")
        rb_sea = QRadioButton("Season")
        rb_ele = QRadioButton("Element")

        rb_est.setChecked(True)

        # when the global mode changes, apply it to all houses
        rb_est.toggled.connect(lambda checked: self.update_all_houses_mode("estate") if checked else None)
        rb_sea.toggled.connect(lambda checked: self.update_all_houses_mode("season") if checked else None)
        rb_ele.toggled.connect(lambda checked: self.update_all_houses_mode("element") if checked else None)

        bg.addButton(rb_est)
        bg.addButton(rb_sea)
        bg.addButton(rb_ele)

        cb_layout.addWidget(QLabel("Mode"), 0, 1)
        cb_layout.addWidget(rb_est, 0, 2)
        cb_layout.addWidget(rb_sea, 0, 3)
        cb_layout.addWidget(rb_ele, 0, 4)

        # connect radio toggles to both “update houses” and “update swatches”
        rb_est.toggled.connect(lambda checked: self.update_all_houses_mode("estate") if checked else None)
        rb_sea.toggled.connect(lambda checked: self.update_all_houses_mode("season") if checked else None)
        rb_ele.toggled.connect(lambda checked: self.update_all_houses_mode("element") if checked else None)

        rb_est.toggled.connect(lambda checked: self.rebuild_swatches_for_mode("estate") if checked else None)
        rb_sea.toggled.connect(lambda checked: self.rebuild_swatches_for_mode("season") if checked else None)
        rb_ele.toggled.connect(lambda checked: self.rebuild_swatches_for_mode("element") if checked else None)

        self.swatch_grid = QGridLayout()

        # initial swatches (Estate selected by default)
        self.rebuild_swatches_for_mode("estate")

        left.addWidget(color_box, 1)
        left.addLayout(self.swatch_grid, 1)

        # Game Phase Widget
        game_phase = MoonPhaseWidget(lib.moonphases, lib.html)
        left.addWidget(game_phase,8)

        # middle: graphics
        center = QVBoxLayout()

        # Move controls (left box)
        move_box = QGroupBox("Move arcs (snap)")
        move_layout = QGridLayout()
        move_box.setLayout(move_layout)

        for row, planet in enumerate(self.planets):
            move_layout.addWidget(QLabel(planet.name), row, 0)

            def bind(p: Planet, kind: str):
                def cb():
                    if kind == "span_cw":
                        p.current_step = (p.current_step + p.span_steps) % p.step_count_circle
                    elif kind == "span_ccw":
                        p.current_step = (p.current_step - p.span_steps) % p.step_count_circle
                    elif kind == "step_cw":
                        p.current_step = (p.current_step + 1) % p.step_count_circle
                    elif kind == "step_ccw":
                        p.current_step = (p.current_step - 1) % p.step_count_circle
                    self.redraw()

                return cb

            btn_span_ccw = QPushButton("span ↓")
            btn_span_cw = QPushButton("span ↑")
            btn_step_ccw = QPushButton("-1")
            btn_step_cw = QPushButton("+1")

            btn_span_ccw.clicked.connect(bind(planet, "span_ccw"))
            btn_span_cw.clicked.connect(bind(planet, "span_cw"))
            btn_step_ccw.clicked.connect(bind(planet, "step_ccw"))
            btn_step_cw.clicked.connect(bind(planet, "step_cw"))

            move_layout.addWidget(btn_span_ccw, row, 1)
            move_layout.addWidget(btn_span_cw, row, 2)
            move_layout.addWidget(btn_step_ccw, row, 3)
            move_layout.addWidget(btn_step_cw, row, 4)

        save_load_box = QGroupBox("Utilities")
        save_load_layout = QGridLayout()
        save_load_box.setLayout(save_load_layout)

        utility_button_height = 80

        btn_save = QPushButton("Save Data")
        btn_save.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_save.setMinimumHeight(utility_button_height)
        btn_save.clicked.connect(lambda checked=False: self.save_load.save_to_file(self.planets, self.king, self.dreaming_combo.currentText()))
        btn_load = QPushButton("Load Data")
        btn_load.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_load.setMinimumHeight(utility_button_height)
        btn_load.clicked.connect(self.save_load.load_from_file)
        btn_print = QPushButton("Print")
        btn_print.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_print.setMinimumHeight(utility_button_height)
        btn_print.clicked.connect(self.printer_logic)
        btn_cal = QPushButton("Calendar Controls")
        btn_cal.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_cal.setMinimumHeight(utility_button_height)
        save_load_layout.setColumnStretch(1, 1)
        save_load_layout.setColumnStretch(0, 1)
        save_load_layout.setRowStretch(0, 1)
        save_load_layout.setRowStretch(1, 1)
        save_load_layout.addWidget(btn_save, 0, 0)
        save_load_layout.addWidget(btn_load, 0, 1)
        save_load_layout.addWidget(btn_print, 1, 0)
        save_load_layout.addWidget(btn_cal, 1, 1)

        center.addWidget(self.view, 1)

        row_layout = QHBoxLayout()
        row_layout.addWidget(move_box)
        row_layout.addWidget(save_load_box)

        row_layout.setStretchFactor(move_box, 1)
        row_layout.setStretchFactor(save_load_box, 1)

        center.addLayout(row_layout)

        # advance-all button
        adv_all = QPushButton("Advance all planets by span (CW) + active house +1")
        adv_all.setMinimumHeight(75)
        adv_all.clicked.connect(self.advance_all_spans)
        adv_all.clicked.connect(self.update_conjunction_table)
        adv_all.clicked.connect(self.update_planet_planet_conjunction_array)

        center.addWidget(adv_all)

        # right: conjunction
        right = QVBoxLayout()
        #right.addWidget(QLabel("House Conjunctions"))
        self.conjunction_table = self.create_conjunction_table(self.generate_house_planet_conjunction_array())
        right.addWidget(QLabel("Planetary Conjunctions"))
        self.generate_planet_planet_conjunction_array()
        right.addWidget(self.ppc_table, 0)

        btn_row = QHBoxLayout()
        self.add_king_btn = QPushButton("𝔎𝔦𝔫𝔤 𝔞𝔫𝔡 ℭ𝔬𝔲𝔯𝔱")
        btn_row.addWidget(self.add_king_btn)
        right.addLayout(btn_row)
        self.add_king_btn.setMinimumHeight(100)
        self.add_king_btn.clicked.connect(self.on_add_king)
        self.add_king_btn.setStyleSheet("font-size: 32px;")

        read_the_stars_box = QGroupBox("Read the stars")
        read_the_stars_layout = QGridLayout()
        read_the_stars_box.setLayout(read_the_stars_layout)

        watcher_button_height = 50

        btn_necromancer = QPushButton("Gate-Watcher")
        read_the_stars_layout.addWidget(btn_necromancer)
        btn_necromancer.clicked.connect(self.wizards[0].popup)
        btn_necromancer.setMinimumHeight(watcher_button_height)

        btn_hierophant = QPushButton("Flame-Watcher")
        read_the_stars_layout.addWidget(btn_hierophant)
        btn_hierophant.clicked.connect(self.wizards[1].popup)
        btn_hierophant.setMinimumHeight(watcher_button_height)

        btn_warlock = QPushButton("Throne-Watcher")
        read_the_stars_layout.addWidget(btn_warlock)
        btn_warlock.clicked.connect(self.wizards[2].king_popup)
        btn_warlock.setMinimumHeight(watcher_button_height)

        btn_mariner = QPushButton("Keeper of the Wilds")
        read_the_stars_layout.addWidget(btn_mariner)
        btn_mariner.clicked.connect(self.wizards[3].popup)
        btn_mariner.setMinimumHeight(watcher_button_height)

        btn_faustian = QPushButton("Chain-Watcher")
        read_the_stars_layout.addWidget(btn_faustian)
        btn_faustian.clicked.connect(self.wizards[4].popup)
        btn_faustian.setMinimumHeight(watcher_button_height)

#       btn_sorcerer = QPushButton("Keeper of the Runes")
#       read_the_stars_layout.addWidget(btn_sorcerer)
#       btn_sorcerer.clicked.connect(self.wizards[5].sorcerer_popup)

        btn_sage = QPushButton("Star-Watcher")
        read_the_stars_layout.addWidget(btn_sage)
        btn_sage.clicked.connect(self.wizards[5].popup)
        btn_sage.setMinimumHeight(watcher_button_height)

        self.dreaming_combo = QComboBox()
        read_the_stars_layout.addWidget(self.dreaming_combo)
        self.dreaming_combo.addItem("Calm")
        self.dreaming_combo.addItem("Uncertain")
        self.dreaming_combo.addItem("Chaotic")
        self.dreaming_combo.addItem("Bleak")
        self.dreaming_combo.currentTextChanged.connect(self.wizards[5].set_dreaming)



        right.addWidget(read_the_stars_box, 1)

        top = QHBoxLayout()
        top.addLayout(left, 1)
        top.addLayout(center, 3)
        top.addLayout(right, 1)
        self.setLayout(top)

        self.redraw()

    def create_conjunction_table(self, house_planet_conjunction_array):
        table = QTableWidget(len(house_planet_conjunction_array), 2)
        table.setHorizontalHeaderLabels(["House", "Conjunctions"])
        for r, (sign, planets) in enumerate(house_planet_conjunction_array):
            table.setItem(r, 0, QTableWidgetItem(sign))
            table.setItem(r, 1, QTableWidgetItem(lib.CONJ_MARK.join(planets)))

            for c in (0, 1):
                item = table.item(r, c)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        table.resizeColumnsToContents()
        return table

    def update_conjunction_table(self):
        table = self.conjunction_table
        new_data = self.generate_house_planet_conjunction_array()
        table.setRowCount(len(new_data))
        table.clearContents()
        for r, (house, planets) in enumerate(new_data):
            table.setItem(r, 0, QTableWidgetItem(house))
            table.setItem(r, 1, QTableWidgetItem(lib.CONJ_MARK.join(planets)))
        table.resizeColumnsToContents()
        table.viewport().update()
        for w in self.wizards:
            w.update_conjunctions(self.planet_conjunction_dict())

    def set_house_mode(self, house_idx: int, mode: str):
        self.house_color_mode[house_idx] = mode
        self.redraw()

    def generate_house_planet_conjunction_array(self):
        conjunction_dict = {}
        for p in self.planets:
            conjunction_dict[p.name] = p.conjunction_table[p.current_step % p.step_count_circle]
            print("Current step of " + p.name + " is " + str(p.current_step % p.step_count_circle))
        print(str(conjunction_dict) + "\u260C")
        indices = sorted({i for planets in conjunction_dict.values() for i in planets})
        house_planet_conjunction_array = []
        for i in indices:
            planets_for_i = sorted([planet for planet, idxs in conjunction_dict.items() if i in idxs])
            if len(planets_for_i) > 1:
                house_planet_conjunction_array.append([self.houses[i].name, planets_for_i])
        print(house_planet_conjunction_array)
        return house_planet_conjunction_array
    def update_all_houses_mode(self, mode: str):
        for idx in range(len(self.houses)):
            self.set_house_mode(idx, mode)


    def advance_all_spans(self):
        lib.current_cycle += 1
        for p in self.planets:
            p.current_step = (p.current_step + p.span_steps) % p.step_count_circle
            print(p.name + " is at " + str(p.current_step))
        self.redraw()
        time.sleep(0.01)


    def redraw(self):
        self.scene.redraw(
            self.houses,
            self.planets,
            self.house_color_mode,
        )


    def printer_logic(self):
        for w in self.wizards:
            w.read_the_stars()
        self.printer.update_wizards(self.wizards)
        self.printer.update_planets(self.planets)
        self.printer.print_html()



    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def rebuild_swatches_for_mode(self, mode: str):
        while self.swatch_grid.count():
            item = self.swatch_grid.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        colors = self.color_dicts.get(mode, {})
        items = list(colors.items())  # [(label, QColor), ...]

        cols = 2  # 2x2 grid

        for i, (label, qc) in enumerate(items):
            r = i // cols
            c = i % cols

            swatch_widget = QWidget()
            swatch_layout = QHBoxLayout(swatch_widget)
            swatch_layout.setContentsMargins(0, 0, 0, 0)

            color_dot = QLabel()
            color_dot.setFixedSize(28, 16)
            color_dot.setStyleSheet(f"background-color: {qc}; border: 1px solid #666;")

            text_label = QLabel(str(label))

            swatch_layout.addWidget(color_dot)
            swatch_layout.addWidget(text_label)

            self.swatch_grid.addWidget(swatch_widget, r, c)

        self.swatch_grid.setRowStretch(0, 1)
        self.swatch_grid.setRowStretch(1, 1)
        self.swatch_grid.setColumnStretch(0, 1)
        self.swatch_grid.setColumnStretch(1, 1)

    def planet_conjunction_dict(self) -> dict:
        planets_to_check = []
        for i in self.planets:
            planets_to_check.append(i.name)
        data = self.generate_house_planet_conjunction_array()
        # planets_to_check: list of planet names you want in the output (including ones with no conjunction)
        adj = {p: set() for p in planets_to_check}

        for _, planets in data:
            planets = list(dict.fromkeys(planets))  # dedupe, keep order
            for p in planets:
                if p not in adj:
                    adj[p] = set()  # only if it appears in data but not in planets_to_check

            for i, p in enumerate(planets):
                for j, q in enumerate(planets):
                    if i != j:
                        adj[p].add(q)

        # return in the same order as planets_to_check
        pcd = {p: sorted(adj.get(p, set()), key=str) for p in planets_to_check}
        return pcd

    def on_add_king(self):
        dlg = SetKingDialog(self,self.king)
        if dlg.exec() == dlg.DialogCode.Accepted:
            self.king=dlg.get_king_data()
            self.wizards[2].update_king(self.king)

    def load_planet_steps(self, steps_list):
        print("loading planet steps")
        for i, planet in enumerate(self.planets):
            if i >= len(steps_list):
                break
            planet.current_step = steps_list[i]
        for w in self.wizards:
            w.update_conjunctions(self.planets)
        self.redraw()

    def load_king(self, king):
        self.king = king

    def load_pendulum(self, pendulum):
        print("loading pendulum")
        self.dreaming_combo.setCurrentIndex(self.dreaming_combo.findText(pendulum))
        self.redraw()

    def generate_planet_planet_conjunction_array(self):
        pcd = self.planet_conjunction_dict()
        pcd_keys = list(pcd)
        key_count = len(pcd_keys) # should always be six but just in case

        table = QTableWidget(key_count, key_count)
        table.setHorizontalHeaderLabels(pcd_keys)
        table.setVerticalHeaderLabels(pcd_keys)

        symbol_true = lib.CONJ_MARK
        symbol_false = ""

        d = self.planet_conjunction_dict()
        sd = {k: set(d[k]) for k in pcd_keys}

        for i, k1 in enumerate(pcd_keys):
            for j, k2 in enumerate(pcd_keys):
                shared = bool(sd[k1] & sd[k2])
                item = QTableWidgetItem(symbol_true if shared else symbol_false)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)

        fm = QFontMetrics(table.font())

        two_char_width = fm.horizontalAdvance("0") * 2
        row_height = fm.height() * 1  # “1 lines” tall approximation

        table.verticalHeader().setDefaultSectionSize(row_height)

        for r in range(table.rowCount()):
            table.setRowHeight(r, row_height)

        for c in range(table.columnCount()):
            table.setColumnWidth(c, two_char_width)

        self.ppc_table = table

    from PyQt6.QtWidgets import QTableWidgetItem
    from PyQt6.QtCore import Qt

    def update_planet_planet_conjunction_array(self):
        pcd = self.planet_conjunction_dict()
        pcd_keys = list(pcd)
        symbol_true = lib.CONJ_MARK
        symbol_false = ""

        d = self.planet_conjunction_dict()
        sd = {k: set(d[k]) for k in pcd_keys}

        for i, k1 in enumerate(pcd_keys):
            s1 = sd[k1]
            for j, k2 in enumerate(pcd_keys):
                shared = bool(s1 & sd[k2])

                item = self.ppc_table.item(i, j)
                if item is None:
                    item = QTableWidgetItem()
                    self.ppc_table.setItem(i, j, item)

                item.setText(symbol_true if shared else symbol_false)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
