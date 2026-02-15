# 🔧 EXACT CHANGES - LINE BY LINE

## File 1: backend/app/schemas/schemas.py

### Change 1: Remove UUID Import
**Location**: Line 7
```python
# REMOVED:
from uuid import UUID
```

### Change 2: PatientResponse.id
**Location**: Line 38
```python
# BEFORE:
id: UUID

# AFTER:
id: str
```

### Change 3: TriageRequest.patient_id
**Location**: Line 60
```python
# BEFORE:
patient_id: UUID

# AFTER:
patient_id: str
```

### Change 4: TriageRequest.ehr_file_id
**Location**: Line 62
```python
# BEFORE:
ehr_file_id: Optional[UUID] = None

# AFTER:
ehr_file_id: Optional[str] = None
```

### Change 5: TriageResponse.session_id
**Location**: Line 90
```python
# BEFORE:
session_id: UUID

# AFTER:
session_id: str
```

### Change 6: HospitalSuggestion.hospital_id
**Location**: Line 78
```python
# BEFORE:
hospital_id: UUID

# AFTER:
hospital_id: str
```

### Change 7: HospitalResponse.id
**Location**: Line 130
```python
# BEFORE:
id: UUID

# AFTER:
id: str
```

### Change 8: HospitalLoadResponse.hospital_id
**Location**: Line 143
```python
# BEFORE:
hospital_id: UUID

# AFTER:
hospital_id: str
```

### Change 9: OutbreakTrendResponse.id
**Location**: Line 167
```python
# BEFORE:
id: UUID

# AFTER:
id: str
```

### Change 10: EHRUploadResponse.document_id
**Location**: Line 198
```python
# BEFORE:
document_id: UUID

# AFTER:
document_id: str
```

### Change 11: TriageHistoryItem.session_id
**Location**: Line 100
```python
# BEFORE:
session_id: UUID

# AFTER:
session_id: str
```

---

## File 2: backend/app/api/v1/patients.py

### Change 1: Remove UUID Import
**Location**: Line 8
```python
# REMOVED:
from uuid import UUID
```

### Change 2: Route Order - Move /search before /{patient_id}
**Location**: Moved from line ~150 to line 60
```python
# MOVED UP:
@router.get("/search", response_model=PatientResponse)
async def search_patient(
    phone: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    # ... implementation
```

### Change 3: get_patient - UUID to str
**Location**: Line 88
```python
# BEFORE:
def get_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def get_patient(
    patient_id: str,
    db: AsyncSession = Depends(get_db)
):
```

### Change 4: update_patient - UUID to str
**Location**: Line 103
```python
# BEFORE:
def update_patient(
    patient_id: UUID,
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def update_patient(
    patient_id: str,
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
```

### Change 5: delete_patient - UUID to str
**Location**: Line 127
```python
# BEFORE:
def delete_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def delete_patient(
    patient_id: str,
    db: AsyncSession = Depends(get_db)
):
```

---

## File 3: backend/app/api/v1/triage.py

### Change 1: Remove UUID Import
**Location**: Line 8
```python
# REMOVED:
from uuid import UUID
```

### Change 2: get_explanation - UUID to str
**Location**: Line ~160
```python
# BEFORE:
def get_explanation(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def get_explanation(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
```

### Change 3: get_triage_history - UUID to str
**Location**: Line ~191
```python
# BEFORE:
def get_triage_history(
    patient_id: UUID,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def get_triage_history(
    patient_id: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
```

### Change 4: Remove UUID() constructor for primary hospital
**Location**: Line ~97
```python
# BEFORE:
primary_hospital = HospitalSuggestion(
    hospital_id=UUID(suggestions[0]["hospital_id"]),
    name=suggestions[0]["name"],
    # ...
)

# AFTER:
primary_hospital = HospitalSuggestion(
    hospital_id=suggestions[0]["hospital_id"],
    name=suggestions[0]["name"],
    # ...
)
```

### Change 5: Remove UUID() constructor for alternate hospitals
**Location**: Line ~108
```python
# BEFORE:
alternate_hospitals = [
    HospitalSuggestion(
        hospital_id=UUID(s["hospital_id"]),
        # ...
    )
    for s in suggestions[1:]
]

# AFTER:
alternate_hospitals = [
    HospitalSuggestion(
        hospital_id=s["hospital_id"],
        # ...
    )
    for s in suggestions[1:]
]
```

---

## File 4: backend/app/api/v1/hospitals.py

### Change 1: Remove UUID Import
**Location**: Line 8
```python
# REMOVED:
from uuid import UUID
```

### Change 2: get_hospital - UUID to str
**Location**: Line ~101
```python
# BEFORE:
def get_hospital(
    hospital_id: UUID,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def get_hospital(
    hospital_id: str,
    db: AsyncSession = Depends(get_db)
):
```

### Change 3: get_hospital_load - UUID to str
**Location**: Line ~122
```python
# BEFORE:
def get_hospital_load(
    hospital_id: UUID,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def get_hospital_load(
    hospital_id: str,
    db: AsyncSession = Depends(get_db)
):
```

### Change 4: update_department_load - UUID to str
**Location**: Line ~213
```python
# BEFORE:
def update_department_load(
    hospital_id: UUID,
    department: str,
    current_patients: int,
    max_capacity: int,
    db: AsyncSession = Depends(get_db)
):

# AFTER:
def update_department_load(
    hospital_id: str,
    department: str,
    current_patients: int,
    max_capacity: int,
    db: AsyncSession = Depends(get_db)
):
```

### Change 5: Remove UUID() constructor in suggest_alternate_hospitals
**Location**: Line ~200
```python
# BEFORE:
return [
    HospitalSuggestion(
        hospital_id=UUID(s["hospital_id"]),
        # ...
    )
    for s in suggestions
]

# AFTER:
return [
    HospitalSuggestion(
        hospital_id=s["hospital_id"],
        # ...
    )
    for s in suggestions
]
```

---

## Summary of Changes by Category

### UUID Type Changes (11 total)
1. PatientResponse.id
2. TriageRequest.patient_id
3. TriageRequest.ehr_file_id
4. TriageResponse.session_id
5. HospitalSuggestion.hospital_id
6. HospitalResponse.id
7. HospitalLoadResponse.hospital_id
8. OutbreakTrendResponse.id
9. EHRUploadResponse.document_id
10. TriageHistoryItem.session_id
11. (Plus 3 endpoint parameters)

### UUID Imports Removed (4 total)
1. schemas.py
2. patients.py
3. triage.py
4. hospitals.py

### UUID() Constructor Calls Removed (3 total)
1. triage.py - primary_hospital
2. triage.py - alternate_hospitals
3. hospitals.py - suggestions

### Route Order Changes (1 total)
1. patients.py - /search moved before /{patient_id}

### Endpoint Parameter Changes (8 total)
1. patients.py - get_patient
2. patients.py - update_patient
3. patients.py - delete_patient
4. triage.py - get_explanation
5. triage.py - get_triage_history
6. hospitals.py - get_hospital
7. hospitals.py - get_hospital_load
8. hospitals.py - update_department_load

---

**Total Changes**: ~32
**Files Modified**: 4
**Status**: ✅ Complete and Verified

