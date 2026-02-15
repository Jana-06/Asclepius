"""
Add Multiple Doctors to Firebase Authentication and Firestore
"""
import requests
import json
from datetime import datetime

# Firebase config
API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'
PROJECT_ID = 'asclepius-f664c'

SIGNUP_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'
FIRESTORE_URL = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents'

# Sample doctors to add
DOCTORS = [
    {
        'email': 'dr.rajesh.emergency@hospital.com',
        'password': 'EmergencyDoctor123!',
        'name': 'Dr. Rajesh Kumar',
        'department': 'Emergency',
        'specialization': 'Emergency Medicine',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.priya.cardiology@hospital.com',
        'password': 'CardiologyDoc456!',
        'name': 'Dr. Priya Sharma',
        'department': 'Cardiology',
        'specialization': 'Interventional Cardiology',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.arun.general@hospital.com',
        'password': 'GeneralMed789!',
        'name': 'Dr. Arun Patel',
        'department': 'General Medicine',
        'specialization': 'Internal Medicine',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.lakshmi.neuro@hospital.com',
        'password': 'Neurology321!',
        'name': 'Dr. Lakshmi Iyer',
        'department': 'Neurology',
        'specialization': 'Neurophysiology',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.suresh.gastro@hospital.com',
        'password': 'Gastroenterology!',
        'name': 'Dr. Suresh Kumar',
        'department': 'Gastroenterology',
        'specialization': 'GI Surgery',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.meera.orthopedic@hospital.com',
        'password': 'Orthopedic456!',
        'name': 'Dr. Meera Singh',
        'department': 'Orthopedics',
        'specialization': 'Sports Medicine',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.vikram.surgery@hospital.com',
        'password': 'Surgery789!',
        'name': 'Dr. Vikram Gupta',
        'department': 'Surgery',
        'specialization': 'General Surgery',
        'hospitalId': '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9',
    },
    {
        'email': 'dr.neha.pediatrics@hospital.com',
        'password': 'Pediatrics123!',
        'name': 'Dr. Neha Verma',
        'department': 'Pediatrics',
        'specialization': 'Neonatology',
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
            print(f"  ⚠️  Email already exists: {email}")
            return None
        print(f"  ❌ Error creating user: {error_msg}")
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

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  ❌ Firestore error: HTTP {response.status_code}")
        return False


def main():
    print("\n" + "="*70)
    print("🏥 ADDING DOCTORS TO FIREBASE")
    print("="*70 + "\n")

    created_count = 0
    skipped_count = 0
    failed_count = 0

    for doctor in DOCTORS:
        print(f"Creating doctor: {doctor['name']}")

        # Create Auth user
        uid = create_firebase_auth_user(doctor['email'], doctor['password'])

        if uid is None:
            skipped_count += 1
            print()
            continue

        # Create Firestore document
        if create_firestore_doctor_doc(uid, doctor):
            print(f"  ✅ Doctor created successfully!")
            print(f"     UID: {uid}")
            print(f"     Email: {doctor['email']}")
            print(f"     Department: {doctor['department']}")
            created_count += 1
        else:
            print(f"  ❌ Failed to create Firestore document")
            failed_count += 1

        print()

    print("="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"✅ Successfully created: {created_count}")
    print(f"⚠️  Skipped (already exist): {skipped_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📋 Total doctors: {len(DOCTORS)}")
    print("="*70 + "\n")

    if created_count > 0:
        print("🔑 LOGIN CREDENTIALS FOR DOCTORS:")
        print("-" * 70)
        for i, doctor in enumerate(DOCTORS, 1):
            print(f"\n{i}. {doctor['name']}")
            print(f"   Email: {doctor['email']}")
            print(f"   Password: {doctor['password']}")
            print(f"   Department: {doctor['department']}")


if __name__ == '__main__':
    main()

