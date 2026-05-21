# =====================================================================
# ZENITH_OS // STANDALONE DATABASE SCHEMA LOCATOR INFRASTRUCTURE
# =====================================================================
import firebase_admin
from firebase_admin import credentials, db

# 1. Direct hardcoded credential anchor injection
db_url = "https://zenith-hub-2026-official-default-rtdb.firebaseio.com/"
cred_path = "/Volumes/X9 Pro/Zenith Rebuild Main/serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {"databaseURL": db_url})

print("SYSTEM: Analyzing live real-time network tree structures...")

try:
    root_ref = db.reference("/")
    snapshot = root_ref.get()
    
    if snapshot:
        print("\n📊 MATCHING KEYS DISCOVERED INSIDE YOUR FIREBASE TREE:")
        for key in snapshot.keys():
            print(f" └──  FOUND PATH: /{key}")
    else:
        print("\n⚠️ SYSTEM WARNING: Database is currently entirely blank.")
except Exception as e:
    print(f"\n❌ UNABLE TO QUERY LIVE DATABASE METRICS: {str(e)}")
