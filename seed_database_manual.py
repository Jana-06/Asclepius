"""
Firebase Firestore Seed Script (REST API Version)
Populates the database with sample hospitals and initial data
Uses Firebase REST API - no service account needed for basic operations
"""

import requests
import json
from datetime import datetime
import uuid

# Firebase Project Configuration
PROJECT_ID = "sih1-c72f3"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# Sample Hospitals Data
HOSPITALS = [
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
]


def convert_to_firestore_format(data: dict) -> dict:
    """Convert Python dict to Firestore REST API format"""
    fields = {}

    for key, value in data.items():
        if isinstance(value, str):
            fields[key] = {"stringValue": value}
        elif isinstance(value, bool):
            fields[key] = {"booleanValue": value}
        elif isinstance(value, int):
            fields[key] = {"integerValue": str(value)}
        elif isinstance(value, float):
            fields[key] = {"doubleValue": value}
        elif isinstance(value, list):
            array_values = []
            for item in value:
                if isinstance(item, str):
                    array_values.append({"stringValue": item})
                elif isinstance(item, int):
                    array_values.append({"integerValue": str(item)})
            fields[key] = {"arrayValue": {"values": array_values}}
        elif value is None:
            fields[key] = {"nullValue": None}

    # Add timestamps
    fields["createdAt"] = {"timestampValue": datetime.utcnow().isoformat() + "Z"}
    fields["updatedAt"] = {"timestampValue": datetime.utcnow().isoformat() + "Z"}

    return {"fields": fields}


def print_manual_instructions():
    """Print instructions for manual database seeding"""
    print("\n" + "="*60)
    print("📋 MANUAL DATABASE SEEDING INSTRUCTIONS")
    print("="*60)
    print("""
Since Firebase REST API requires authentication for writes,
you can seed the database manually through Firebase Console:

1. Go to: https://console.firebase.google.com/project/sih1-c72f3/firestore

2. Create a collection called 'hospitals'

3. Add documents with the following data:

""")

    for i, hospital in enumerate(HOSPITALS, 1):
        print(f"\n--- Hospital {i}: {hospital['name']} ---")
        print(json.dumps(hospital, indent=2))

    print("""
\n4. Create a collection called 'outbreak_signals' (optional)

5. The 'patients', 'doctors', 'tokens', and 'triage_sessions' 
   collections will be created automatically when users sign up
   and use the app.

""")


def generate_flutter_seed_code():
    """Generate Dart code to seed data from the Flutter app"""
    print("\n" + "="*60)
    print("📱 FLUTTER SEED CODE")
    print("="*60)
    print("""
Add this to your Flutter app to seed hospitals on first run:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

Future<void> seedHospitals() async {
  final firestore = FirebaseFirestore.instance;
  final hospitalsRef = firestore.collection('hospitals');
  
  // Check if already seeded
  final existing = await hospitalsRef.limit(1).get();
  if (existing.docs.isNotEmpty) {
    print('Hospitals already seeded');
    return;
  }

  final hospitals = [
""")

    for hospital in HOSPITALS:
        print(f"    {json.dumps(hospital, indent=4)},")

    print("""
  ];

  for (final hospital in hospitals) {
    await hospitalsRef.add({
      ...hospital,
      'createdAt': FieldValue.serverTimestamp(),
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }
  
  print('Seeded ${hospitals.length} hospitals');
}
```
""")


if __name__ == "__main__":
    print("🚀 SwasthyaFlow AI - Database Seeder")
    print("="*60)

    print_manual_instructions()

    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"\nTotal hospitals to add: {len(HOSPITALS)}")
    print("\nCollections structure:")
    print("  • hospitals - Government healthcare facilities")
    print("  • patients - Created on user signup")
    print("  • doctors - Created on doctor registration")
    print("  • tokens - Created when patients get queue tokens")
    print("  • triage_sessions - Created on triage assessment")
    print("  • outbreak_signals - System-generated alerts")
    print("\n✅ Firestore rules and indexes already deployed!")

