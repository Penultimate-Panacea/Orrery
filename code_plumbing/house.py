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
    def start_deg(self) -> float:
        """Start angle (in degrees) for this sector.

        Uses a 12-sector, 30 degrees-per-sector layout, with 0° positioned at 12 o'clock
        and angles increasing clockwise.

        Returns:
            float: Sector start angle in degrees.
        """
        # 0 at 12 o'clock, increasing clockwise
        return self.index * 30.0

    @property
    def end_deg(self) -> float:
        """End angle (in degrees) for this sector.

        The end angle is the start angle plus 30 degrees for a 12-sector layout.

        Returns:
            float: Sector end angle in degrees.
        """
        return (self.index + 1) * 30.0

    def contains_angle(self, deg: float) -> bool:
        """Check whether a given angle falls within this sector.

        Normalizes `deg` into [0, 360) and compares it against the sector's
        start/end angles. For the last sector (`index == 11`), it correctly
        handles wrap-around across 360°.

        Args:
            deg: Angle in degrees to test.

        Returns:
            bool: True if `deg` lies within the sector, otherwise False.
        """
        d = deg % 360.0
        start = self.start_deg % 360.0
        end = self.end_deg % 360.0
        if self.index == 11:
            return d >= start or d < end
        return (d >= start) and (d < end)

    def color_for(self, mode: str) -> str:
        """Return the sector color for a given coloring mode.

        Args:
            mode: Coloring mode selector. Expected values:
                - "estate": use `self.estate_color`
                - "season": use `self.season_color`
                - any other value: use `self.element_color`

        Returns:
            str: Color value for the selected mode.
        """
        if mode == "estate":
            return self.estate_color
        if mode == "season":
            return self.season_color
        return self.element_color
