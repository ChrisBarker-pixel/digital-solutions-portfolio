
import shutil
import os

class InfrastructureSentry(OmniBase):
    def __init__(self, engine):
        super().__init__(engine)
        self.name = "InfraSentry_Lite_v1"
        self.id = 15
        self.hz = 396.0
        self.tag = "INFRA"
        self.announce_ignition()

    def execute(self, **kwargs):
        path = getattr(self.engine, 'ROOT_PATH', '/Volumes/X9 Pro/Zenith Rebuild Main/')

        try:
            # Check if the X9 Pro is physically there
            if not os.path.exists(path):
                return {"status": "OFFLINE", "error": "X9_PRO_NOT_FOUND"}

            # Storage Calculations using built-in shutil
            total, used, free = shutil.disk_usage(path)
            capacity_pct = (used / total) * 100

            return {
                "drive": "X9_PRO_5TB",
                "status": "OPTIMAL" if capacity_pct < 90 else "WARNING",
                "total_gb": total // (2**30),
                "used_gb": used // (2**30),
                "free_gb": free // (2**30),
                "capacity_usage": f"{capacity_pct:.2f}%"
            }
        except Exception as e:
            return {"status": "CRITICAL", "error": str(e)}
