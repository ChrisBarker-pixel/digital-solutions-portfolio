import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore


# --- 🛰️ THE CLOUD FOUNDRY ---
class CloudLattice:
    def __init__(self, cert_path, rtdb_url):
        self.cert_path = cert_path
        self.rtdb_url = rtdb_url
        self.fs = None
        self.connect()

    def connect(self):
        try:
            if os.path.exists(self.cert_path):
                if not firebase_admin._apps:
                    cred = credentials.Certificate(self.cert_path)
                    firebase_admin.initialize_app(cred)
                self.fs = firestore.client()
        except:
            pass


# --- 🧠 THE NAVIGATOR KERNEL (V2.1 SCROLL-LATCH) ---
class ZenithNavigator(tk.Toplevel):  # Changed to Toplevel for Master Core Handshake
    def __init__(self, parent=None):  # Added parent for Bi-Directional Latch
        if parent is None:
            # Standalone Boot Logic
            self.root = tk.Tk()
            super().__init__(self.root)
            self.parent = None
            self.active_lattice = {}
        else:
            # Master Core Latch Logic
            super().__init__(parent)
            self.parent = parent
            # Sync to the Master Core's actual RAM
            self.active_lattice = getattr(parent, 'active_lattice', {})

        self.title("ZENITH_NAV: BI-DIRECTIONAL_CLOUD_LATCH")
        self.geometry("1440x850")
        self.configure(bg="#050505")

        self.cert_path = "/Volumes/X9 Pro/Zenith Rebuild Main/vault/serviceAccountKey.json"
        self.rtdb_url = "https://zenith-hub-2026-official-default-rtdb.firebaseio.com/"

        # 🧪 STATE LATCHES
        self.ram_buffer = []
        self.fs_depth = []
        self.db_path = "/"
        self.ssd_path = "/Volumes/X9 Pro" if os.path.exists("/Volumes/X9 Pro") else os.path.expanduser("~")

        self.cloud = CloudLattice(self.cert_path, self.rtdb_url)
        self.setup_ui()

        if parent is None:
            self.root.withdraw()  # Hide the ghost root in standalone

    def setup_ui(self):
        self.master_f = tk.Frame(self, bg="#050505")
        self.master_f.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for i in range(4): self.master_f.columnconfigure(i, weight=1)

        self.pillars = {}
        disks = [("💾 SSD", "#00FFFF", "SSD"), ("🔥 FS", "#39FF14", "FS"),
                 ("🛰️ DB", "#00BFFF", "DB"), ("🧠 RAM", "#8B00FF", "RAM")]

        for i, (label, color, key) in enumerate(disks):
            pillar_f = tk.Frame(self.master_f, bg="#0a0a0a", highlightthickness=1, highlightbackground="#1a1a1a")
            pillar_f.grid(row=0, column=i, sticky="nsew", padx=4)

            # Header + Action Bar
            head = tk.Frame(pillar_f, bg="#0a0a0a")
            head.pack(fill=tk.X, pady=5)
            tk.Label(head, text=label, fg=color, bg="#0a0a0a", font=("Courier", 10, "bold")).pack()

            btn_f = tk.Frame(head, bg="#0a0a0a")
            btn_f.pack(fill=tk.X)

            if key != "RAM":
                tk.Button(btn_f, text="[ BACK ]", bg="#222", fg=color, font=("Courier", 7, "bold"),
                          command=lambda k=key: self.on_drill_up(None, k)).pack(side=tk.LEFT, padx=2, expand=True,
                                                                                fill=tk.X)
                tk.Button(btn_f, text="[ SYNC ]", bg="#333", fg="#000", font=("Courier", 7, "bold"),
                          command=lambda k=key: self.batch_sync(k)).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
            else:
                tk.Button(btn_f, text="[ CLEAR_RAM ]", bg="#FF3131", fg="#000", font=("Courier", 8, "bold"),
                          command=self.clear_ram).pack(fill=tk.X, padx=5)

            # TreeView (Linked to the Vertical Scroll Latch)
            container = tk.Frame(pillar_f, bg="#000")
            container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            scrollbar = ttk.Scrollbar(container, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree = ttk.Treeview(container, columns=("Name", "Path", "Type"), show="", height=25,
                                yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)

            tree.tag_configure('col', foreground=color)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.pillars[key] = tree

            tree.bind("<Double-1>", lambda e, k=key: self.on_double_click(e, k))
            self.refresh_pillar(key)

    def refresh_pillar(self, key):
        tree = self.pillars[key]
        tree.delete(*tree.get_children())

        if key == "SSD" and os.path.exists(self.ssd_path):
            try:
                for item in sorted(os.listdir(self.ssd_path)):
                    if item.startswith('.'): continue
                    full = os.path.join(self.ssd_path, item)

                    # 🛡️ THE BLUEPRINT FILTER
                    if os.path.isfile(full):
                        if not item.endswith('.json') or not self.is_zenith_scene(full):
                            continue  # Hide configs, firebase.json, etc.

                    itype = "DIR" if os.path.isdir(full) else "FILE"
                    tree.insert("", tk.END, values=(item, full, itype), tags=('col',))
            except:
                pass

    def is_zenith_scene(self, path):
        """🔍 Peeks at the file to see if it holds Node IDs."""
        try:
            with open(path, 'r') as f:
                content = f.read(200)  # Only read the start for speed
                import re
                # Matches patterns like "1": or '16': at the start of the JSON
                return bool(re.search(r'["\']\d+["\']\s*:', content))
        except:
            return False

    def on_double_click(self, event, key):
        tree = self.pillars[key]
        sel = tree.selection()
        if not sel: return
        name, path, itype = tree.item(sel[0])['values']

        if key == "RAM":
            if self.parent:
                from __main__ import NodeEditor
                # Ensure the path (ID) exists in the parent lattice before calling
                node_id = int(path)
                if node_id in self.parent.active_lattice:
                    NodeEditor(self.parent, node_id, self.parent.active_lattice[node_id])
        elif itype in ["DIR", "COL", "KEY"]:
            if key == "SSD":
                self.ssd_path = path
            elif key == "FS":
                self.fs_depth.append(name)
            elif key == "DB":
                self.db_path = f"{path}/"
            self.refresh_pillar(key)
        else:
            # 🛰️ THIS IS THE TRIGGER
            self.add_to_ram(name, path, key)
            if self.parent:
                self.parent.remanifest_grid()  # Force-draw the scene

    def add_to_ram(self, name, path, origin):
        """🛰️ HARDENED_LATCH: Sanitizes and Rehydrates Node Manifests."""
        if self.parent and origin == "SSD" and path.endswith(".json"):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    raw_content = f.read().strip()

                # 🛡️ THE SANITIZER: Handles empty files and potential corruption
                if not raw_content:
                    raise ValueError("File is empty.")

                try:
                    data = json.loads(raw_content)
                except json.JSONDecodeError:
                    # Attempt a "Soft Repair" for single quotes if strict JSON fails
                    import ast
                    data = ast.literal_eval(raw_content)
                    self.parent.log_system("⚠️ REPAIR: Handled non-standard JSON syntax.", "WARNING")

                # 🧬 SCHEMA VALIDATION
                if isinstance(data, dict) and any(k.isdigit() for k in data.keys()):
                    self.parent.log_system(f"🌀 REHYDRATING: {name}...", "ZENITH")

                    # Atomic Update: Clear and Inject
                    self.parent.active_lattice.clear()
                    for k, v in data.items():
                        if k.isdigit():
                            self.parent.active_lattice[int(k)] = v

                    self.parent.remanifest_grid()
                    self.parent.log_system("✅ LATCH_SUCCESS.", "SUCCESS")
                else:
                    self.parent.log_system(f"📜 CONFIG: Opening {name} in Editor.", "INFO")
                    self.open_editor(name, path, origin)

            except Exception as e:
                self.parent.log_system(f"❌ LATCH_ERR: {e}", "DANGER")

    def on_drill_up(self, event, key):
        if key == "SSD":
            self.ssd_path = os.path.dirname(self.ssd_path)
        elif key == "FS" and self.fs_depth:
            self.fs_depth.pop()
        elif key == "DB" and self.db_path != "/":
            parts = self.db_path.strip("/").split("/")
            self.db_path = "/" + "/".join(parts[:-1]) + "/" if len(parts) > 1 else "/"
        self.refresh_pillar(key)



    def batch_sync(self, key):
        """🔥 MASS_REHYDRATION: Latches all pillar nodes to the Master grid."""
        tree = self.pillars[key]
        for item_id in tree.get_children():
            name, path, itype = tree.item(item_id)['values']
            # Ignore directories and collections; only sync files/docs
            if itype not in ["DIR", "COL", "KEY"]:
                self.add_to_ram(name, path, key)

        # After the batch, force the grid to redraw
        if self.parent:
            self.parent.remanifest_grid()

    def clear_ram(self):
        self.ram_buffer = []
        self.refresh_pillar("RAM")

    def open_editor(self, label, path, origin):
        win = tk.Toplevel(self)
        win.title(f"NODE_EDITOR: {label}")
        win.geometry("800x600")
        txt = scrolledtext.ScrolledText(win, bg="#000", fg="#00BFFF", font=("Courier", 11), insertbackground="white")
        txt.pack(fill=tk.BOTH, expand=True)
        try:
            payload = ""
            if origin == "SSD":
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    payload = f.read()
            elif origin == "DB":
                r = requests.get(f"{self.rtdb_url}{path}.json");
                payload = json.dumps(r.json(), indent=4)
            elif origin == "FS":
                doc = self.cloud.fs.collection(self.fs_depth[-1]).document(path).get()
                payload = json.dumps(doc.to_dict(), indent=4)
            txt.insert(tk.END, payload if payload else "// VOID_PAYLOAD")
        except Exception as e:
            txt.insert(tk.END, f"// LATCH_ERROR: {e}")


if __name__ == "__main__":
    app = ZenithNavigator()
    app.mainloop()