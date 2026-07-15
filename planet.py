# coding=utf-8
from dataclasses import dataclass
from PyQt6.QtGui import QColor


@dataclass
class Planet:
    name: str
    arc_color: QColor
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
