# coding=utf-8
# qt_arcs_planets_houses_v3.py
import sys
import math
import lib
import time
import os
from dataclasses import dataclass
from typing import List, Tuple, Set
sys.path.insert(1, './BreezeStyleSheets-main/resources')
import qdarkstyle

from PyQt6.QtCore import Qt, QRectF, QPointF, QFile, QTextStream, QIODevice
from PyQt6.QtGui import QPen, QColor, QPainterPath, QBrush, QFont, QTextDocument, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsView, QGraphicsScene, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QGroupBox, QRadioButton, QButtonGroup, QSizePolicy, QDialog, QTextEdit, QTextBrowser
)
from PyQt6.QtSvgWidgets import QSvgWidget


# -----------------------------
# Houses (12 equal regions)
# -----------------------------
@dataclass
class House:
    name: str
    index: int                 # 0..11
    estate_color: str
    season_color: str
    element_color: str

    @property
    def start_deg(self) -> float:  # 0 at 12 o'clock, increasing clockwise
        return self.index * 30.0

    @property
    def end_deg(self) -> float:
        return (self.index + 1) * 30.0

    def contains_angle(self, deg: float) -> bool:
        d = deg % 360.0
        start = self.start_deg % 360.0
        end = self.end_deg % 360.0
        if self.index == 11:
            return d >= start or d < end
        return (d >= start) and (d < end)


    def color_for(self, mode: str) -> str:
        if mode == "estate":
            return self.estate_color
        if mode == "season":
            return self.season_color
        return self.element_color


# -----------------------------
# Planets (arcs)
# -----------------------------
@dataclass
class Planet:
    name: str
    arc_color: str
    span_steps: int
    step_count_circle: int
    conjunction_table: list
    current_step: int = 0
    ring_radius: float = 140.0
    ring_thickness: float = 14.0
    grid_offset_half_step: bool = False  # used for 36-step half-step offset


    @property
    def step_deg(self) -> float:
        return 360.0 / self.step_count_circle

    def start_deg(self) -> float:
        # 0 at 12 o'clock clockwise
        base = (self.current_step % self.step_count_circle)
        if self.grid_offset_half_step:
            base = base + 0.5
        return (base % self.step_count_circle) * self.step_deg

    def angle_for_step(self, step_offset: int) -> float:
        base = (self.current_step + step_offset) % self.step_count_circle
        if self.grid_offset_half_step:
            base = base + 0.5
        return (base % self.step_count_circle) * self.step_deg


# -----------------------------
# Drawing scene
# -----------------------------
class ArcScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(QRectF(-320, -280, 640, 560))
        self.planets_items: List[object] = []
        self.house_fill_items: List[object] = []
        self.houses_line_items: List[object] = []
        self.houses_label_items: List[object] = []
        self.planet_label_items: List[object] = []

    @staticmethod
    def polar_point_scene(r: float, qt_deg: float) -> QPointF:
        rad = math.radians(qt_deg)  # Qt: 0 at +x, CCW+
        x = r * math.cos(rad)
        y = -r * math.sin(rad)     # scene y grows downward
        return QPointF(x, y)

    def clear_all(self):
        for it in self.planets_items:
            self.removeItem(it)
        self.planets_items.clear()

        for it in self.planet_label_items:
            self.removeItem(it)
        self.planet_label_items.clear()

        for it in self.house_fill_items:
            self.removeItem(it)
        self.house_fill_items.clear()

        for it in self.houses_line_items:
            self.removeItem(it)
        self.houses_line_items.clear()

        for it in self.houses_label_items:
            self.removeItem(it)
        self.houses_label_items.clear()

    def draw_house_fills_and_labels(self, houses: List[House], house_color_mode: List[str]):

        # ring outer for determining house wedge size
        max_r = 235

        # center dot
        pen_dot = QPen(QColor("#111111"))
        self.addEllipse(-4, -4, 8, 8, pen_dot, QColor("#111111"))

        for i in range(12):
            house = houses[i]
            mode = house_color_mode[i]
            col = QColor(house.color_for(mode))
            fill = QColor(col)
            fill.setAlpha(55)  # transparent

            # house wedge: our angles are 0 at 12 o'clock, clockwise
            # convert our -> qt:
            # our=0 at 12 clockwise => qt=90 at CCW
            # qt = 90 - our
            our_start = i * 30.0
            our_end = (i + 1) * 30.0

            qt_start = 90.0 - (our_start % 360.0)
            qt_end = 90.0 - (our_end % 360.0)

            # Build wedge path as a filled sector from start->end clockwise in our space.
            # Convert to qt sweep: clockwise in our => negative CCW in qt.
            qt_span = -(30.0)

            rect = QRectF(-max_r, -max_r, 2 * max_r, 2 * max_r)

            path = QPainterPath()
            center = QPointF(0, 0)
            path.moveTo(center)

            # arcTo draws along qt_span
            # move from center to arc start point implicitly:
            start_pt = self.polar_point_scene(max_r, qt_start)
            path.moveTo(start_pt)
            path.arcTo(rect, qt_start, qt_span)

            path.lineTo(center)
            path.closeSubpath()

            self.house_fill_items.append(self.addPath(path, QPen(Qt.PenStyle.NoPen), QBrush(fill)))

            # separator line
            sep_pen = QPen(QColor("#2a2a2a"))
            sep_pen.setWidth(1)
            end_pt = self.polar_point_scene(max_r, qt_start)
            self.houses_line_items.append(self.addLine(0, 0, end_pt.x(), end_pt.y(), sep_pen))

            # label
            mid_our = i * 30.0 + 15.0
            qt_mid = 90.0 - (mid_our % 360.0)
            label_pos = self.polar_point_scene(max_r - 35, qt_mid)

            label = self.addText(house.name)
            label_color = QColor(col)
            label_color.setAlpha(220)
            label.setDefaultTextColor(label_color)

            f = QFont()
            f.setPointSize(12)
            label.setFont(f)

            br = label.boundingRect()
            label.setPos(label_pos.x() - br.width() / 2, label_pos.y() - br.height() / 2)
            self.houses_label_items.append(label)

    def draw_arc(self, planet: Planet):
        r_outer = planet.ring_radius
        t = planet.ring_thickness
        r_inner = max(0.0, r_outer - t)

        start_our = planet.start_deg() % 360.0
        qt_start = 90.0 - start_our
        span_deg = planet.span_steps * planet.step_deg
        qt_span = -span_deg  # clockwise sweep

        rect_outer = QRectF(-r_outer, -r_outer, 2 * r_outer, 2 * r_outer)
        rect_inner = QRectF(-r_inner, -r_inner, 2 * r_inner, 2 * r_inner)

        outer_start_pt = self.polar_point_scene(r_outer, qt_start)
        inner_end_pt = self.polar_point_scene(r_inner, qt_start + qt_span)

        path = QPainterPath()
        path.moveTo(outer_start_pt)

        # Outer boundary
        path.arcTo(rect_outer, qt_start, qt_span)

        # End radial edge to inner boundary
        path.lineTo(inner_end_pt)

        # Inner boundary back to start
        path.arcTo(rect_inner, qt_start + qt_span, -qt_span)

        path.closeSubpath()

        pen = QPen(QColor(planet.arc_color))
        pen.setWidth(1)
        brush = QBrush(QColor(planet.arc_color))

        item = self.addPath(path, pen, brush)
        self.planets_items.append(item)

        # planet label near arc midpoint
        mid_step_offset = planet.span_steps / 2.0
        mid_our = planet.angle_for_step(mid_step_offset)
        qt_mid = 90.0 - (mid_our % 360.0)
        label_pos = self.polar_point_scene(r_outer - t * 0.4, qt_mid)

        text = self.addText(planet.name)
        if planet.grid_offset_half_step: # Saturn will be black in background so the color must be white
            text.setDefaultTextColor(QColor("White"))
        else: text.setDefaultTextColor(QColor("Black"))
        f = QFont()
        f.setPointSize(14)
        text.setFont(f)

        br = text.boundingRect()
        text.setPos(label_pos.x() - br.width() / 2, label_pos.y() - br.height() / 2)
        self.planet_label_items.append(text)

    def redraw(self, houses, planets, house_color_mode):
        self.clear_all()
        self.draw_house_fills_and_labels(houses, house_color_mode)
        for p in planets:
            self.draw_arc(p)


# -----------------------------
# Moon Phase Widget
# -----------------------------

class GamePhaseWidget(QWidget):
    """
    Displays the current SVG from a list, a Next button, and an HTML info area.
    """
    def __init__(self, svg_paths: list[str], html_snippets: list[str] | None = None, parent=None):
        super().__init__(parent)

        self.svg_paths = svg_paths or []
        self.html_snippets = html_snippets or [""] * len(self.svg_paths)
        if len(self.html_snippets) < len(self.svg_paths):
            self.html_snippets += [""] * (len(self.svg_paths) - len(self.html_snippets))

        self.index = 0

        # --- UI ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.svg_title = QLabel("SVG Viewer")
        self.svg_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_svg)

        top_row.addWidget(self.svg_title, 1)
        top_row.addWidget(self.next_btn, 0)

        self.svg_widget = QSvgWidget()
        self.svg_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.svg_widget.setMinimumHeight(300)

        self.info_browser = QTextBrowser()
        self.info_browser.setOpenExternalLinks(True)

        main_layout.addLayout(top_row)
        main_layout.addWidget(self.svg_widget, 1)
        main_layout.addWidget(self.info_browser, 0)

        if not self.svg_paths:
            self.info_browser.setHtml("<b>No SVGs provided.</b>")
            self.next_btn.setEnabled(False)
        else:
            self.update_view()

    def current_svg_path(self) -> str | None:
        if 0 <= self.index < len(self.svg_paths):
            return self.svg_paths[self.index]
        return None

    def update_view(self):
        path = self.current_svg_path()
        if not path or not os.path.exists(path):
            self.svg_widget.load(b"")
            self.info_browser.setHtml("<b>Missing SVG file.</b>")
            return

        self.svg_title.setText(f"SVG Viewer ({self.index + 1}/{len(self.svg_paths)})")
        self.svg_widget.load(path)

        html = self.html_snippets[self.index] if self.index < len(self.html_snippets) else ""
        self.info_browser.setHtml(html)

    def next_svg(self):
        if not self.svg_paths:
            return
        self.index = (self.index + 1) % len(self.svg_paths)
        self.update_view()

    # Optional: expose a way to go back / set index
    def set_index(self, idx: int):
        if not self.svg_paths:
            return
        self.index = idx % len(self.svg_paths)
        self.update_view()

# -----------------------------
# Main widget
# -----------------------------
class MainWidget(QWidget):
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

        # spans per your request
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

        moonphases = ["new_moon.svg","visions.svg","planning.svg","story.svg","meeting.svg","quiet.svg"]
        html = ["new_moon.html","visions.html","planning.html","story.html","meeting.html","quiet.html"]
        game_phase = GamePhaseWidget(moonphases,html)
        left.addWidget(game_phase,1)

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
        btn_necromancer = QPushButton("Necromancer")
        read_the_stars_layout.addWidget(btn_necromancer)
        btn_necromancer.clicked.connect(self.necromancer)
        btn_hierophant = QPushButton("Hierophant")
        read_the_stars_layout.addWidget(btn_hierophant)
        btn_hierophant.clicked.connect(self.hierophant)
        btn_warlock = QPushButton("Warlock")
        read_the_stars_layout.addWidget(btn_warlock)
        # btn_warlock.clicked.connect(self.warlock)
        btn_mariner = QPushButton("Mariner")
        read_the_stars_layout.addWidget(btn_mariner)
        btn_faustian = QPushButton("Faustian")
        read_the_stars_layout.addWidget(btn_faustian)
        btn_faustian.clicked.connect(self.faustian) # TODO incomplete, need to add house information
        btn_sorcerer = QPushButton("Sorcerer")
        read_the_stars_layout.addWidget(btn_sorcerer)
        btn_sorcerer.clicked.connect(self.sorcerer)
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

    def necromancer(self):
        conjunctions = self.planet_conjunction_dict()
        print("Conjunctions are: " + str(conjunctions))
        saturn_conjunctions = conjunctions[lib.SATURN]
        necromancer_magic_number =0b0000000
        if len(saturn_conjunctions) == 0:
            print ("Saturn Stands Alone")
            necromancer_magic_number ^= ( 1 << 0)
        if lib.MERCURY in saturn_conjunctions:
            print ("Mercury in Conjunction")
            necromancer_magic_number ^= (1 << 1)
        if lib.VENUS in saturn_conjunctions:
            print ("Venus in Conjunction")
            necromancer_magic_number ^= (1 << 2)
        if lib.MARS in saturn_conjunctions:
            print ("Mars in Conjunction")
            necromancer_magic_number ^= (1 << 3)
        if lib.JUPITER in saturn_conjunctions:
            print ("Jupiter in Conjunction")
            necromancer_magic_number ^= (1 << 4)
        if lib.SOL in saturn_conjunctions:
            print ("Sol in Conjunction")
            necromancer_magic_number ^= (1 << 5)
        print(necromancer_magic_number)
        self.necromancer_popup(necromancer_magic_number)
        return
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def necromancer_popup(self, magic_number):
        necro_pop = QDialog()
        necro_pop.setWindowTitle("Necromancer Reads the Stars")

        layout = QVBoxLayout(necro_pop)  # attach layout to the dialog

        saturn_alone_html = ""
        if magic_number & (1 << 0):
            saturn_alone_html = """
                <h3> Saturn Stands Alone -- Tragedy outside Death brings many new souls to its Gates. </h3>
                Add a total of eight Souls to the Red, Yellow, and Black Gates, distributed in whatever way you please.
            """

        saturn_mercury_html = ""
        if magic_number & (1 << 1):
            saturn_mercury_html = """
                <h3> Mercury in Conjunction -- The dead claw against the Gates. </h3>
                Advance all Foes forward in Death. If a Foe is in a Near Gate, and nothing bars its way, it Escapes.
            """

        saturn_venus_html = ""
        if magic_number & (1 << 2):
            saturn_venus_html = """
                       <h3> Venus in Conjunction -- A Foe consolidates Power. </h3>
                       Create a new Foe within Death, a recent enemy of the Pact or a familiar face. Place them within any Far Gate.
                   """

        saturn_mars_html = ""
        if magic_number & (1 << 3):
            saturn_mars_html = """
                               <h3> Mars in Conjunction -- Primoridal evil festers in the furthest Gates. </h3>
                               I.   Move all Foes in Far and Furthest Gates forward. <br>
                               II.  Create a new Foe within Death, an ancient evil forgotten by the Pact who has finally escaped their bondage. Place them within Terminus.
                           """

        saturn_jupiter_html = ""
        if magic_number & (1 << 4):
            saturn_jupiter_html = """
                                    <h3> Jupiter in Conjunction -- A new Disruptive Ghoulcaller. </h3>
                                    Create a Ghoulcaller and place them in any Near Gate. As long as they continue their operations unchecked, every month all Souls and Foes of Death in an attached Far or Furthest Gate will advance towards them, like a piece of wriggling bait.
                                """

        saturn_sol_html = ""
        if magic_number & (1 << 5):
            saturn_sol_html = """
                                       <h3> Sol in Conjunction --The armies of death coordinate together and march against you. </h3>
                                       I.  Exhaust all Allies. <br>
                                       II. Advance all Foes.
                                   """
        saturn_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Necromancer </h2>
              {saturn_alone_html}
              {saturn_mercury_html}
              {saturn_venus_html}
              {saturn_mars_html}
              {saturn_jupiter_html}
              {saturn_sol_html}
            </div>
        """

        saturn_document = QTextDocument()
        saturn_document.setHtml(saturn_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(saturn_document)

        layout.addWidget(text)

        necro_pop.resize(900, 600)
        necro_pop.exec()


    def hierophant(self):
        conjunctions = self.planet_conjunction_dict()
        print("Conjunctions are: " + str(conjunctions))
        jupiter_conjunctions = conjunctions[lib.JUPITER]
        hierophant_magic_number =0b0000000
        if len(jupiter_conjunctions) == 0:
            print ("Jupiter Stands Alone")
            hierophant_magic_number ^= ( 1 << 0)

        if lib.MERCURY in jupiter_conjunctions:
            print ("Mercury in Conjunction")
            hierophant_magic_number ^= (1 << 1)

        if lib.VENUS in jupiter_conjunctions:
            print ("Venus in Conjunction")
            hierophant_magic_number ^= (1 << 2)

        if lib.MARS in jupiter_conjunctions:
            print ("Mars in Conjunction")
            hierophant_magic_number ^= (1 << 3)

        if lib.SATURN in jupiter_conjunctions:
            print ("Saturn in Conjunction")
            hierophant_magic_number ^= (1 << 4)
        if lib.SOL in jupiter_conjunctions:
            print ("Sol in Conjunction")
            hierophant_magic_number ^= (1 << 5)
        print(hierophant_magic_number)
        self.hierophant_popup(hierophant_magic_number)
        return
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def hierophant_popup(self, magic_number):
        hiero_pop = QDialog()
        hiero_pop.setWindowTitle("Hierophant Reads the Stars")

        layout = QVBoxLayout(hiero_pop)  # attach layout to the dialog

        jupiter_alone_html = ""
        if magic_number & (1 << 0):
            jupiter_alone_html = """
                <h3> Jupiter Stands Alone -- The masses are <i>Starving</i>. </h3>
                    Take from each Temple, then create a Throng of Petitioners in the Temple with the fewest Abundances, representing a community in desperate need of help.
                """

        jupiter_mercury_html = ""
        if magic_number & (1 << 1):
            jupiter_mercury_html = """
                <h3> Mercury in Conjunction -- The masses are <i>Demanding</i>. </h3>
                All Petitioners gain another Hunger. If there are no Petitioners, create a Petitioner in a Temple --- a lost soul with nowhere else to turn.
            """

        jupiter_venus_html = ""
        if magic_number & (1 << 2):
            jupiter_venus_html = """
                       <h3> Venus in Conjunction -- The masses are <i>Devoted</i>. </h3>
                       I.   Add a new Patron to a Temple. <br>
                       II.  Create a Throng of Petitioners at that Temple --- a surge of faithful looking for support
                   """

        jupiter_mars_html = ""
        if magic_number & (1 << 3):
            jupiter_mars_html = """
                               <h3> Mars in Conjunction -- The masses are <i>Violent</i></h3>
                               Each Petitioner Takes from their associated Temple (<i>this doesn't satisfy Hunger</i>). If there are no Petitioners, createa Petitoner in a Temple --- a heartbroken soul whose home was destroyed by violence.
                           """

        jupiter_saturn_html = ""
        if magic_number & (1 << 4):
            jupiter_saturn_html = """
                                    <h3> Saturn in Conjunction -- The masses are <i>Superstitious</i></h3>
                                    You must Spend Time this month sacrificing a named character to the Immortal Flames. Choose someone, and ask the Celestial Audience if any of them have the right to stop the sacrifice (through the king's authority, someone's destiny, and so on). If someone stops you, they take a Major Complication. If you don't sacrifice somone by the end of the month, create a Throng of Petitoners in the Temple with the fewest Abundances, convinced that the world is ending once more.
                                """

        jupiter_sol_html = ""
        if magic_number & (1 << 5):
            jupiter_sol_html = """
                                       <h3> Sol in Conjunction -- The masses are <i>Observant</i></h3>
                                       Choose a Holidat this month. It counts as a Feast Day for the rest of the month. If the current month is already a Feast Day, instead a new Prophet appears at the Temple with the greatest number of Abundances, preaching of a radical interpeation to the Orthodoxy of the Immortal Flame.
                                   """
        jupiter_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Hierophant </h2>
              {jupiter_alone_html}
              {jupiter_mercury_html}
              {jupiter_venus_html}
              {jupiter_mars_html}
              {jupiter_saturn_html}
              {jupiter_sol_html}
            </div>
        """

        jupiter_document = QTextDocument()
        jupiter_document.setHtml(jupiter_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(jupiter_document)

        layout.addWidget(text)

        hiero_pop.resize(900, 600)
        hiero_pop.exec()

    def sorcerer(self):
        conjunctions = self.planet_conjunction_dict()
        print("Conjunctions are: " + str(conjunctions))
        sol_conjunctions = conjunctions[lib.SOL]
        sorcerer_magic_number =0b0000000
        if len(sol_conjunctions) == 0:
            print ("Sol Stands Alone")
            sorcerer_magic_number ^= ( 1 << 0)

        if (lib.MERCURY in sol_conjunctions) ^ (lib.VENUS in sol_conjunctions):
            print ("Mercury or Venus in Conjunction")
            sorcerer_magic_number ^= (1 << 1)

        if lib.MERCURY in sol_conjunctions and lib.VENUS in sol_conjunctions:
            print ("Mercury and Venus in Conjunction")
            sorcerer_magic_number ^= (1 << 2)

        if lib.MARS in sol_conjunctions:
            print ("Mars in Conjunction")
            sorcerer_magic_number ^= (1 << 3)

        if lib.JUPITER in sol_conjunctions:
            print ("Jupiter in Conjunction")
            sorcerer_magic_number ^= (1 << 4)

        if lib.SATURN in sol_conjunctions:
            print ("Saturn in Conjunction")
            sorcerer_magic_number ^= (1 << 5)
        print(sorcerer_magic_number)
        self.sorcerer_popup(sorcerer_magic_number)
        return
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def sorcerer_popup(self, magic_number):
        sorc_pop = QDialog()
        sorc_pop.setWindowTitle("Sorcerer Reads the Stars")

        layout = QVBoxLayout(sorc_pop)  # attach layout to the dialog

        sol_alone_html = ""
        if magic_number & (1 << 0):
            sol_alone_html = """
                <h3> Sol Stands Alone -- Magic dreams of Wildness, and it sparks across the land</h3>
                    For each Region with any number of Hidden Traces on it, double the number of Traces in that region. If there are no hidden traces, instead ask the Celestial Audience which Wizard has the last control over his Domain. Place a Hidden Trace in each Region of that Wizard's Domain.
                """

        sol_mercury_OR_venus_html = ""
        if magic_number & (1 << 1):
            sol_mercury_OR_venus_html = """
                <h3> Mercury or Venus in Conjunction -- Magic dreams of Power, and those who serve it feel its call.</h3>
                Place a hidden trace on each Occultist. If there are no Occultists, place a new Occultist, accompanied by three Hidden Traces, in one of the Wizard's Authorities.
            """

        sol_mercury_AND_venus_html = ""
        if magic_number & (1 << 2):
            sol_mercury_AND_venus_html = """
                       <h3> Mercury and Venus in Conjunction -- Magic dreams of Power, and those who serve it feel its call </h3>
                       I.   Place a hidden trace on each Occultist. <br>
                       II.  Place a new Occultist, accompanied by three Hidden Traces, in one of the Wizard's Authorities.
                   """

        sol_mars_html = ""
        if magic_number & (1 << 3):
            sol_mars_html = """
                               <h3> Mars in Conjunction -- Magic dreams of excitement, and across the Faraway Sea, the world hears its call.</h3>
                               For each Region with a Trace on it, place another Hidden Trace upon it. If fewer than three Traces are placed in this way, then place two Hidden Traces on three different Islands.
                           """

        sol_jupiter_html = ""
        if magic_number & (1 << 4):
            sol_jupiter_html = """
                                    <h3> Jupiter in Conjunction -- Magic dreams of wisdom, and its students become fascinated with its seductive power.</i></h3>
                                    I.  Put a Hidden Trace on one of your Agents. <br>
                                    II. They become an Occultist.<br>
                                    The Agent will remain loyal (and the Academy will thus remain under your Control) until you Confiscate the Agent's Traces, at which point they will depart the Academy and move into an adjacent Domain. <br>
                                    <b>If there is already an Occultist on an Academy,</b> or if you have no Agents, instead ask the Celestial Audience which Domain is stealing from your own, and move half of all Traces in your Tower into that Domain's Authority. These Traces become Hidden.
                                """

        sol_saturn_html = ""
        if magic_number & (1 << 5):
            sol_saturn_html = """
                                       <h3> Saturn in Conjunction -- Magic dreams of desolation, and its presence in Isha leads to calamity.</h3>
                                       Place three Hidden Traces in one of the Secret Regions, as dangerous power builds at the edge of the world. Ask the Wizard whose Domain it falls under to invent a mighty enemy Occultist, but to keep them secret from you for now --- you can discover who they are when you Investigate.
                                   """
        sol_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Hierophant </h2>
              {sol_alone_html}
              {sol_mercury_OR_venus_html}
              {sol_mercury_AND_venus_html}
              {sol_mars_html}
              {sol_saturn_html}
              {sol_jupiter_html}
            </div>
        """

        sol_document = QTextDocument()
        sol_document.setHtml(sol_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(sol_document)

        layout.addWidget(text)

        sorc_pop.resize(900, 600)
        sorc_pop.exec()

    def faustian(self):
        conjunctions = self.planet_conjunction_dict()
        print("Conjunctions are: " + str(conjunctions))
        mercury_conjunctions = conjunctions[lib.MERCURY]
        faust_factor = len(mercury_conjunctions)
        self.faustian_popup(faust_factor)
        return
            ## TODO: Magic number bits 6 & 7 are reserved for calamity and extinction which are beyond the scope of the project at the moment
    def faustian_popup(self, magic_number):
        faust_pop = QDialog()
        faust_pop.setWindowTitle("Faustian Reads the Stars")

        layout = QVBoxLayout(faust_pop)  # attach layout to the dialog

        faust_alone_html = ""
        if magic_number == 0:
            mercury_alone_html = """
                <h3> The Devil seeks the affection of another Wizard.</h3>
                    Another Wizard recieves an invitation to Spend Time and have a Scene with the Devil, in which the Devil will make him a Bargain. If a Wizard refuses to meet with the Devil at all, the Devil places a Scheme onto each of that Wizard's Communities.
                """
        else:
            mercury_among_html = """
            <h3> The Devil Schemes </h3>
            Place two Scheme Cards per planet in conjunction with the current house.
            """

        mercury_stars_html = f"""
            <div style="font-family: serif;">
              <h2> Faustian </h2>
              {mercury_alone_html}
              {mercury_among_html}
            </div>
        """

        faust_document = QTextDocument()
        faust_document.setHtml(mercury_stars_html)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setDocument(faust_document)

        layout.addWidget(text)

        faust_pop.resize(900, 600)
        faust_pop.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    latin = "NotoSans-VariableFont_wdth,wght.ttf"
    sym1 = "NotoSansSymbols2-Regular.ttf"
    sym2 = "NotoSansSymbols-VariableFont_wght.ttf"  # or another symbols font


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
    w = MainWidget()
    w.resize(1500, 760)
    w.show()
    sys.exit(app.exec())
