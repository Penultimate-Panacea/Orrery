# coding=utf-8
import sys
import lib
import time
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QTextDocument
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsView, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QGroupBox, QRadioButton, QButtonGroup, QSizePolicy, QDialog, QTextEdit
)
from house import House
from planet import Planet
from ArcScene import ArcScene
from MoonPhaseWidget import MoonPhaseWidget
from necromancer import Necromancer
from hierophant import Hierophant
from mariner import Mariner
from warlock import Warlock
from faustian import Faustian
from sorcerer import Sorcerer
from sage import Sage
from wizard import Wizard

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Orrery \u260C")
        self.color_dicts = {
            "estate": lib.estate_color_dict,
            "season": lib.season_color_dict,
            "element": lib.element_color_dict,
        }

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
            Planet(lib.MERCURY, QColor("Blue"), span_steps=13, step_count_circle=48, current_step=0,  ring_radius=100, ring_thickness=16, conjunction_table=lib.CONJ_MERCURY),
            Planet(lib.VENUS, QColor("Green"), span_steps=9,  step_count_circle=48, current_step=1,  ring_radius=140, ring_thickness=16, conjunction_table=lib.CONJ_VENUS),
            Planet(lib.MARS, QColor("Red"), span_steps=5,  step_count_circle=48, current_step=2, ring_radius=180, ring_thickness=16, conjunction_table=lib.CONJ_MARS),
            Planet(lib.JUPITER, QColor("Orange"), span_steps=3,  step_count_circle=48, current_step=3, ring_radius=220, ring_thickness=16, conjunction_table=lib.CONJ_JUPITER),
            Planet(lib.SATURN, QColor("Gray"), span_steps=1,  step_count_circle=36, current_step=0,  ring_radius=280, ring_thickness=16,
                   grid_offset_half_step=True, conjunction_table=lib.CONJ_SATURN),
            Planet(lib.SOL, QColor("Yellow"), span_steps=1, step_count_circle=12, current_step=0, ring_radius=240,
                   ring_thickness=16, conjunction_table=lib.CONJ_SOL)
        ]
        self.house_color_mode = ["estate"] * 12

        self.wizards: List[Wizard] = [
            Necromancer(self.planet_conjunction_dict()),
            Hierophant(self.planet_conjunction_dict()),
            Mariner(self.planet_conjunction_dict()),
            Warlock(self.planet_conjunction_dict()),
            Faustian(self.planet_conjunction_dict()),
            Sorcerer(self.planet_conjunction_dict()),
            Sage(self.planet_conjunction_dict)
        ]

        self.scene = ArcScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)
        self.view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Left panel: swatches + per-house color radio
        left = QVBoxLayout()
        color_box = QGroupBox("House color (global per house)")
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

        # Move controls
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

        center.addWidget(self.view, 1)
        center.addWidget(move_box)

        # advance-all button
        adv_all = QPushButton("Advance all planets by span (CW) + active house +1")
        adv_all.setMinimumHeight(75)
        adv_all.clicked.connect(self.advance_all_spans)
        adv_all.clicked.connect(self.update_conjunction_table)

        center.addWidget(adv_all)

        # right: conjunction
        right = QVBoxLayout()
        right.addWidget(QLabel("Conjunctions (simplified)"))
        self.table = self.create_conjunction_table(self.generate_house_planet_conjunction_array())
        right.addWidget(self.table, 1)
        read_the_stars_box = QGroupBox("Read the stars")
        read_the_stars_layout = QGridLayout()
        read_the_stars_box.setLayout(read_the_stars_layout)
        # TODO
        # for w in wizards:
        # make button
        # connect button
        # relabel button
        # resize button
        btn_necromancer = QPushButton("Necromancer")
        read_the_stars_layout.addWidget(btn_necromancer)
        btn_necromancer.clicked.connect(self.wizards[0].make_magic_number)
        btn_hierophant = QPushButton("Hierophant")
        read_the_stars_layout.addWidget(btn_hierophant)
        btn_hierophant.clicked.connect(self.wizards[1].make_magic_number)
        btn_warlock = QPushButton("Warlock")
        read_the_stars_layout.addWidget(btn_warlock)
        # btn_warlock.clicked.connect(self.warlock)
        btn_mariner = QPushButton("Mariner")
        read_the_stars_layout.addWidget(btn_mariner)
        btn_faustian = QPushButton("Faustian")
        read_the_stars_layout.addWidget(btn_faustian)
        btn_faustian.clicked.connect(self.wizards[4].generate_faust_factor) # TODO incomplete, need to add house information
        btn_sorcerer = QPushButton("Sorcerer")
        read_the_stars_layout.addWidget(btn_sorcerer)
        btn_sorcerer.clicked.connect(self.wizards[5].make_magic_number)
        btn_sage = QPushButton("Sage")
        read_the_stars_layout.addWidget(btn_sage)

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
        DELIM = "\u260C"
        for r, (sign, planets) in enumerate(house_planet_conjunction_array):
            table.setItem(r, 0, QTableWidgetItem(sign))
            table.setItem(r, 1, QTableWidgetItem(lib.DELIM.join(planets)))

            for c in (0, 1):
                item = table.item(r, c)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        table.resizeColumnsToContents()
        return table

    def update_conjunction_table(self):
        table = self.table
        new_data = self.generate_house_planet_conjunction_array()
        table.setRowCount(len(new_data))
        table.clearContents()
        for r, (house, planets) in enumerate(new_data):
            table.setItem(r, 0, QTableWidgetItem(house))
            table.setItem(r, 1, QTableWidgetItem(lib.DELIM.join(planets)))
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

        for r, (label, qc) in enumerate(items):  # up to 4 entries
            swatch_widget = QWidget()
            swatch_layout = QHBoxLayout(swatch_widget)
            swatch_layout.setContentsMargins(0, 0, 0, 0)

            color_dot = QLabel()
            color_dot.setFixedSize(28, 16)
            color_dot.setStyleSheet(f"background-color: {qc}; border: 1px solid #666;")

            text_label = QLabel(str(label))

            swatch_layout.addWidget(color_dot)
            swatch_layout.addWidget(text_label)

            self.swatch_grid.addWidget(swatch_widget, r, 0)

    def planet_conjunction_dict(self):
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
        return {p: sorted(adj.get(p, set()), key=str) for p in planets_to_check}


