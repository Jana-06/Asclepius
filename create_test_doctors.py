"""
Fix the original test doctor account and create backup test doctors
"""
import requests
import json
from datetime import datetime

API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'
PROJECT_ID = 'asclepius-f664c'

SIGNUP_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'
FIRESTORE_URL = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents'

# Test doctors - EASY credentials for testing
TEST_DOCTORS = [
    {
        'email': 'test.doctor@test.com',
        'password': 'Test123456!',
        'name': 'Dr. Test',
        'department': 'Emergency',
        'specialization': 'Emergency Medicine',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'demo.doctor@test.com',
        'password': 'Demo123456!',
        'name': 'Dr. Demo',
        'department': 'General Medicine',
        'specialization': 'Internal Medicine',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
]

def create_firebase_auth_user(email: str, password: str) -> str:
    """Create Firebase Auth user and return UID"""
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }
    params = {'key': API_KEY}

    response = requests.post(SIGNUP_URL, json=payload, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('localId')
    else:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        if error_msg == 'EMAIL_EXISTS':
            print(f"  ℹ️  Email already exists: {email}")
            return None
        print(f"  ❌ Error: {error_msg}")
        return None


def create_firestore_doctor_doc(uid: str, doctor_info: dict) -> bool:
    """Create doctor document in Firestore"""
    doctor_data = {
        'fields': {
            'uid': {'stringValue': uid},
            'email': {'stringValue': doctor_info['email']},
            'name': {'stringValue': doctor_info['name']},
            'department': {'stringValue': doctor_info['department']},
            'specialization': {'stringValue': doctor_info.get('specialization', '')},
            'hospitalId': {'stringValue': doctor_info['hospitalId']},
            'maxPatientsPerHour': {'integerValue': '5'},
            'isAvailable': {'booleanValue': True},
            'currentPatientCount': {'integerValue': '0'},
            'userType': {'stringValue': 'doctor'},
            'createdAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
            'updatedAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
        }
    }

    doc_url = f'{FIRESTORE_URL}/doctors/{uid}'
    params = {'key': API_KEY}

    response = requests.patch(doc_url, json=doctor_data, params=params)

    return response.status_code in [200, 201]


def main():
    print("\n" + "="*70)
    print("🏥 CREATING TEST DOCTOR ACCOUNTS")
    print("="*70 + "\n")

    created_count = 0

    for doctor in TEST_DOCTORS:
        print(f"Creating: {doctor['name']}")

        uid = create_firebase_auth_user(doctor['email'], doctor['password'])

        if uid is None:
            print(f"  Skipped\n")
            continue

        if create_firestore_doctor_doc(uid, doctor):
            print(f"  ✅ Success!")
            print(f"     Email: {doctor['email']}")
            print(f"     Password: {doctor['password']}")
            created_count += 1

        print()

    print("="*70)
    print("🔑 EASY TEST CREDENTIALS (Copy & Paste Ready)")
    print("="*70 + "\n")

    print("Test Doctor 1:")
    print("  Email: test.doctor@test.com")
    print("  Password: Test123456!\n")

    print("Test Doctor 2:")
    print("  Email: demo.doctor@test.com")
    print("  Password: Demo123456!\n")

    print("Plus 8 Professional Doctors (from previous setup)")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

