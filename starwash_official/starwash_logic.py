from twilio.rest import Client
from firebase_admin import credentials, firestore, initialize_app

# --- 1. SETTINGS ---
# Replace with your actual Twilio credentials from your Make.com setup
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE = '+15550005555'
SON_PHONE = '+15551234567'  # Your son's phone number

# --- 2. FIREBASE & TWILIO CLIENTS ---
# Uses the service account key you already have in the root
cred = credentials.Certificate("zenith-hub-2026-official-firebase-adminsdk.json")
initialize_app(cred)
db = firestore.client()
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def process_new_booking(doc_id):
    # Fetch the booking data
    doc_ref = db.collection('starwash_bookings').document(doc_id)
    booking = doc_ref.get().to_dict()

    if not booking:
        return

    name = booking.get('customerName')
    vehicle = booking.get('vehicle')
    price = booking.get('priceLocked', 0)

    # --- 3. THE 15% GROWTH FUND MATH ---
    # Since he is 16, this ledger keeps things transparent
    growth_fund_cut = round(price * 0.15, 2)

    # --- 4. SEND THE NOTIFICATION ---
    msg_body = (
        f"⭐ STARWASH ALERT\n"
        f"New Booking: {name}\n"
        f"Vehicle: {vehicle}\n"
        f"Your Growth Fund Cut: ${growth_fund_cut}\n"
        f"Check the Zenith Hub for details!"
    )

    message = twilio_client.messages.create(
        body=msg_body,
        from_=TWILIO_PHONE,
        to=SON_PHONE
    )

    print(f"✅ Notification sent to Son! SID: {message.sid}")

    # --- 5. LOG TO LEDGER ---
    # Update his personal ledger in Firebase
    db.collection('growth_funds').document('son_ledger').collection('entries').add({
        'booking_id': doc_id,
        'amount': growth_fund_cut,
        'date': booking.get('appointmentDate')
    })

# Run this test with a Document ID from your Firestore screenshot
# process_new_booking('eKP8rx...')firebase init functions