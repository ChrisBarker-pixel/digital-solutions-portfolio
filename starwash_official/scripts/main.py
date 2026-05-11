import os
from firebase_functions import firestore_fn
from firebase_admin import initialize_app, firestore
from twilio.rest import Client

initialize_app()


@firestore_fn.on_document_created(
    document="starwash_bookings/{bookingId}",
    secrets=["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE", "SON_PHONE"]
)
def handle_new_booking(event):
    snapshot = event.data
    if not snapshot: return
    booking = snapshot.to_dict()
    db = firestore.client()

    status = booking.get('status')
    phone = booking.get('customerPhone')  # Captured from new form
    name = booking.get('customerName', 'Customer')

    # --- 1. NEW LEAD ALERT (The Ping) ---
    if status == 'pending':
        send_text(os.environ.get('SON_PHONE'),
                  f"🚿 STARWASH LEAD: {name} requested {booking.get('package')}. Phone: {phone}")
        return

    # --- 2. COMPLETION LOGIC (The Payout & Loyalty) ---
    if status == 'completed':
        # LOYALTY PROGRAM (5-and-1)
        loyalty_ref = db.collection('loyalty_programs').document(phone)
        loyalty_doc = loyalty_ref.get()
        count = (loyalty_doc.to_dict().get('wash_count', 0) if loyalty_doc.exists else 0) + 1

        reward_text = ""
        if count >= 5:
            loyalty_ref.set({'wash_count': 0, 'free_washes': firestore.Increment(1)}, merge=True)
            reward_text = "🎁 LOYALTY: 5th wash hit! Next one is FREE."
        else:
            loyalty_ref.set({'wash_count': count}, merge=True)
            reward_text = f"⭐ Loyalty: {count}/5."

        # GROWTH FUND (15% Math)
        price = float(booking.get('priceLocked', 0))
        growth_cut = round(price * 0.15, 2)

        db.collection('growth_funds').document('son_ledger').set({
            'total_balance': firestore.Increment(growth_cut)
        }, merge=True)

        # FINAL TEXT
        send_text(os.environ.get('SON_PHONE'),
                  f"💰 GROWTH FUND: +${growth_cut} from {name}. {reward_text}")


def send_text(to, body):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    client.messages.create(body=body, from_=os.environ.get('TWILIO_PHONE'), to=to)