import os
import json
import importlib
import sys

# 🎯 CONFIGURATION
scene_path = "/Volumes/X9 Pro/Zenith Rebuild Main/scene.json"
project_root = "/Volumes/X9 Pro/Zenith Rebuild Main"

def check_zenith_lattice():
    print("\n--- 🛰️ ZENITH OS: PRE-FLIGHT DIAGNOSTIC ---")
    
    # 1. Check Scene Persistence
    if not os.path.exists(scene_path):
        print("❌ FAIL: scene.json missing from X9 Pro.")
        return
    
    with open(scene_path, 'r') as f:
        try:
            scene_data = json.load(f)
            print(f"✅ SUCCESS: Loaded Scene '{scene_data.get('scene_name')}'")
        except Exception as e:
            print(f"❌ FAIL: scene.json is corrupt - {e}")
            return

    # 2. Check Module Integrity
    if project_root not in sys.path: 
        sys.path.insert(0, project_root)

    for node in scene_data.get('nodes', []):
        slot = node.get('slot')
        module_name = node.get('module')
        class_name = node.get('class')
        
        print(f"\n[NODE_{slot}]: Checking {node.get('id')}...")
        
        file_path = os.path.join(project_root, f"{module_name}.py")
        if os.path.exists(file_path):
            print(f"  - File found: {module_name}.py")
            try:
                mod = importlib.import_module(module_name)
                if hasattr(mod, class_name):
                    print(f"  - ✅ Class '{class_name}' verified.")
                else:
                    print(f"  - ❌ FAIL: Class '{class_name}' not in file.")
            except Exception as e:
                print(f"  - ❌ IMPORT_ERR: {e}")
        else:
            print(f"  - ❌ FAIL: {module_name}.py missing.")

if __name__ == "__main__":
    check_zenith_lattice()
