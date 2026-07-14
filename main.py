import tkinter as tk
from tkinter import filedialog
import math
import struct
# import lib
from planet import Planet
from planet import Saturn
from house import House


class OrreryApp:
    # Binary file format:
    # magic(8s) = b'ORRERY1\0'
    # version(uint32) = 1
    # steps(uint32)   = STEPS
    # planet_count(uint32)
    # planet_step_indices(uint16 * planet_count)  (each is 0..47)
    MAGIC = b"ORRERY1\0"
    VERSION = 1

    def __init__(self, root):
        self.root = root
        self.root.title("Orrery")

        main = tk.Frame(root)
        main.grid(row=0, column=0, sticky="nsew")

        left = tk.Frame(main)
        left.grid(row=0, column=0, sticky="ns", padx=(10, 12), pady=10)

        self.mode = tk.StringVar(value="Estates")
        tk.Label(left, text="Render:").pack(anchor="w", pady=(0, 6))
        for label in ("Estates", "Elements", "Seasons"):
            tk.Radiobutton(
                left,
                text=label,
                variable=self.mode,
                value=label,
                command=self.draw,
                anchor="w",
            ).pack(anchor="w")

        center = tk.Frame(main)
        center.grid(row=0, column=1, sticky="nsew")
        self.canvas = tk.Canvas(center, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=(0, 10), pady=10)

        right = tk.Frame(main)
        right.grid(row=0, column=2, sticky="ns", padx=(0, 10), pady=10)

        self.table_frame = tk.LabelFrame(right, text="conjunctions")
        self.table_frame.pack(fill="both", expand=False)

        self.table_grid = tk.Frame(self.table_frame)
        self.table_grid.pack(padx=8, pady=8)

        self.center = (CANVAS_SIZE // 2, CANVAS_SIZE // 2)
        self.outer_r = MAX_RADIUS

        self.planets = [
            Planet(name="Mercury", radius=RADII[0], color="#0b57d0", sweep_steps=ARC_SWEEP_STEPS[0]),
            Planet(name="Venus", radius=RADII[1], color="#ff6b6b", sweep_steps=ARC_SWEEP_STEPS[1]),
            Planet(name="Mars", radius=RADII[2], color="#2ecc71", sweep_steps=ARC_SWEEP_STEPS[2]),
            Planet(name="Jupiter", radius=RADII[3], color="#f39c12", sweep_steps=ARC_SWEEP_STEPS[3]),
            Saturn(name="Saturn", radius=RADII[4], color="#9b59b6", sweep_steps=ARC_SWEEP_STEPS[4]),
        ]

        house_names = [
            "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius",
            "Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini",
        ]

        estate_color_dict = {'cosmic':"#b7cece", 'spiritual':"#89408c", 'terrestrial':"#583e23"}
        element_color_dict = {'fire':"#7c1b1b", 'water':"#0e40ad", 'earth':"#774714", 'air':"#19b3ad"}
        season_color_dict = {'winter':"#43acc7", 'spring':"#0d5945", 'summer':"#edd892", 'autumn':"#dd8c61"}
        estate_fill = [
            estate_color_dict['terrestrial'],estate_color_dict['terrestrial'],estate_color_dict['terrestrial'],
            estate_color_dict['cosmic'],estate_color_dict['cosmic'],estate_color_dict['cosmic'],
            estate_color_dict['cosmic'],estate_color_dict['spiritual'],estate_color_dict['spiritual'],
            estate_color_dict['spiritual'],estate_color_dict['spiritual'],estate_color_dict['terrestrial'],
        ]
        element_fill = [
            element_color_dict['air'], element_color_dict['earth'], element_color_dict['fire'],
            element_color_dict['water'], element_color_dict['air'], element_color_dict['earth'],
            element_color_dict['fire'], element_color_dict['water'], element_color_dict['air'],
            element_color_dict['earth'], element_color_dict['fire'], element_color_dict['water'],
        ]
        season_fill = [
            season_color_dict['summer'], season_color_dict['summer'], season_color_dict['summer'],
            season_color_dict['spring'], season_color_dict['spring'], season_color_dict['spring'],
            season_color_dict['winter'], season_color_dict['winter'], season_color_dict['winter'],
            season_color_dict['autumn'], season_color_dict['autumn'], season_color_dict['autumn'],
        ]

        self.houses = [
            House(
                index_1_based=i + 1,
                name=house_names[i],
                estate_fill=estate_fill[i],
                element_fill=element_fill[i],
                season_fill=season_fill[i],
                outline_color=GRID12_OUTLINE,
                step_index_zero_based=i,
            )
            for i in range(GRID12_STEPS)
        ]

        controls = tk.Frame(root)
        controls.grid(row=1, column=0, sticky="ew", padx=10, pady=6)
        controls.grid_columnconfigure(0, weight=1)

        top = tk.Frame(controls)
        top.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 8))

        tk.Button(
            top,
            text="Save state (binary)",
            command=self.save_state,
            width=18,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            top,
            text="Load state (binary)",
            command=self.load_state,
            width=18,
        ).pack(side="left", padx=(0, 18))

        tk.Button(
            top,
            text="Sweep all arcs forward by their sweep value ▶▶",
            command=self.sweep_all_forward_clockwise_by_sweep,
            width=40,
        ).pack(side="left")

        per_arc = tk.Frame(controls)
        per_arc.grid(row=1, column=0, columnspan=5, sticky="ew")

        for i, p in enumerate(self.planets):
            box = tk.LabelFrame(per_arc, text=f"{p.name} (sweep={p.sweep_steps} steps)")
            box.grid(row=0, column=i, padx=6, pady=4, sticky="n")

            tk.Button(
                box,
                text="forward sweep ▶▶",
                command=lambda idx=i: self.move_arc_by_sweep(idx, -1),
                width=14,
            ).pack(side="top", padx=6, pady=4)

            tk.Button(
                box,
                text="◀◀ back sweep",
                command=lambda idx=i: self.move_arc_by_sweep(idx, +1),
                width=14,
            ).pack(side="top", padx=6, pady=4)

            tk.Button(
                box,
                text="forward step ▶",
                command=lambda idx=i: self.move_arc_by_step(idx, -1),
                width=14,
            ).pack(side="top", padx=6, pady=4)

            tk.Button(
                box,
                text="◀ back step",
                command=lambda idx=i: self.move_arc_by_step(idx, +1),
                width=14,
            ).pack(side="top", padx=6, pady=4)

        self.draw()

    def move_arc_by_sweep(self, idx: int, direction_sign: int):
        self.planets[idx].move_by_sweep(direction_sign)
        self.draw()

    def move_arc_by_step(self, idx: int, direction_sign: int):
        self.planets[idx].move_by_step(direction_sign)
        self.draw()

    def sweep_all_forward_clockwise_by_sweep(self):
        for p in self.planets:
            p.move_by_sweep(-1)
        self.draw()


    def _draw_48_step_grid(self):
        cx, cy = self.center
        for k in range(STEPS):
            ang = deg_to_rad(k * STEP_ANGLE)
            x2 = cx + math.cos(ang) * self.outer_r
            y2 = cy + math.sin(ang) * self.outer_r
            self.canvas.create_line(cx, cy, x2, y2, fill=GRID48_OUTLINE, width=1)

            tick = 6
            tx = cx + math.cos(ang) * (self.outer_r - tick)
            ty = cy + math.sin(ang) * (self.outer_r - tick)
            self.canvas.create_oval(tx - 2, ty - 2, tx + 2, ty + 2, fill=GRID48_OUTLINE, outline="")

    def save_state(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".orr",
            filetypes=[("Orrery state", "*.orr"), ("All files", "*.*")],
            title="Save binary state",
        )
        if not path:
            return

        planet_step_indices = [p.step_index() for p in self.planets]
        planet_count = len(planet_step_indices)

        header = struct.pack("<8sIII", self.MAGIC, self.VERSION, STEPS, planet_count)  # (magic, ver, steps, count)
        body = struct.pack(f"<{planet_count}H", *planet_step_indices)  # each as uint16

        with open(path, "wb") as f:
            f.write(header)
            f.write(body)

    def load_state(self):
        path = filedialog.askopenfilename(
            filetypes=[("Orrery state", "*.orr"), ("All files", "*.*")],
            title="Load binary state",
        )
        if not path:
            return

        with open(path, "rb") as f:
            header = f.read(struct.calcsize("<8sIII"))
            if len(header) != struct.calcsize("<8sIII"):
                return

            magic, version, steps_in_file, planet_count = struct.unpack("<8sIII", header)
            if magic != self.MAGIC or version != self.VERSION:
                return
            if steps_in_file != STEPS:
                return

            body = f.read(struct.calcsize(f"<{planet_count}H"))
            if len(body) != struct.calcsize(f"<{planet_count}H"):
                return

            step_indices = list(struct.unpack(f"<{planet_count}H", body))

        # Apply only as many as we have planets in this app
        n = min(len(self.planets), len(step_indices))
        for i in range(n):
            self.planets[i].set_step_index(step_indices[i])

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        cx, cy = self.center

        self.canvas.create_oval(
            cx - self.outer_r, cy - self.outer_r,
            cx + self.outer_r, cy + self.outer_r,
            outline="#000000", width=2
        )

       # self._draw_48_step_grid()

        mode = self.mode.get()
        for h in self.houses:
            h.draw(canvas=self.canvas, cx=cx, cy=cy, outer_r=self.outer_r, mode=mode)

        for p in self.planets:
            r = p.radius
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=p.angle,
                extent=p.sweep_degrees(),
                style=tk.ARC,
                outline=p.color,
                width=ARC_WIDTH,
            )

        self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#333", outline="")

        # self._render_conjunctions_table()


if __name__ == "__main__":
    root = tk.Tk()
    OrreryApp(root)
    root.mainloop()