import firebase_admin
from firebase_admin import credentials, firestore

# 1. Setup Connection to the Grid
# Ensure your serviceAccountKey.json is in your project folder
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def monitor_testimonials():
    print("🛰️ TESTIMONIAL JUDGE ONLINE // STANDING BY FOR TRANSMISSIONS...")

    # Create a query to watch for unverified reviews
    reviews_ref = db.collection('starwash_testimonials').where('verified', '==', False)

    # Function to handle the incoming data
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                doc = change.document
                data = doc.to_dict()

                print("\n" + "=" * 40)
                print(f"⭐ NEW TESTIMONIAL DETECTED")
                print(f"👤 CLIENT: {data.get('name')}")
                print(f"🌟 RATING: {data.get('rating')} Stars")
                print(f"💬 MESSAGE: {data.get('text')}")
                print("=" * 40)

                choice = input("APPROVE FOR LIVE SITE? (y/n/skip): ").lower()

                if choice == 'y':
                    doc.reference.update({'verified': True})
                    print("✅ SIGNAL VERIFIED // PUSHED TO LIVE GRID")
                elif choice == 'n':
                    doc.reference.delete()
                    print("🗑️ SIGNAL PURGED // DISCARDED")
                else:
                    print("⏭️ REMAINING IN PENDING QUEUE")

    # Watch the collection in real-time
    reviews_ref.on_snapshot(on_snapshot)

    # Keep the script running
    import time
    while True:
        time.sleep(1)


if __name__ == "__main__":
    monitor_testimonials()