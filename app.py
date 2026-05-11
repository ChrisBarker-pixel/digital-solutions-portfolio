from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)


# 🛰️ MASTER CLOUD LATCH
def get_db():
    cert_path = "/vault/serviceAccountKey.json"
    if not firebase_admin._apps:
        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


@app.route('/')
def index():
    try:
        db = get_db()
        # 🎯 TARGETING THE SCREENSHOT COLLECTION
        docs = db.collection('starwash').stream()
        packages = []

        for doc in docs:
            p = doc.to_dict()
            # Ensure keys match index.html: 'package' and 'price'
            packages.append({
                "package": p.get('package', 'Unknown'),
                "price": p.get('price', '0'),
                "id": doc.id
            })

        # 🛰️ HEARTBEAT: Check terminal to see if data exists
        print(f"--- 🛰️ STARWASH_SYNC: Found {len(packages)} Packages ---")
        for p in packages: print(f"  - {p['package']}: ${p['price']}")

        return render_template('index.html', packages=packages)
    except Exception as e:
        print(f"❌ KERNEL_ERROR: {e}")
        return f"System Offline: {str(e)}"


@app.route('/strike', methods=['POST'])
def handle_strike():
    db = get_db()
    data = request.json
    db.collection('orders').add({
        "package": data.get('package'),
        "timestamp": firestore.SERVER_TIMESTAMP,
        "status": "PENDING"
    })
    return jsonify({"status": "SUCCESS"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)