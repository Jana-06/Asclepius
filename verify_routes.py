#!/usr/bin/env python3
"""
Verification script to check route ordering and UUID fixes
"""

import sys
import re

def check_file(filepath, checks):
    """Check a file against multiple conditions"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        results = {}
        for check_name, pattern, should_exist in checks:
            found = bool(re.search(pattern, content))
            results[check_name] = {
                'found': found,
                'expected': should_exist,
                'passed': found == should_exist
            }

        return results
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

# Define checks
patients_checks = [
    ("UUID import removed", r'from uuid import UUID', False),
    ("/search route before /{patient_id}", r'@router\.get\("/search".*?@router\.get\("/{patient_id}"', True),
    ("get_patient uses str", r'def get_patient\(\s*patient_id: str', True),
    ("update_patient uses str", r'def update_patient\(\s*patient_id: str', True),
    ("delete_patient uses str", r'def delete_patient\(\s*patient_id: str', True),
]

triage_checks = [
    ("UUID import removed", r'from uuid import UUID', False),
    ("get_explanation uses str", r'def get_explanation\(\s*session_id: str', True),
    ("get_triage_history uses str", r'def get_triage_history\(\s*patient_id: str', True),
    ("No UUID() constructor calls", r'UUID\(.*?\)', False),
]

hospitals_checks = [
    ("UUID import removed", r'from uuid import UUID', False),
    ("get_hospital uses str", r'def get_hospital\(\s*hospital_id: str', True),
    ("get_hospital_load uses str", r'def get_hospital_load\(\s*hospital_id: str', True),
    ("update_department_load uses str", r'def update_department_load\(\s*hospital_id: str', True),
    ("No UUID() constructor calls", r'UUID\(.*?\)', False),
]

schemas_checks = [
    ("UUID import removed", r'from uuid import UUID', False),
    ("PatientResponse uses str id", r'class PatientResponse.*?id: str', True),
    ("TriageRequest uses str patient_id", r'class TriageRequest.*?patient_id: str', True),
    ("TriageResponse uses str session_id", r'class TriageResponse.*?session_id: str', True),
    ("HospitalSuggestion uses str hospital_id", r'class HospitalSuggestion.*?hospital_id: str', True),
]

files_to_check = [
    ("backend/app/api/v1/patients.py", patients_checks),
    ("backend/app/api/v1/triage.py", triage_checks),
    ("backend/app/api/v1/hospitals.py", hospitals_checks),
    ("backend/app/schemas/schemas.py", schemas_checks),
]

all_passed = True
for filepath, checks in files_to_check:
    print(f"\n{'='*60}")
    print(f"Checking: {filepath}")
    print(f"{'='*60}")

    results = check_file(filepath, checks)
    if results is None:
        all_passed = False
        continue

    for check_name, result in results.items():
        status = "✅" if result['passed'] else "❌"
        expected = "should NOT exist" if not result['expected'] else "should exist"
        found = "Found" if result['found'] else "Not found"
        print(f"{status} {check_name}")
        print(f"   Expected: {expected}, {found}")
        if not result['passed']:
            all_passed = False

print(f"\n{'='*60}")
if all_passed:
    print("✅ ALL CHECKS PASSED!")
    sys.exit(0)
else:
    print("❌ SOME CHECKS FAILED!")
    sys.exit(1)

