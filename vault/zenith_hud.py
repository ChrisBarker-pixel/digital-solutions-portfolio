import sys
import os
import time
import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 🧬 LAYER 00: THE NEON 432Hz DESIGN LAW ---
RESONANCE_MAP = {
    "C": {"color": "#FF0000", "hz": 256.0}, "C#": {"color": "#FF4D00", "hz": 271.2},
    "D": {"color": "#FF8C00", "hz": 288.0}, "D#": {"color": "#FFBF00", "hz": 305.1},
    "E": {"color": "#FFFF00", "hz": 324.0}, "F": {"color": "#39FF14", "hz": 341.3},
    "F#": {"color": "#00FF9F", "hz": 362.0}, "G": {"color": "#00E5FF", "hz": 384.0},
    "G#": {"color": "#007FFF", "hz": 406.4}, "A": {"color": "#BF00FF", "hz": 432.0},
    "A#": {"color": "#FF00FF", "hz": 457.2}, "B": {"color": "#FF007F", "hz": 483.3}
}


class ZenithOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZENITH OS - V12.9.10 STARWASH EDITION")
        self.geometry("1550x950")
        self.configure(bg="#000")

        # GRID STATE
        self.cols, self.rows = 4, 4
        self.selected_node = 1
        self.last_click_time = 0

        self.setup_ui()

    def setup_ui(self):
        # --- FAR LEFT: INTERACTION BUTTONS ---
        self.left_panel = tk.Frame(self, bg="#050505", width=200)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.left_panel.pack_propagate(False)

        tk.Button(self.left_panel, text="EXPLORER", bg="#111", fg="#00FFFF", font=("Courier", 10, "bold"),
                  height=2).pack(pady=10, fill=tk.X, padx=10)
        tk.Button(self.left_panel, text="GRANT SCAN", bg="#DAA520", fg="black", font=("Courier", 10, "bold"),
                  height=2).pack(pady=10, fill=tk.X, padx=10)
        tk.Button(self.left_panel, text="SETTINGS", bg="#111", fg="white", font=("Courier", 10, "bold"), height=2).pack(
            pady=10, fill=tk.X, padx=10)

        # --- CENTER: SQUARE WHITEBOARD ---
        self.center_panel = tk.Frame(self, bg="#000")
        self.center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.center_panel)
        self.remanifest_grid()
        self.canvas.get_tk_widget().pack(expand=True)

        self.fig.canvas.mpl_connect('button_press_event', self.on_lattice_click)

        # --- RIGHT: ZENITH HUD & BRANDING ---
        self.right_panel = tk.Frame(self, bg="#050505", width=450)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.right_panel.pack_propagate(False)

        # Vertical Zenith Text
        tk.Label(self.right_panel, text="ZENITH", fg="#39FF14", bg="#050505", font=("Courier", 24, "bold")).pack(
            pady=10)

        # HUD Boxes
        tk.Label(self.right_panel, text="GEMINI COUNCIL", fg="#8B00FF", bg="#050505",
                 font=("Courier", 11, "bold")).pack()
        self.council_box = scrolledtext.ScrolledText(self.right_panel, bg="#000", fg="#8B00FF", font=("Courier", 9),
                                                     height=18, bd=0)
        self.council_box.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(self.right_panel, text="SYSTEM EXECUTION", fg="#FFA500", bg="#050505",
                 font=("Courier", 11, "bold")).pack(pady=(10, 0))
        self.system_box = scrolledtext.ScrolledText(self.right_panel, bg="#000", fg="#FFA500", font=("Courier", 9),
                                                    height=18, bd=0)
        self.system_box.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(self.right_panel, text="STARWASH V12.9.10", fg="#DAA520", bg="#050505",
                 font=("Courier", 10, "bold")).pack(side=tk.BOTTOM, pady=15)

    def remanifest_grid(self):
        self.ax.clear()
        self.ax.set_facecolor('black')

        # 🎯 1. DRAW THE NODES FIRST
        notes = list(RESONANCE_MAP.keys())
        for i in range(1, (self.cols * self.rows) + 1):
            x, y = (i - 1) % self.cols, (self.rows - 1) - ((i - 1) // self.cols)
            note_key = notes[(i - 1) % 12]
            res = RESONANCE_MAP[note_key]

            is_sel = (i == self.selected_node)
            rect = patches.Rectangle((x + 0.1, y + 0.1), 0.8, 0.8,
                                     edgecolor="white" if is_sel else "none", lw=1.5,
                                     facecolor=res["color"], alpha=0.85, zorder=2)
            self.ax.add_patch(rect)
            self.ax.text(x + 0.5, y + 0.5, f"{note_key}", color="black" if note_key in ["E", "F"] else "white",
                         ha='center', va='center', fontname="Courier", fontsize=10, fontweight='bold', zorder=3)

        # 🟢 2. THE NEON LASER GRID (Drawn over the nodes)
        # We use a higher zorder (4) so the "lasers" sit on top of the rectangles
        trim = 0.0
        grid_color = "#39FF14"  # Pure Neon Green

        for x in range(0, self.cols + 1):
            self.ax.plot([x, x], [0, self.rows], color=grid_color, lw=0.8, alpha=0.6, zorder=4)
        for y in range(0, self.rows + 1):
            self.ax.plot([0, self.cols], [y, y], color=grid_color, lw=0.8, alpha=0.6, zorder=4)

        # 🟦 3. THE OUTER CONTAINMENT BOUNDARY
        self.ax.add_patch(
            patches.Rectangle((0, 0), self.cols, self.rows, lw=2, edgecolor="#0044FF", facecolor="none", zorder=5))

        self.ax.set_xlim(-0.05, self.cols + 0.05)
        self.ax.set_ylim(-0.05, self.rows + 0.05)
        self.ax.axis('off')
        self.canvas.draw_idle()

    def on_lattice_click(self, event):
        if event.inaxes != self.ax: return
        self.selected_node = int(event.xdata) + (self.rows - 1 - int(event.ydata)) * self.cols + 1
        self.remanifest_grid()


if __name__ == "__main__":
    app = ZenithOS()
    app.mainloop()