# 🔄 BEFORE & AFTER CODE EXAMPLES

## 1. Schemas - UUID to String Conversion

### BEFORE ❌
```python
# backend/app/schemas/schemas.py
from uuid import UUID

class PatientResponse(BaseModel):
    id: UUID  # ❌ Expected UUID object
    age: int
    gender: GenderEnum
    # ...

class TriageRequest(BaseModel):
    patient_id: UUID  # ❌ Expected UUID object
    symptoms: List[str]
    vitals: VitalsInput
    ehr_file_id: Optional[UUID] = None  # ❌
    # ...

class TriageResponse(BaseModel):
    session_id: UUID  # ❌ Expected UUID object
    risk_level: RiskLevelEnum
    # ...
```

### AFTER ✅
```python
# backend/app/schemas/schemas.py
# UUID import removed ✅

class PatientResponse(BaseModel):
    id: str  # ✅ Accepts string IDs
    age: int
    gender: GenderEnum
    # ...

class TriageRequest(BaseModel):
    patient_id: str  # ✅ Accepts string IDs
    symptoms: List[str]
    vitals: VitalsInput
    ehr_file_id: Optional[str] = None  # ✅
    # ...

class TriageResponse(BaseModel):
    session_id: str  # ✅ Accepts string IDs
    risk_level: RiskLevelEnum
    # ...
```

---

## 2. Patients API - Route Order & Type Fixes

### BEFORE ❌
```python
# backend/app/api/v1/patients.py
from uuid import UUID

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient_data: PatientCreate, db: AsyncSession = Depends(get_db)):
    """Register a new patient"""
    # ... implementation ...
    return patient


@router.get("/{patient_id}", response_model=PatientResponse)  # ❌ Defined first!
async def get_patient(
    patient_id: UUID,  # ❌ Expects UUID
    db: AsyncSession = Depends(get_db)
):
    """Get patient by ID"""
    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)  # Type mismatch!
    )
    # ...


@router.get("/search", response_model=PatientResponse)  # ❌ Defined second - unreachable!
async def search_patient(
    phone: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Search for a patient by phone or email"""
    # ... implementation ...
```

### AFTER ✅
```python
# backend/app/api/v1/patients.py
# UUID import removed ✅

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient_data: PatientCreate, db: AsyncSession = Depends(get_db)):
    """Register a new patient"""
    # ... implementation ...
    return patient


@router.get("/search", response_model=PatientResponse)  # ✅ Defined first - will be matched!
async def search_patient(
    phone: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Search for a patient by phone or email"""
    # ... implementation ...


@router.get("/{patient_id}", response_model=PatientResponse)  # ✅ Defined second - fallback
async def get_patient(
    patient_id: str,  # ✅ Accepts string IDs
    db: AsyncSession = Depends(get_db)
):
    """Get patient by ID"""
    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)  # ✅ Type match!
    )
    # ...


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,  # ✅ Changed from UUID
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update patient information"""
    # ...


@router.delete("/{patient_id}", response_model=MessageResponse)
async def delete_patient(
    patient_id: str,  # ✅ Changed from UUID
    db: AsyncSession = Depends(get_db)
):
    """Delete a patient record"""
    # ...
```

---

## 3. Triage API - Type Fixes & Constructor Removal

### BEFORE ❌
```python
# backend/app/api/v1/triage.py
from uuid import UUID

@router.post("/", response_model=TriageResponse)
async def submit_triage(
    triage_data: TriageRequest,  # ❌ Contains patient_id: UUID
    db: AsyncSession = Depends(get_db)
):
    """Submit patient symptoms for triage assessment"""
    
    # Get patient information - expects UUID but database has string
    result = await db.execute(
        select(Patient).where(Patient.id == triage_data.patient_id)  # Type mismatch!
    )
    # ...
    
    # Create hospital suggestions
    if suggestions:
        primary_hospital = HospitalSuggestion(
            hospital_id=UUID(suggestions[0]["hospital_id"]),  # ❌ Unnecessary conversion
            name=suggestions[0]["name"],
            # ...
        )
        
        alternate_hospitals = [
            HospitalSuggestion(
                hospital_id=UUID(s["hospital_id"]),  # ❌ Unnecessary conversion
                # ...
            )
            for s in suggestions[1:]
        ]


@router.get("/{session_id}/explain")
async def get_explanation(
    session_id: UUID,  # ❌ Expects UUID
    db: AsyncSession = Depends(get_db)
):
    """Get detailed explanation for a triage session"""
    result = await db.execute(
        select(TriageSession).where(TriageSession.id == session_id)  # Type mismatch!
    )
    # ...


@router.get("/history/{patient_id}", response_model=List[TriageHistoryItem])
async def get_triage_history(
    patient_id: UUID,  # ❌ Expects UUID
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get triage history for a patient"""
    result = await db.execute(
        select(TriageSession)
        .where(TriageSession.patient_id == patient_id)  # Type mismatch!
        # ...
    )
    # ...
```

### AFTER ✅
```python
# backend/app/api/v1/triage.py
# UUID import removed ✅

@router.post("/", response_model=TriageResponse)
async def submit_triage(
    triage_data: TriageRequest,  # ✅ Contains patient_id: str
    db: AsyncSession = Depends(get_db)
):
    """Submit patient symptoms for triage assessment"""
    
    # Get patient information - perfect type match
    result = await db.execute(
        select(Patient).where(Patient.id == triage_data.patient_id)  # ✅ Type match!
    )
    # ...
    
    # Create hospital suggestions
    if suggestions:
        primary_hospital = HospitalSuggestion(
            hospital_id=suggestions[0]["hospital_id"],  # ✅ Direct string assignment
            name=suggestions[0]["name"],
            # ...
        )
        
        alternate_hospitals = [
            HospitalSuggestion(
                hospital_id=s["hospital_id"],  # ✅ Direct string assignment
                # ...
            )
            for s in suggestions[1:]
        ]


@router.get("/{session_id}/explain")
async def get_explanation(
    session_id: str,  # ✅ Accepts string IDs
    db: AsyncSession = Depends(get_db)
):
    """Get detailed explanation for a triage session"""
    result = await db.execute(
        select(TriageSession).where(TriageSession.id == session_id)  # ✅ Type match!
    )
    # ...


@router.get("/history/{patient_id}", response_model=List[TriageHistoryItem])
async def get_triage_history(
    patient_id: str,  # ✅ Accepts string IDs
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get triage history for a patient"""
    result = await db.execute(
        select(TriageSession)
        .where(TriageSession.patient_id == patient_id)  # ✅ Type match!
        # ...
    )
    # ...
```

---

## 4. Hospitals API - Type Fixes & Constructor Removal

### BEFORE ❌
```python
# backend/app/api/v1/hospitals.py
from uuid import UUID

@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(
    hospital_id: UUID,  # ❌ Expects UUID
    db: AsyncSession = Depends(get_db)
):
    """Get hospital by ID"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # Type mismatch!
    )
    # ...


@router.get("/{hospital_id}/load", response_model=HospitalLoadResponse)
async def get_hospital_load(
    hospital_id: UUID,  # ❌ Expects UUID
    db: AsyncSession = Depends(get_db)
):
    """Get real-time department load for a hospital"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # Type mismatch!
    )
    # ...
    load_data = load_balancer.get_hospital_load(str(hospital_id))  # Hack: convert to str
    # ...


@router.post("/suggest", response_model=List[HospitalSuggestion])
async def suggest_alternate_hospitals(
    request: AlternateHospitalRequest,
    db: AsyncSession = Depends(get_db)
):
    """Get alternate hospital suggestions"""
    # ...
    return [
        HospitalSuggestion(
            hospital_id=UUID(s["hospital_id"]),  # ❌ Unnecessary conversion
            # ...
        )
        for s in suggestions
    ]


@router.put("/{hospital_id}/load")
async def update_department_load(
    hospital_id: UUID,  # ❌ Expects UUID
    department: str,
    current_patients: int,
    max_capacity: int,
    db: AsyncSession = Depends(get_db)
):
    """Update department load"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # Type mismatch!
    )
    # ...
    load_balancer.update_load(
        str(hospital_id), department, current_patients, max_capacity  # Hack: convert to str
    )
    # ...
```

### AFTER ✅
```python
# backend/app/api/v1/hospitals.py
# UUID import removed ✅

@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(
    hospital_id: str,  # ✅ Accepts string IDs
    db: AsyncSession = Depends(get_db)
):
    """Get hospital by ID"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # ✅ Type match!
    )
    # ...


@router.get("/{hospital_id}/load", response_model=HospitalLoadResponse)
async def get_hospital_load(
    hospital_id: str,  # ✅ Accepts string IDs
    db: AsyncSession = Depends(get_db)
):
    """Get real-time department load for a hospital"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # ✅ Type match!
    )
    # ...
    load_data = load_balancer.get_hospital_load(hospital_id)  # ✅ Direct string usage
    # ...


@router.post("/suggest", response_model=List[HospitalSuggestion])
async def suggest_alternate_hospitals(
    request: AlternateHospitalRequest,
    db: AsyncSession = Depends(get_db)
):
    """Get alternate hospital suggestions"""
    # ...
    return [
        HospitalSuggestion(
            hospital_id=s["hospital_id"],  # ✅ Direct string assignment
            # ...
        )
        for s in suggestions
    ]


@router.put("/{hospital_id}/load")
async def update_department_load(
    hospital_id: str,  # ✅ Accepts string IDs
    department: str,
    current_patients: int,
    max_capacity: int,
    db: AsyncSession = Depends(get_db)
):
    """Update department load"""
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)  # ✅ Type match!
    )
    # ...
    load_balancer.update_load(
        hospital_id, department, current_patients, max_capacity  # ✅ Direct string usage
    )
    # ...
```

---

## Request/Response Examples

### Triage Endpoint - Before vs After

#### BEFORE ❌
```bash
$ curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "symptoms": ["fever", "cough"],
    "vitals": {...}
  }'

HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "type": "uuid_parsing",
      "loc": ["body", "patient_id"],
      "msg": "Input should be a valid UUID, unable to parse string as a UUID: 550e8400-e29b-41d4-a716-446655440000",
      "input": "550e8400-e29b-41d4-a716-446655440000",
      "ctx": {"error": "invalid UUID version"}
    }
  ]
}
```

#### AFTER ✅
```bash
$ curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "symptoms": ["fever", "cough"],
    "vitals": {...}
  }'

HTTP/1.1 200 OK
Content-Type: application/json

{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "risk_level": "HIGH",
  "department": "Emergency",
  "confidence": 0.95,
  "explanation": {
    "top_features": [...],
    "shap_values": {...},
    "model_confidence": 0.95,
    "rule_triggered": null
  },
  "primary_hospital": {
    "hospital_id": "f1e2d3c4-b5a6-9870-fedc-ba9876543210",
    "name": "Central Medical Hospital",
    "distance_km": 2.5,
    "current_load": 0.65,
    "estimated_wait_minutes": 15,
    "departments_available": ["Emergency", "ICU", "General"]
  },
  "alternate_hospitals": [...],
  "estimated_wait_minutes": 15,
  "created_at": "2026-02-15T10:30:45.123456"
}
```

---

**Summary**: All changes align the type system throughout the backend, eliminating validation errors and enabling proper request processing.

