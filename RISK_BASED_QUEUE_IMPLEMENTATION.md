## ✅ Risk-Based Queue Management System - Implementation Guide

### Overview
This document outlines the implementation of a risk-based patient queue management system with wait time calculation, medical report uploads, and real-time queue status updates.

---

## 🎯 Key Features Implemented

### 1. **Risk-Based Wait Time Calculation**
**Backend**: `backend/app/api/v1/tokens.py`

Wait times now differ based on patient risk level:
- **HIGH RISK** → 5 minutes per patient in queue
- **MEDIUM RISK** → 10 minutes per patient in queue  
- **LOW RISK** → 15 minutes per patient in queue

**Example:**
- HIGH risk patient at position 2 → 10 minutes wait
- MEDIUM risk patient at position 2 → 20 minutes wait
- LOW risk patient at position 2 → 30 minutes wait

**Implementation:**
```python
def calculate_wait_time_by_risk(risk_level: str, queue_position: int) -> int:
    """Calculate wait time based on risk level"""
    base_wait = {
        'HIGH': 5,      # 5 minutes per patient
        'MEDIUM': 10,   # 10 minutes per patient
        'LOW': 15,      # 15 minutes per patient
    }
    wait_per_patient = base_wait.get(risk_level, 10)
    return queue_position * wait_per_patient
```

---

### 2. **Doctor Dashboard - Next Patient Preview**
**File**: `lib/features/doctor_dashboard/doctor_dashboard_screen.dart`

New **`_NextPatientCard`** widget shows:
- ✅ **Risk Level** with color coding (HIGH=Red, MEDIUM=Yellow, LOW=Green)
- ✅ **Token Number** (#1, #2, etc.)
- ✅ **Estimated Wait Time** (calculated from risk level)
- ✅ **Priority Indicator** (arrow showing urgent patients)

**Visual Design:**
```
┌─────────────────────────────────┐
│ Next Patient                 HIGH│
│ Token #5                         │
│ Est. wait: 10 minutes      →     │
└─────────────────────────────────┘
```

**Queue Priority Order:**
1. HIGH risk patients (called first)
2. MEDIUM risk patients  
3. LOW risk patients

---

### 3. **Patient Queue Status Screen**
**File**: `lib/features/patient_queue/patient_queue_status_screen.dart`

New comprehensive screen showing:

#### A. **Patient Information Card**
- Name, Age, Gender
- Contact information (if available)

#### B. **Risk Level & Token Card**
- Risk level with color-coded badge (HIGH/MEDIUM/LOW)
- Token number (#1, #2, etc.)

#### C. **Wait Time Timer Card**
- **Live countdown timer** showing remaining time
- Queue position (#1 in queue, #2 in queue, etc.)
- Estimated wait time (e.g., "15 minutes")
- Visual progress bar showing time elapsed

**Timer Logic:**
```dart
Expected Time = Created At + Estimated Wait Minutes
Remaining Time = Expected Time - Now
```

#### D. **Department Card**
- Department name (e.g., Emergency, Cardiology)
- Doctor specialization (when assigned)

#### E. **Medical Reports Section**
- Upload PDF medical reports
- View uploaded documents with metadata
- Delete reports if needed

---

### 4. **Medical Report Upload**
**File**: `lib/data/services/medical_document_service.dart`

**Features:**
- ✅ File picker for PDF selection only
- ✅ Upload to Firebase Storage
- ✅ File size validation (max 10MB)
- ✅ Download URL generation
- ✅ List all uploaded reports
- ✅ Delete reports functionality
- ✅ Sort by upload date (newest first)

**Storage Path Structure:**
```
medical-reports/
  └── {patientId}/
      ├── report_1707123456.pdf
      ├── report_1707124567.pdf
      └── report_1707125678.pdf
```

**Upload Implementation:**
```dart
// User picks PDF file
final result = await FilePicker.platform.pickFiles(
  type: FileType.custom,
  allowedExtensions: ['pdf'],
);

// Upload to Firebase Storage
final ref = _storage.ref('medical-reports/$patientId/$fileName');
await ref.putFile(file);

// Get download URL
final downloadUrl = await ref.getDownloadURL();
```

---

## 📊 Database/Firestore Structure

### Tokens Collection
```json
{
  "id": "token-uuid",
  "tokenNumber": 5,
  "patientId": "patient-uuid",
  "sessionId": "session-uuid",
  "riskLevel": "HIGH",        // HIGH, MEDIUM, or LOW
  "department": "Emergency",
  "hospitalId": "hospital-uuid",
  "priority": 100050,         // Calculated from risk + time
  "status": "waiting",        // waiting, in_progress, completed, cancelled
  "queuePosition": 1,         // Position in queue
  "estimatedWaitMinutes": 10, // RISK-BASED calculation
  "doctorId": "doctor-uuid",  // Assigned when called
  "createdAt": "2024-02-15T10:30:00Z",
  "calledAt": null,
  "completedAt": null
}
```

### Patients Collection
```json
{
  "uid": "firebase-uid",
  "name": "Patient Name",
  "age": 35,
  "gender": "M",
  "email": "patient@example.com",
  "phone": "+91-9876543210",
  "district": "Chennai",
  "state": "Tamil Nadu",
  "preExistingConditions": ["Hypertension", "Diabetes"],
  "userType": "patient",
  "createdAt": "2024-02-01T10:00:00Z",
  "updatedAt": "2024-02-15T10:30:00Z"
}
```

### Medical Reports (Firebase Storage)
```
medical-reports/{patientId}/{reportFileName}.pdf

Metadata:
- uploadedAt: 2024-02-15T10:30:00Z
- size: 2097152 (bytes)
- contentType: application/pdf
```

---

## 🔄 API Endpoints

### New/Updated Endpoints

#### 1. **Get Next Patient (Preview)**
```
GET /api/v1/tokens/next-patient/{doctor_id}/{hospital_id}/{department}

Response:
{
  "id": "token-id",
  "tokenNumber": 5,
  "patientId": "patient-id",
  "riskLevel": "HIGH",
  "estimatedWaitMinutes": 10,
  "queuePosition": 1,
  ...
}
```

#### 2. **Generate Token (Risk-Based)**
```
POST /api/v1/tokens/generate

Request:
{
  "patient_id": "patient-uuid",
  "session_id": "session-uuid",
  "risk_level": "HIGH",           // HIGH, MEDIUM, or LOW
  "department": "Emergency",
  "hospital_id": "hospital-uuid",
  "doctor_id": null
}

Response includes:
- "estimatedWaitMinutes": 10  // Calculated from risk level
- "queuePosition": 1
```

#### 3. **Get Patient Token**
```
GET /api/v1/tokens/patient/{patient_id}

Returns current active token with live data
```

#### 4. **Call Next Patient**
```
POST /api/v1/tokens/call-next/{doctor_id}/{hospital_id}/{department}

Changes token status to "in_progress"
Updates queue positions for remaining patients
```

---

## 🎨 UI/UX Components

### Color Coding by Risk Level
```dart
// In AppTheme or theme constants
highRiskColor = Colors.red[600]      // #D32F2F
mediumRiskColor = Colors.amber[600]  // #F57F17
lowRiskColor = Colors.green[600]     // #388E3C
```

### Doctor Dashboard
- [x] Doctor info card (name, department, specialization)
- [x] Queue overview (total, high, medium, low counts)
- [x] **Next Patient Card** (NEW - with risk badge)
- [x] "Call Next Patient" button (primary action)
- [x] Waiting patients list (scrollable)
- [x] Availability toggle (break management)

### Patient Dashboard
- [x] Patient info card
- [x] **Risk Level badge** (color-coded)
- [x] **Token number**
- [x] **Live wait time timer** (NEW)
- [x] Queue position
- [x] Department info
- [x] **Medical Report Upload** (NEW)
- [x] **Uploaded Reports List** (NEW - with delete)

---

## 🔧 Setup & Configuration

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Update if needed:
# - fastapi
# - python-jose
# - passlib
# - pydantic
```

### Flutter Setup
```bash
flutter pub get
flutter clean
flutter pub get
```

### Firebase Configuration
1. Enable Cloud Storage in Firebase Console
2. Update Firestore security rules to allow authenticated users to upload/download:

```firestore
match /medical-reports/{patientId}/{document=**} {
  allow read, write: if request.auth.uid == patientId;
}
```

---

## 📱 Patient Flow

1. **Patient logs in** → Firestore loads patient profile
2. **Patient completes triage** → Risk assessment (HIGH/MEDIUM/LOW)
3. **Token generated** → Queue position + risk-based wait time calculated
4. **Patient views queue status**:
   - Risk level displayed with color
   - Live countdown timer
   - Queue position
   - Can upload medical reports
5. **Wait time updates** in real-time via Firestore listener

---

## 👨‍⚕️ Doctor Flow

1. **Doctor logs in** → Loads dashboard
2. **Doctor sees next patient card**:
   - Risk level (color-coded)
   - Token number
   - Estimated wait time
3. **Doctor clicks "Call Next Patient"**:
   - Highest priority patient selected (by risk level + arrival time)
   - Status changed to "in_progress"
   - Doctor assigned to token
   - Remaining queue positions recalculated
4. **Doctor views patient details** → Can see:
   - Patient info
   - Risk factors
   - Medical reports (PDF)
   - SHAP explanations (if available)

---

## 🧮 Priority Calculation Algorithm

```
Priority Score = (Risk Level Base * 1000) + Time Factor

Risk Level Base:
  - HIGH   = 100
  - MEDIUM = 50
  - LOW    = 10

Time Factor = (1440 - minutes_since_midnight) / 100
  - Earlier arrivals get slightly higher priority within same risk level
  - Max ~14 points

Examples:
  - HIGH risk at 10:00 AM  = 100,000 + 5 = 100,005
  - MEDIUM risk at 10:00 AM = 50,000 + 5 = 50,005
  - LOW risk at 10:00 AM    = 10,000 + 5 = 10,005

Wait Time = Queue Position * Base Wait Time
  - HIGH risk wait     = position * 5 min
  - MEDIUM risk wait   = position * 10 min
  - LOW risk wait      = position * 15 min
```

---

## ✅ Testing Checklist

### Backend Testing
- [ ] Risk-based wait time calculation (HIGH/MEDIUM/LOW)
- [ ] Queue position updates after token generation
- [ ] `/next-patient` endpoint returns correct patient
- [ ] Priority sorting (HIGH before MEDIUM before LOW)
- [ ] Call next patient flow

### Flutter Testing
- [ ] Patient queue status screen loads
- [ ] Live timer counts down correctly
- [ ] Risk level colors display properly
- [ ] Medical report upload works
- [ ] Reports list shows uploaded files
- [ ] Delete report functionality works
- [ ] Doctor next patient card shows HIGH risk first
- [ ] "Call Next Patient" button updates queue
- [ ] Queue positions recalculate after a patient is called

### Integration Testing
- [ ] Patient logs in → sees queue status with timer
- [ ] Doctor logs in → sees next HIGH risk patient
- [ ] Doctor calls patient → patient's status updates
- [ ] Remaining patients' queue positions update
- [ ] Multiple patients → correct risk-based ordering

---

## 🐛 Known Limitations & Future Improvements

### Current Limitations
1. **In-memory token storage** - tokens lost on app restart (use Redis/Firestore in production)
2. **No real doctor profiles** - doctor details need to be in Firestore for full functionality
3. **No video/audio call** - integration with Agora/Jitsi for actual consultation
4. **No SMS notifications** - patient notifications for doctor availability
5. **No analytics** - wait time trends, department load analysis

### Future Enhancements
1. Implement persistent token storage (Firestore/Redis)
2. Add SMS notifications for patients
3. Add video consultation capability
4. Add department load forecasting
5. Add fairness audit for bias detection
6. Add outbreak signal detection
7. Implement doctor availability calendar

---

## 📞 Support

For issues or questions:
1. Check the API documentation: `/api/v1/docs` (Swagger)
2. Review Flutter logs: `flutter logs`
3. Check Firebase Console for storage/auth errors
4. Review backend logs in Cloud Run/Docker

---

**Last Updated**: February 15, 2026
**Version**: 1.1.0

