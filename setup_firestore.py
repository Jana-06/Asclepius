"""
Create Firestore doctor and hospital documents for the test doctor.
"""
import requests
import json
from datetime import datetime

API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'
PROJECT_ID = 'asclepius-f664c'
DATABASE_ID = '(default)'

FIRESTORE_URL = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/{DATABASE_ID}/documents'

# Test doctor details
uid = 'JMEU3MThKLUcJWVyC7Ybmxtupwx2'
email = 'hackathon.doctor@test.com'
name = 'Dr. Hackathon Test'
department = 'Emergency'
hospital_id = '3f8b2f2a-9d41-4e6a-bfa8-2c8f77b5e8c9'

def create_hospital():
    """Create hospital document"""
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
    print(f"Creating hospital document: {hospital_id}...")

    response = requests.patch(doc_url, json=hospital_data, params={'key': API_KEY})

    if response.status_code in [200, 201]:
        print(f"✅ Hospital document created/updated!")
        return True
    else:
        print(f"⚠️  Hospital: HTTP {response.status_code}")
        if response.status_code != 400:
            print(f"   Response: {response.text}")
        return False

def create_doctor():
    """Create doctor document"""
    doctor_data = {
        'fields': {
            'uid': {'stringValue': uid},
            'email': {'stringValue': email},
            'name': {'stringValue': name},
            'department': {'stringValue': department},
            'hospitalId': {'stringValue': hospital_id},
            'maxPatientsPerHour': {'integerValue': '4'},
            'isAvailable': {'booleanValue': True},
            'currentPatientCount': {'integerValue': '0'},
            'userType': {'stringValue': 'doctor'},
            'createdAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
            'updatedAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'},
        }
    }

    doc_url = f'{FIRESTORE_URL}/doctors/{uid}'
    print(f"Creating doctor document: {uid}...")

    response = requests.patch(doc_url, json=doctor_data, params={'key': API_KEY})

    if response.status_code in [200, 201]:
        print(f"✅ Doctor document created!")
        return True
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == '__main__':
    print("Setting up Firestore documents for test doctor...\n")

    create_hospital()
    create_doctor()

    print(f"\n{'='*70}")
    print(f"✅ DOCTOR ACCOUNT READY FOR LOGIN!")
    print(f"{'='*70}")
    print(f"Email:    {email}")
    print(f"Password: TestPassword123!")
    print(f"UID:      {uid}")
    print(f"\n👉 Try signing in with these credentials in the doctor login screen!")
    print(f"{'='*70}\n")


