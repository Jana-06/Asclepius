"""
Create a Firebase Auth user using the REST API (no service account needed)
This script creates a doctor user in Firebase Authentication.
"""
import requests
import json
import sys

# Firebase project config (from lib/firebase_options.dart)
API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'  # Android API key
PROJECT_ID = 'asclepius-f664c'

# Firebase Auth REST API endpoint
SIGNUP_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'

def create_doctor_auth_user(email: str, password: str):
    """Create a Firebase Auth user via REST API"""
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }

    params = {'key': API_KEY}

    print(f"Creating Firebase Auth user: {email}...")
    response = requests.post(SIGNUP_URL, json=payload, params=params)

    if response.status_code == 200:
        data = response.json()
        uid = data.get('localId')
        print(f"✅ Firebase Auth user created successfully!")
        print(f"   UID: {uid}")
        print(f"   Email: {email}")
        return uid
    else:
        error_data = response.json()
        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
        print(f"❌ Error creating user: {error_msg}")
        print(f"   Full response: {json.dumps(error_data, indent=2)}")
        return None

if __name__ == '__main__':
    email = 'dr.hackathon@example.com'
    password = 'Hack@2026'

    uid = create_doctor_auth_user(email, password)

    if uid:
        print(f"\n🔑 Use this UID for Firestore doctor document ID: {uid}")
    else:
        sys.exit(1)

