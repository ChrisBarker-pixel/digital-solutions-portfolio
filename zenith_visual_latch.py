import tkinter as tk
from PIL import Image, ImageTk
import os

class VisualLatch:
    def __init__(self, parent_app):
        self.app = parent_app

    def manifest_image(self, node_id):
        data = self.app.active_lattice.get(node_id)
        if not data: return
        img_path = data.get('path')
        if not img_path or not os.path.exists(img_path):
            self.app.log_system(f"PATH_ERR: {img_path}")
            return

        win = tk.Toplevel(self.app)
        win.title(f"VIEWER >> {data.get('title')}")
        win.configure(bg="#050505")
        win.attributes('-topmost', True)

        try:
            img = Image.open(img_path)
            img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=photo, bg="#000", highlightthickness=1, highlightbackground="#DAA520")
            lbl.image = photo
            lbl.pack(padx=20, pady=20)
            tk.Label(win, text=f"SOURCE: {img_path}", fg="#DAA520", bg="#050505", font=("Courier", 9)).pack(pady=5)
        except Exception as e:
            self.app.log_system(f"RENDER_ERR: {e}")

def strike(app, node_id):
    latch = VisualLatch(app)
    latch.manifest_image(node_id)