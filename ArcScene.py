# coding=utf-8
import sys
import math
from typing import List
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPen, QColor, QPainterPath, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsScene
from planet import Planet

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
        pen.setCapStyle(Qt.RoundCap)
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
