"""
Get Firebase Auth user details and create Firestore doctor document.
Uses Firebase REST APIs (no service account needed).
"""
import requests
import json
import sys
from datetime import datetime

# Firebase config
API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'  # Android API key
PROJECT_ID = 'asclepius-f664c'
DATABASE_ID = '(default)'

# Firebase Auth REST API
SIGNIN_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'

# Firebase Firestore REST API
FIRESTORE_URL = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DATABASE_ID}/documents'

def get_firebase_uid(email: str, password: str):
    """Get UID by signing in with email/password"""
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }

    params = {'key': API_KEY}

    print(f"Getting UID for {email}...")
    response = requests.post(SIGNIN_URL, json=payload, params=params)

    if response.status_code == 200:
        data = response.json()
        uid = data.get('localId')
        print(f"✅ UID found: {uid}")
        return uid
    else:
        error_data = response.json()
        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
        print(f"❌ Error: {error_msg}")
        return None

def create_firestore_doctor_doc(uid: str, email: str, name: str, department: str, hospital_id: str):
    """Create a doctor document in Firestore"""

    # Doctor document data
    doctor_data = {
        'fields': {
            'uid': {'stringValue': uid},
            'email': {'stringValue': email},
            'name': {'stringValue': name},
            'department': {'stringValue': department},
            'hospitalId': {'stringValue': hospital_id},
            'specialization': {'nullValue': True},
            'licenseNumber': {'nullValue': True},
            'maxPatientsPerHour': {'integerValue': '4'},
            'isAvailable': {'booleanValue': True},
            'currentPatientCount': {'integerValue': '0'},
            'userType': {'stringValue': 'doctor'},
            'createdAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
            'updatedAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
        }
    }

    # Create or update the doctor document
    doc_url = f'{FIRESTORE_URL}/doctors/{uid}'

    print(f"\nCreating Firestore doctor document...")
    print(f"  URL: {doc_url}")
    print(f"  Document ID: {uid}")

    response = requests.patch(doc_url, json=doctor_data, params={'key': API_KEY})

    if response.status_code in [200, 201]:
        print(f"✅ Doctor document created successfully!")
        print(f"   Collection: doctors")
        print(f"   Document ID: {uid}")
        print(f"   Name: {name}")
        print(f"   Department: {department}")
        print(f"   HospitalId: {hospital_id}")
        return True
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def create_firestore_hospital_doc(hospital_id: str):
    """Create a sample hospital document if it doesn't exist"""

    hospital_data = {
        'fields': {
            'name': {'stringValue': 'Government General Hospital'},
            'code': {'stringValue': 'GGH-001'},
            'hospitalType': {'stringValue': 'Tertiary'},
            'district': {'stringValue': 'Chennai'},
            'state': {'stringValue': 'Tamil Nadu'},
            'address': {'stringValue': 'Park Town, Chennai - 600003'},
            'totalBeds': {'integerValue': '500'},
            'emergencyBeds': {'integerValue': '50'},
            'departments': {'arrayValue': {'values': [
                {'stringValue': 'General Medicine'},
                {'stringValue': 'Emergency'},
                {'stringValue': 'Cardiology'},
            ]}},
            'contactPhone': {'stringValue': '+91-44-25305000'},
            'isActive': {'booleanValue': True},
            'createdAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
        }
    }

    doc_url = f'{FIRESTORE_URL}/hospitals/{hospital_id}'

    print(f"\nCreating Firestore hospital document...")
    print(f"  Document ID: {hospital_id}")

    response = requests.patch(doc_url, json=hospital_data, params={'key': API_KEY})

    if response.status_code in [200, 201]:
        print(f"✅ Hospital document created successfully!")
        return True
    else:
        print(f"⚠️  Could not create hospital (may already exist): HTTP {response.status_code}")
        return False

if __name__ == '__main__':
    email = 'dr.hackathon@example.com'
    password = 'Hack@2026'
    name = 'Dr. Hackathon'
    department = 'Emergency'
    hospital_id = '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9'

    # Step 1: Get UID
    uid = get_firebase_uid(email, password)
    if not uid:
        print("Failed to get UID. Exiting.")
        sys.exit(1)

    # Step 2: Create hospital doc
    create_firestore_hospital_doc(hospital_id)

    # Step 3: Create doctor doc
    success = create_firestore_doctor_doc(uid, email, name, department, hospital_id)

    if success:
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS! Doctor account is ready for login!")
        print(f"{'='*60}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"UID: {uid}")
        print(f"\nTry signing in to the doctor app now!")
    else:
        sys.exit(1)

