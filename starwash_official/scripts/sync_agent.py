import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURATION ---
# Replace with the actual name of your service account file
SERVICE_ACCOUNT_FILE = "zenith-hub-2026-official-firebase-adminsdk.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_calendar_service():
    creds = None
    # Token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


def sync_availability(user_id):
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    for event in events:
        if "UNAVAILABLE" in event.get('summary', '').upper():
            # Get the date (handles both all-day and timed events)
            start_date = event['start'].get('date') or event['start'].get('dateTime').split('T')[0]

            # Aligning with your Firestore screenshot fields
            doc_ref = db.collection('business_availability').document(user_id)
            doc_ref.set({
                'date': start_date,
                'status': 'unavailable',
                'user': user_id
            })
            print(f"✅ Node Synced: {user_id} is LOCKED for {start_date}")


if __name__ == '__main__':
    # You can run this for yourself.
    # For your son, you'd eventually run it with his calendar credentials.
    sync_availability('dad')