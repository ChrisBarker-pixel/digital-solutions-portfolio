import sys
import os
import time
import datetime
import threading
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk
import importlib.util
import webbrowser
import matplotlib

# 🎯 ENSURE BACKEND STABILITY
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 🛰️ MODERN NEURAL LATCH
try:
    from google import genai
except ImportError:
    print("❌ CRITICAL: google-genai missing.")

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, db as rtdb
except ImportError:
    print("❌ CRITICAL: firebase-admin missing.")

# --- 🛰️ PATH LAW (X9 PRO) ---
VAULT_PATH = "/Volumes/X9 Pro/Zenith Rebuild Main/vault/.env"
NAV_PATH = "/Volumes/X9 Pro/Zenith Rebuild Main/zenith_navigator_isolated.py"
SERVICE_KEY = "/Volumes/X9 Pro/Zenith Rebuild Main/serviceAccountKey.json"
MASTER_JSON = "/Volumes/X9 Pro/Zenith Rebuild Main/portal_nodes_MASTER.json"

NEURAL_CONFIG = {
    "ENGINE": "models/gemini-3.1-flash-lite-preview",
    "GRANT": "models/gemini-3.1-pro",
    "GROQ": "llama-3.3-70b-versatile"
}

RESONANCE_MAP = {
    0: {"note": "C", "color": "#FF0000"}, 1: {"note": "C#", "color": "#FF4D00"},
    2: {"note": "D", "color": "#FF8C00"}, 3: {"note": "D#", "color": "#FFBF00"},
    4: {"note": "E", "color": "#FFFF00"}, 5: {"note": "F", "color": "#39FF14"},
    6: {"note": "F#", "color": "#00FF9F"}, 7: {"note": "G", "color": "#00E5FF"},
    8: {"note": "G#", "color": "#007FFF"}, 9: {"note": "A", "color": "#BF00FF"},
    10: {"note": "A#", "color": "#FF00FF"}, 11: {"note": "B", "color": "#FF007F"}
}


def get_api_key():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, 'r') as f:
                for line in f:
                    if 'GOOGLE_API_KEY' in line:
                        return line.split('=')[1].strip().strip('"').strip("'")
        except:
            pass
    return None


# --- 📋 COMPONENT: HIGH-DETAIL NODE INDEX ---
class ZenithNodeMenu(tk.Toplevel):
    def __init__(self, parent, nodes_dict):
        super().__init__(parent)
        self.parent = parent
        self.title("ZENITH_LATTICE_INDEX // 432Hz")
        self.geometry("850x500")
        self.configure(bg="#050505")
        self.attributes('-topmost', True)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Preview"), show="headings")
        self.tree.heading("ID", text="ID");
        self.tree.heading("Title", text="NODE_TITLE");
        self.tree.heading("Preview", text="PAYLOAD_PREVIEW")
        self.tree.column("ID", width=60, anchor=tk.CENTER);
        self.tree.column("Title", width=240);
        self.tree.column("Preview", width=500)
        self.tree.pack(fill=tk.BOTH, expand=True)

        for n_id, data in sorted(nodes_dict.items()):
            logic = data.get('logic', '').strip()
            preview = logic.split('\n')[0][:80] if logic else "EMPTY"
            self.tree.insert("", tk.END, values=(f"{n_id:03d}", data.get('title', 'UNTITLED'), preview))
        self.tree.bind("<Double-1>", lambda e: self.open_selected())

    def open_selected(self):
        item = self.tree.selection()[0]
        n_id = int(self.tree.item(item)['values'][0])
        NodeEditor(self.parent, n_id, self.parent.active_lattice[n_id])
        self.destroy()


# --- 🧪 COMPONENT: PAYLOAD EDITOR ---
class NodeEditor(tk.Toplevel):
    def __init__(self, parent, node_id, data):
        super().__init__(parent)
        self.parent, self.node_id = parent, node_id
        self.title(f"PAYLOAD: NODE_{node_id:03d}");
        self.geometry("600x650");
        self.configure(bg="#050505")
        self.attributes('-topmost', True)

        header = tk.Frame(self, bg="#050505");
        header.pack(fill=tk.X, pady=10)
        tk.Label(header, text=data.get('title', 'NODE'), fg=data.get('color', '#39FF14'), bg="#050505",
                 font=("sans-serif", 14, "bold")).pack(side=tk.LEFT, padx=20)

        self.txt = scrolledtext.ScrolledText(self, bg="#000", fg="#39FF14", font=("monospace", 11), bd=0)
        self.txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.txt.insert(tk.END, data.get('logic', '# Empty Logic Stream'))

        btn_frame = tk.Frame(self, bg="#050505");
        btn_frame.pack(pady=20, fill=tk.X, padx=20)
        btn_law = {"bg": "#bbbbbb", "fg": "#000", "font": ("sans-serif", 9, "bold"), "relief": "flat", "height": 2}
        tk.Button(btn_frame, text="RUN", **btn_law, width=10, command=self.execute_payload).pack(side=tk.LEFT, padx=5,
                                                                                                 expand=True)
        tk.Button(btn_frame, text="APPLY", **btn_law, width=10, command=self.apply_to_ram).pack(side=tk.LEFT, padx=5,
                                                                                                expand=True)
        tk.Button(btn_frame, text="TRASH", **btn_law, width=10, command=self.trash_node).pack(side=tk.LEFT, padx=5,
                                                                                              expand=True)

    def apply_to_ram(self):
        self.parent.active_lattice[self.node_id]['logic'] = self.txt.get("1.0", tk.END)
        self.parent.log_system(f"🧠 RAM_LATCH: Node_{self.node_id} updated.")
        self.parent.remanifest_grid();
        self.destroy()

    def execute_payload(self): self.parent.execute_node_logic(self.node_id)

    def trash_node(self):
        if self.node_id in self.parent.active_lattice:
            del self.parent.active_lattice[self.node_id]
            self.parent.after(0, self.parent.remanifest_grid);
            self.destroy()


# --- 🛰️ CORE ENGINE: ZENITH_OS ---
class ZenithOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZENITH_OS // 432Hz RESONANCE");
        self.geometry("1400x900");
        self.configure(bg="#050505")
        self.active_lattice, self.manifest_count, self.node_mode, self.last_click_time = {}, 0, True, 0
        self.setup_ui();
        self.background_boot()
        self.fig, self.ax = plt.subplots(figsize=(12, 9), facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.whiteboard_slot)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.after(500, self.auto_hydrate_from_master)

    def setup_ui(self):
        btn_law = {"bg": "#bbbbbb", "fg": "#000", "font": ("sans-serif", 11, "bold"), "relief": "flat", "height": 2}
        self.left_f = tk.Frame(self, bg="#050505", width=220);
        self.left_f.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=10);
        self.left_f.pack_propagate(False)
        tk.Button(self.left_f, text="NAVIGATOR", **btn_law, command=self.launch_navigator).pack(pady=5, fill=tk.X,
                                                                                                padx=10)
        tk.Button(self.left_f, text="NODE MENU", **btn_law, command=self.open_node_menu).pack(pady=5, fill=tk.X,
                                                                                              padx=10)
        tk.Button(self.left_f, text="NODE_MODE", **btn_law, command=self.toggle_mode).pack(pady=5, fill=tk.X, padx=10)
        tk.Button(self.left_f, text="SAVE SCENE AS...", bg="#FFA500", fg="#000", font=("sans-serif", 11, "bold"),
                  command=self.save_scene_as).pack(pady=20, fill=tk.X, padx=10)
        tk.Button(self.left_f, text="NEW SCENE (CLEAR)", bg="#FF3131", fg="#FFF", font=("sans-serif", 11, "bold"),
                  command=self.clear_to_new_scene).pack(pady=5, fill=tk.X, padx=10)

        # --- 🛰️ PORTAL ZONE (MODERNIZED) ---
        btn_portal = {"bg": "#111", "fg": "#00E5FF", "font": ("sans-serif", 10, "bold"), "relief": "flat", "height": 2}

        def launch_portal(url, name):
            self.log_system(f"🚀 NAVIGATING: {name} Portal Latching...", "ZENITH")
            if hasattr(self, 'trigger_siren'): self.trigger_siren(name)
            webbrowser.open(url)

        tk.Button(self.left_f, text="🌐 ZENITH HUB LIVE", **btn_portal,
                  command=lambda: launch_portal("https://zenith-hub-2026-official.web.app", "ZENITH_HUB")).pack(
            side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        tk.Button(self.left_f, text="🥋 WING CHUN SITE", **btn_portal,
                  command=lambda: launch_portal("https://sprout-wing-chun.web.app", "WING_CHUN")).pack(side=tk.BOTTOM,
                                                                                                       fill=tk.X,
                                                                                                       padx=10, pady=5)

        # 🧼 STARWASH BUTTON (DYNAMIC LATCH)
        tk.Button(self.left_f, text="🌐 STARWASH LIVE", **btn_portal,
                  command=lambda: launch_portal("https://star-wash-express.com", "STARWASH")).pack(side=tk.BOTTOM,
                                                                                                   fill=tk.X, padx=10,
                                                                                                   pady=5)

        self.right_f = tk.Frame(self, bg="#050505", width=450);
        self.right_f.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=10);
        self.right_f.pack_propagate(False)
        self.council_box = scrolledtext.ScrolledText(self.right_f, bg="#000", fg="#8B00FF", font=("monospace", 10),
                                                     height=18, bd=0);
        self.council_box.pack(padx=10, pady=5, fill=tk.X)
        self.system_box = scrolledtext.ScrolledText(self.right_f, bg="#000", fg="#FFA500", font=("monospace", 10),
                                                    height=18, bd=0);
        self.system_box.pack(padx=10, pady=5, fill=tk.X)

        self.center_f = tk.Frame(self, bg="#000");
        self.center_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_bar = tk.Entry(self.center_f, bg="#111", fg="#39FF14", font=("sans-serif", 14),
                                 insertbackground="white", bd=0);
        self.chat_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        self.chat_bar.bind("<Return>", self.handle_input)
        self.whiteboard_slot = tk.Frame(self.center_f, bg="#000");
        self.whiteboard_slot.pack(fill=tk.BOTH, expand=True)

    def background_boot(self):
        api_key = get_api_key()
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key);
                self.log_system("🧠 NEURAL_ENGINE: v2 Online")
            except Exception as e:
                self.log_system(f"⚠️ NEURAL_ERR: {e}")
        try:
            if os.path.exists(SERVICE_KEY):
                if not firebase_admin._apps:
                    cred = credentials.Certificate(SERVICE_KEY)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': 'https://zenith-hub-2026-official-default-rtdb.firebaseio.com/'})
                self.db = firestore.client()
                self.db_realtime = rtdb
                self.log_system("BOOT: DUAL_FIREBASE_ACTIVE")
        except Exception as e:
            self.log_system(f"❌ BOOT_ERR: {e}")

    def execute_node_logic(self, node_id):
        data = self.active_lattice.get(node_id)
        if not data: return
        self.log_system(f"⚡ PULSE: Node_{node_id:03d}")
        context = {"app": self, "os": os, "time": time, "tk": tk, "firestore": firestore,
                   "db": self.db_realtime if hasattr(self, 'db_realtime') else None}
        try:
            exec(data['logic'], context)
        except Exception as e:
            self.log_system(f"❌ EXEC_ERR: {e}")

    def remanifest_grid(self):
        self.current_cols, self.current_rows = 16, 12
        self.ax.clear();
        self.ax.set_facecolor('#050505');
        self.ax.set_xlim(-0.1, self.current_cols);
        self.ax.set_ylim(-0.1, self.current_rows);
        self.ax.axis('off')
        for n_id, data in self.active_lattice.items():
            try:
                idx = int(n_id) - 1
                col, row = idx % self.current_cols, (self.current_rows - 1) - (idx // self.current_cols)
                rect = patches.Rectangle((col + 0.05, row + 0.05), 0.9, 0.9, facecolor=data.get('color', '#1a1a1a'),
                                         alpha=0.9, edgecolor='#ffffff', linewidth=0.3, zorder=2)
                self.ax.add_patch(rect)
                self.ax.text(col + 0.5, row + 0.5, f"{int(n_id)}\n{data.get('title')[:10]}", color='white', fontsize=6,
                             ha='center', va='center', fontweight='bold', zorder=3)
            except:
                continue
        self.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax: return
        now = time.time()
        col, row = int(event.xdata), (self.current_rows - 1) - int(event.ydata)
        idx = row * self.current_cols + col + 1
        if idx in self.active_lattice:
            if now - self.last_click_time < 0.4:
                NodeEditor(self, idx, self.active_lattice[idx])
            else:
                self.execute_node_logic(idx)
        self.last_click_time = now

    def manifest_node(self, **kwargs):
        node_id = kwargs.get('node_id', self.manifest_count + 1)
        self.manifest_count = max(self.manifest_count, node_id)
        self.active_lattice[node_id] = {'title': kwargs.get('title', 'NODE'),
                                        'color': kwargs.get('color', RESONANCE_MAP[node_id % 12]['color']),
                                        'logic': kwargs.get('logic', '# Logic'), 'metadata': kwargs}
        self.after(0, self.remanifest_grid)

    def relay_pipeline(self, query):
        try:
            resp = self.client.models.generate_content(model=NEURAL_CONFIG["ENGINE"],
                                                       contents=f"Output ONLY Python code: app.manifest_node(node_id=INT, title='', logic=''). Target: {query}")
            clean_code = resp.text.replace('```python', '').replace('```', '').strip()
            self.after(0, lambda code=clean_code: exec(code, {"app": self}))
        except Exception as e:
            self.log_system(f"❌ RELAY_ERR: {e}")

    def chat_pipeline(self, q):
        try:
            resp = self.client.models.generate_content(model=NEURAL_CONFIG["ENGINE"], contents=q)
            self.after(0, lambda: self.log_council(f"ENGINE >> {resp.text}"))
        except:
            pass

    def handle_input(self, event):
        q = self.chat_bar.get().strip();
        self.chat_bar.delete(0, tk.END)
        if q: threading.Thread(target=self.relay_pipeline if self.node_mode else self.chat_pipeline, args=(q,),
                               daemon=True).start()

    def auto_hydrate_from_master(self):
        if os.path.exists(MASTER_JSON):
            try:
                with open(MASTER_JSON, 'r') as f:
                    nodes = json.load(f)
                for k, v in nodes.items(): self.active_lattice[int(k)], self.manifest_count = v, max(
                    self.manifest_count, int(k))
                self.remanifest_grid()
            except:
                pass

    def save_scene_as(self, scene_name=None):
        if not scene_name: scene_name = simpledialog.askstring("SCENE_NAMING", "Enter Designation:")
        if not scene_name: return
        filename = f"portal_nodes_{scene_name.upper().replace(' ', '_')}.json"
        save_path = os.path.join(os.path.dirname(MASTER_JSON), filename)
        try:
            manifest = {str(k): v for k, v in self.active_lattice.items()}
            with open(save_path, 'w') as f:
                json.dump(manifest, f, indent=4)
            self.log_system(f"✅ SCENE_BURNED: {filename} latched to X9 Pro.")
        except Exception as e:
            self.log_system(f"❌ BURN_ERR: {e}")

    def clear_to_new_scene(self):
        self.active_lattice, self.manifest_count = {}, 0; self.remanifest_grid()

    def open_node_menu(self):
        ZenithNodeMenu(self, self.active_lattice)

    def log_system(self, msg, status="INFO"):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        display_msg = f"[{ts}] {status}: {msg}" if status != "INFO" else f"[{ts}] {msg}"
        self.system_box.insert(tk.END, f"{display_msg}\n")
        self.system_box.see(tk.END)

    def log_council(self, msg):
        self.council_box.insert(tk.END, f"{msg}\n\n"); self.council_box.see(tk.END)

    def toggle_mode(self):
        self.node_mode = not self.node_mode

    def launch_navigator(self):
        if os.path.exists(NAV_PATH):
            spec = importlib.util.spec_from_file_location("nav", NAV_PATH)
            m = importlib.util.module_from_spec(spec);
            spec.loader.exec_module(m)
            m.ZenithNavigator(self)


if __name__ == "__main__":
    ZenithOS().mainloop()