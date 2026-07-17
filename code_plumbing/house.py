# coding=utf-8
from dataclasses import dataclass

@dataclass
class House:
    name: str
    index: int
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