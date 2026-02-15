"""
Utility to create a doctor user in Firebase Authentication and add a doctor document in Firestore.

Usage:
  python create_doctor_account.py --email doctor@example.com --password "StrongP@ssw0rd" --name "Dr. Test" --department Emergency

Notes:
- Requires Firebase Admin SDK and a service account JSON file named 'service-account-key.json' in the backend folder, or set GOOGLE_APPLICATION_CREDENTIALS to point to a service account key.
- If service account isn't available this script will exit with clear instructions.
"""
import argparse
import sys
import os
from datetime import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, auth, firestore
except Exception as e:
    print("Missing firebase_admin SDK. Install with: pip install firebase-admin")
    raise

SERVICE_ACCOUNT = 'service-account-key.json'


def init_firebase():
    # Prefer GOOGLE_APPLICATION_CREDENTIALS env var if set
    key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or SERVICE_ACCOUNT
    if not os.path.exists(key_path):
        print(f"Service account key not found at '{key_path}'.")
        print("Place the Firebase service account JSON in the backend folder named 'service-account-key.json' or set GOOGLE_APPLICATION_CREDENTIALS to its path.")
        sys.exit(1)

    cred = credentials.Certificate(key_path)
    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        # Already initialized
        pass


def create_doctor(email: str, password: str, name: str, department: str):
    init_firebase()
    user = auth.create_user(email=email, password=password, display_name=name)
    print(f"Created Firebase Auth user: uid={user.uid}")

    db = firestore.client()
    doc_ref = db.collection('doctors').document(user.uid)
    doc_ref.set({
        'name': name,
        'email': email,
        'department': department,
        'created_at': datetime.utcnow(),
        'role': 'doctor',
        'availability': True,
        'maxPatientsPerHour': 5
    })
    print(f"Created Firestore doctor document with id={user.uid}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create doctor account in Firebase')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--department', default='General Medicine')
    args = parser.parse_args()

    create_doctor(args.email, args.password, args.name, args.department)

