import tkinter as tk
from tkinter import ttk, messagebox


class ZenithNodeMenu(tk.Toplevel):
    """
    VISUAL_ENGINE // LATTICE_INDEX_V2.2
    PATCH_NOTES:
    1. Enabled vertical scrolling for high-density clusters.
    2. Added TRASH/DELETE functionality via Right-Click logic.
    """

    def __init__(self, parent=None, nodes_dict=None, editor_callback=None):
        if parent is None:
            self.root = tk.Tk()
            super().__init__(self.root)
        else:
            super().__init__(parent)

        self.parent = parent
        self.title("ZENITH_LATTICE_INDEX // MASTER_ACTIVE")
        self.geometry("700x750")
        self.configure(bg="#050505")

        # Default Data / Fallback for Standalone Testing
        self.nodes = nodes_dict if nodes_dict is not None else {
            i: {"title": f"NODE_{i:03d}", "logic": "READY_FOR_LOGIC_INJECTION"}
            for i in range(1, 14)
        }
        self.editor_callback = editor_callback

        self.setup_styles()
        self.setup_header()
        self.setup_search()
        self.setup_treeview()
        self.setup_context_menu()  # 🗑️ TRASH LATCH
        self.populate_index()

        self.attributes('-topmost', True)
        if parent is None:
            self.root.withdraw()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#000", foreground="#39FF14",
                        fieldbackground="#000", font=("Courier", 10),
                        rowheight=38, borderwidth=0)
        style.map("Treeview",
                  background=[('selected', '#1A1A1A')],
                  foreground=[('selected', '#00FFFF')])
        style.configure("Treeview.Heading",
                        background="#111", foreground="#00FFFF",
                        font=("Courier", 11, "bold"))

        style.configure("Vertical.TScrollbar", gripcount=0, background="#111",
                        darkcolor="#000", lightcolor="#111", bordercolor="#111",
                        troughcolor="#050505")

    def setup_header(self):
        header = tk.Frame(self, bg="#111", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="ZENITH_LATTICE_INDEX // MASTER",
                 fg="#00FFFF", bg="#111", font=("Courier", 14, "bold")).pack(side=tk.LEFT, padx=25)
        tk.Label(header, text="V2.2_TRASH_ENABLED",
                 fg="#FF3131", bg="#111", font=("Courier", 8)).pack(side=tk.RIGHT, padx=10)

    def setup_search(self):
        search_f = tk.Frame(self, bg="#050505", pady=10)
        search_f.pack(fill=tk.X, padx=20)
        tk.Label(search_f, text="SEARCH_LOGIC >>",
                 fg="#8B00FF", bg="#050505", font=("Courier", 10, "bold")).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_index)
        self.entry = tk.Entry(search_f, textvariable=self.search_var, bg="#111", fg="white",
                              font=("Courier", 11), insertbackground="#39FF14", bd=0)
        self.entry.pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True)

    def setup_treeview(self):
        container = tk.Frame(self, bg="#000")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.v_scroll = ttk.Scrollbar(container, orient="vertical")
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(container, columns=("ID", "Label", "Logic"),
                                 show="headings", yscrollcommand=self.v_scroll.set)

        self.v_scroll.config(command=self.tree.yview)

        self.tree.heading("ID", text="CODE")
        self.tree.column("ID", width=70, anchor="center")
        self.tree.heading("Label", text="TITLE/TAG")
        self.tree.column("Label", width=180)
        self.tree.heading("Logic", text="PAYLOAD_PREVIEW")
        self.tree.column("Logic", width=300)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<MouseWheel>", self.on_mousewheel)
        # Bind for Windows/Linux (Button-3) and macOS (Button-2)
        self.tree.bind("<Button-2>", self.show_context_menu)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def setup_context_menu(self):
        """Creates the Trash/Delete context menu."""
        self.context_menu = tk.Menu(self, tearoff=0, bg="#111", fg="#FF3131", font=("Courier", 10))
        self.context_menu.add_command(label="🗑️ TRASH_NODE", command=self.delete_node)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⚡ OPEN_EDITOR", command=self.on_double_click)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def populate_index(self, filter_text=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        sorted_nodes = sorted(self.nodes.items())
        for n_id, data in sorted_nodes:
            title = data.get('title', 'UNTITLED')
            logic = data.get('logic', '')
            snippet = logic.replace('\n', ' ')[:50] + "..." if len(logic) > 50 else logic

            if filter_text.lower() in title.lower() or filter_text.lower() in logic.lower():
                self.tree.insert("", tk.END, values=(f"{n_id:03d}", title, snippet))

    def filter_index(self, *args):
        self.populate_index(self.search_var.get())

    def on_mousewheel(self, event):
        self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def delete_node(self):
        """Removes the node from the RAM lattice and the UI."""
        selection = self.tree.selection()
        if not selection: return

        item = selection[0]
        node_id = int(self.tree.item(item)['values'][0])

        confirm = messagebox.askyesno("CONFIRM_TRASH", f"Are you sure you want to delete NODE_{node_id:03d}?")
        if confirm:
            if node_id in self.nodes:
                del self.nodes[node_id]  # Wipe from dictionary

            # If launched from ZenithOS, trigger grid refresh
            if self.parent and hasattr(self.parent, 'remanifest_grid'):
                self.parent.remanifest_grid()

            self.populate_index(self.search_var.get())  # Refresh UI list

    def on_double_click(self, event=None):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            node_id_str = self.tree.item(item)['values'][0]
            node_id = int(node_id_str)
            if self.editor_callback:
                self.editor_callback(node_id)
            else:
                print(f"DEBUG: Latched to Node {node_id} (Standalone Mode)")
            self.destroy()


if __name__ == "__main__":
    app = ZenithNodeMenu()
    app.mainloop()