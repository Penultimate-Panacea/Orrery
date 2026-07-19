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
    grid_offset_half_step: bool = False  # used for Saturn's 36-step half-step offset

    @property
    def step_deg(self) -> float:
        """Degrees advanced per step around a full circle.

        Computes the size of one step in degrees based on the configured
        `step_count_circle`.

        Returns:
            float: The angular increment (degrees) corresponding to a single step.
        """
        return 360.0 / self.step_count_circle

    def start_deg(self) -> float:
        """Angular position for the current step (in degrees).

        Uses the convention of 0 degrees at the 12 o'clock position and increases
        clockwise. If `grid_offset_half_step` is enabled, applies a +0.5 step
        offset.

        Returns:
            float: The start angle for the current step, in degrees, normalized
                to the configured circle step count.
        """
        # 0 at 12 o'clock clockwise
        base = (self.current_step % self.step_count_circle)
        if self.grid_offset_half_step:
            base += 0.5
        return (base % self.step_count_circle) * self.step_deg

    def angle_for_step(self, step_offset: int) -> float:
        """Angular position for a step relative to the current step.

        Computes the angle (in degrees) corresponding to `current_step +
        step_offset`, normalized to the circle step count. Uses the convention
        of 0 degrees at 12 o'clock and increases clockwise. If `grid_offset_half_step`
        is enabled, applies a +0.5 step offset.

        Args:
            step_offset (int): Integer offset (in steps) relative to `current_step`.

        Returns:
            float: The angle for the requested step offset, in degrees.
        """
        base = (self.current_step + step_offset) % self.step_count_circle
        if self.grid_offset_half_step:
            base += 0.5
        return (base % self.step_count_circle) * self.step_deg

    def set_current_step(self, new_step):
        """Set the internal current step index.

        Updates `self.current_step` to the provided value.

        Args:
            new_step: The new step index to store in `self.current_step`.

        Returns:
            None
        """
        self.current_step = new_step

