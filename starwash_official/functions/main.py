from firebase_functions import firestore_fn
from firebase_admin import initialize_app, firestore
from twilio.rest import Client
import os

# Initialize the Firebase Admin SDK
initialize_app()


@firestore_fn.on_document_created(
    document="starwash_bookings/{bookingId}",
    # These must match the secret names you set in your terminal
    secrets=["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE", "SON_PHONE"]
)
def handle_new_booking(event):
    """
    This function triggers automatically when a new document
    is added to the 'starwash_bookings' collection.
    """
    snapshot = event.data
    if not snapshot:
        print("No data found in the event.")
        return

    # Get the dictionary of data from the new document
    booking = snapshot.to_dict()
    db = firestore.client()

    # --- 1. THE FILTER ---
    # Only run for completed jobs done by 'solo_dad'
    status = booking.get('status')
    job_type = booking.get('job_type')

    if status != 'completed' or job_type != 'solo_dad':
        print(f"Skipping: Status is {status}, Job Type is {job_type}")
        return

    # --- 2. THE MATH ---
    try:
        # Ensure price is treated as a number
        price = float(booking.get('price', 0))
        expenses_due = 100.0  # Placeholder for your monthly deficit

        # Calculate 15% of the net proceeds (price minus half the deficit)
        cost_share = expenses_due * 0.50
        net_after_cost = price - cost_share
        growth_fund_cut = round(net_after_cost * 0.15, 2)

        # Safety check: don't allow a negative deposit
        if growth_fund_cut < 0:
            growth_fund_cut = 0

    except (ValueError, TypeError) as e:
        print(f"Math Error: Could not process price. Error: {e}")
        return

    # --- 3. THE NOTIFICATION (Twilio) ---
    try:
        # Pull secrets from the environment
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_num = os.environ.get('TWILIO_PHONE')
        son_num = os.environ.get('SON_PHONE')

        client = Client(account_sid, auth_token)

        msg_body = (
            f"⭐ STARWASH: New Job!\n"
            f"Customer: {booking.get('customerName', 'Client')}\n"
            f"Your Growth Fund: +${growth_fund_cut}\n"
            f"Cost Share: -${cost_share}"
        )

        client.messages.create(
            body=msg_body,
            from_=twilio_num,
            to=son_num
        )
        print("✅ Twilio text sent successfully.")
    except Exception as e:
        print(f"❌ Twilio Error: {e}")

    # --- 4. THE LEDGER (Firebase Update) ---
    try:
        # Log this specific deposit
        db.collection('growth_funds').document('son_ledger').collection('entries').add({
            'amount': growth_fund_cut,
            'customer': booking.get('customerName'),
            'type': 'automated_deposit',
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        # Update the running total balance
        db.collection('growth_funds').document('son_ledger').set({
            'total_balance': firestore.Increment(growth_fund_cut),
            'last_updated': firestore.SERVER_TIMESTAMP
        }, merge=True)

        print(f"✅ Ledger updated: +${growth_fund_cut}")
    except Exception as e:
        print(f"❌ Ledger Error: {e}")