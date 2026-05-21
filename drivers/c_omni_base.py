
import json
import os
import threading
from datetime import datetime

class OmniBase:
    def __init__(self, engine):
        self.engine = engine
        self.name = "OMNI_CORE_v6"
        self.root = engine.ROOT_PATH
        self.scenes_path = os.path.join(self.root, "scenes")
        self.db_base_url = "https://zenith-hub-2026-official-default-rtdb.firebaseio.com/directives/scenes"

    def announce_ignition(self):
        self.log_to_engine(f"💎 {self.name.upper()}: ONLINE", "SUCCESS")

    def log_to_engine(self, message, status="INFO"):
        if hasattr(self.engine, 'update_cmd'):
            self.engine.update_cmd(message, status)
        else:
            print(f"[{status}] {message}")

    def force_grid_refresh(self):
        if hasattr(self.engine, 'whiteboard'):
            self.log_to_engine("📐 SPATIAL_OS: Recalculating grid alignment...", "INFO")
            self.engine.force_canvas_sync()

    def update_node_state(self, node_id, payload):
        scene_name = getattr(self.engine, 'active_scene_name', 'OMNI_BASE')
        local_file = os.path.join(self.scenes_path, f"{scene_name}.json")
        try:
            if not os.path.exists(self.scenes_path):
                os.makedirs(self.scenes_path, exist_ok=True)
            self.engine.entities = [n for n in self.engine.entities if str(n.get('id')) != str(node_id)]
            self.engine.entities.append(payload)
            with open(local_file, 'w', encoding="utf-8") as f:
                json.dump({"nodes": self.engine.entities, "scene": scene_name}, f, indent=4)
            def cloud_sync():
                if hasattr(self.engine, 'FIREBASE_READY'):
                    from firebase_admin import db
                    ref = db.reference(f'directives/scenes/{scene_name}/{node_id}')
                    ref.set(payload)
            threading.Thread(target=cloud_sync, daemon=True).start()
            self.force_grid_refresh()
            self.log_to_engine(f"✅ HARMONIC_LATCH: Node {node_id} mirrored.", "SUCCESS")
            return True
        except Exception as e:
            self.log_to_engine(f'🚨 DNA_CRASH: {str(e)}', 'DANGER')
            return False

    def apply_lattice_tension(self, node_id):
        for node in self.engine.entities:
            if str(node.get('id')) == str(node_id):
                node['physics'] = {'mass': 1.0, 'tension': 0.8}
                self.log_to_engine(f"🧬 PHYSICS: Node_{node_id} weighted.", "INFO")
