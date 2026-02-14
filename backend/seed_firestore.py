"""
Firebase Firestore Seed Script
Populates the database with sample hospitals and initial data
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid

# Initialize Firebase Admin SDK
# You'll need to download the service account key from Firebase Console
# and save it as 'service-account-key.json'

try:
    cred = credentials.Certificate('service-account-key.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase initialization error: {e}")
    print("Make sure you have 'service-account-key.json' in the backend folder")
    exit(1)

db = firestore.client()

# Sample Hospitals Data
HOSPITALS = [
    {
        "id": str(uuid.uuid4()),
        "name": "Government General Hospital",
        "code": "GGH-001",
        "hospitalType": "Tertiary",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "address": "Park Town, Chennai - 600003",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "totalBeds": 500,
        "emergencyBeds": 50,
        "departments": [
            "General Medicine", "Emergency", "Cardiology", "Pulmonology",
            "Neurology", "Gastroenterology", "Orthopedics", "Surgery",
            "Dermatology", "ENT", "Ophthalmology", "Urology"
        ],
        "contactPhone": "+91-44-25305000",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "District Hospital Coimbatore",
        "code": "DHC-001",
        "hospitalType": "District",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "address": "Trichy Road, Coimbatore - 641018",
        "latitude": 11.0168,
        "longitude": 76.9558,
        "totalBeds": 300,
        "emergencyBeds": 30,
        "departments": [
            "General Medicine", "Emergency", "Cardiology", "Pulmonology",
            "Orthopedics", "Surgery", "Pediatrics", "Obstetrics & Gynecology"
        ],
        "contactPhone": "+91-422-2301234",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Primary Health Center Ambattur",
        "code": "PHC-001",
        "hospitalType": "PHC",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "address": "Ambattur Industrial Estate, Chennai - 600058",
        "latitude": 13.1143,
        "longitude": 80.1548,
        "totalBeds": 30,
        "emergencyBeds": 5,
        "departments": ["General Medicine", "Emergency", "Pediatrics"],
        "contactPhone": "+91-44-26574321",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Community Health Center Madurai",
        "code": "CHC-001",
        "hospitalType": "CHC",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "address": "Anna Nagar, Madurai - 625020",
        "latitude": 9.9252,
        "longitude": 78.1198,
        "totalBeds": 100,
        "emergencyBeds": 15,
        "departments": [
            "General Medicine", "Emergency", "Pediatrics",
            "Obstetrics & Gynecology", "Surgery"
        ],
        "contactPhone": "+91-452-2345678",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    },
    {
        "id": str(uuid.uuid4()),
        "name": "AIIMS Delhi",
        "code": "AIIMS-001",
        "hospitalType": "Tertiary",
        "district": "New Delhi",
        "state": "Delhi",
        "address": "Ansari Nagar, New Delhi - 110029",
        "latitude": 28.5672,
        "longitude": 77.2100,
        "totalBeds": 2500,
        "emergencyBeds": 200,
        "departments": [
            "General Medicine", "Emergency", "Cardiology", "Pulmonology",
            "Neurology", "Gastroenterology", "Orthopedics", "Surgery",
            "Dermatology", "ENT", "Ophthalmology", "Urology", "Oncology",
            "Nephrology", "Psychiatry", "Pediatrics"
        ],
        "contactPhone": "+91-11-26588500",
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    },
]

# Sample Doctors Data (will need Firebase Auth UIDs after registration)
SAMPLE_DOCTORS = [
    {
        "name": "Dr. Rajesh Kumar",
        "department": "Emergency",
        "specialization": "Emergency Medicine",
        "maxPatientsPerHour": 6,
    },
    {
        "name": "Dr. Priya Sharma",
        "department": "Cardiology",
        "specialization": "Interventional Cardiology",
        "maxPatientsPerHour": 4,
    },
    {
        "name": "Dr. Arun Patel",
        "department": "General Medicine",
        "specialization": "Internal Medicine",
        "maxPatientsPerHour": 5,
    },
    {
        "name": "Dr. Lakshmi Iyer",
        "department": "Neurology",
        "specialization": "Neurophysiology",
        "maxPatientsPerHour": 4,
    },
]


def seed_hospitals():
    """Add sample hospitals to Firestore"""
    print("\n📍 Seeding Hospitals...")

    for hospital in HOSPITALS:
        doc_ref = db.collection('hospitals').document(hospital['id'])
        doc_ref.set(hospital)
        print(f"  ✅ Added: {hospital['name']}")

    print(f"\n✅ Added {len(HOSPITALS)} hospitals")


def create_sample_outbreak_signals():
    """Create sample outbreak signals for testing"""
    print("\n🦠 Creating sample outbreak signals...")

    signals = [
        {
            "id": str(uuid.uuid4()),
            "region": "Chennai",
            "symptomCluster": ["fever", "cough", "breathlessness"],
            "caseCount": 45,
            "severity": "MEDIUM",
            "status": "active",
            "detectedAt": datetime.utcnow(),
            "description": "Respiratory illness cluster detected in Chennai urban area",
        },
        {
            "id": str(uuid.uuid4()),
            "region": "Coimbatore",
            "symptomCluster": ["fever", "diarrhea", "vomiting"],
            "caseCount": 28,
            "severity": "LOW",
            "status": "monitoring",
            "detectedAt": datetime.utcnow(),
            "description": "Gastroenteritis cases increasing in Coimbatore district",
        },
    ]

    for signal in signals:
        doc_ref = db.collection('outbreak_signals').document(signal['id'])
        doc_ref.set(signal)
        print(f"  ✅ Added outbreak signal: {signal['region']}")


def print_summary():
    """Print database summary"""
    print("\n" + "="*50)
    print("📊 DATABASE SEEDING COMPLETE")
    print("="*50)
    print(f"\nFirestore Collections Created:")
    print(f"  • hospitals: {len(HOSPITALS)} documents")
    print(f"  • outbreak_signals: 2 documents")
    print("\n📝 Next Steps:")
    print("  1. Users can now sign up through the app")
    print("  2. Patient data will be created on registration")
    print("  3. Doctors need to be registered by admin")
    print("\n🔗 Firebase Console: https://console.firebase.google.com/project/asclepius-f664c")


if __name__ == "__main__":
    print("🚀 SwasthyaFlow AI - Database Seeder")
    print("="*50)

    try:
        seed_hospitals()
        create_sample_outbreak_signals()
        print_summary()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

