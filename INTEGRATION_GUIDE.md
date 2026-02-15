## 🔗 Integration Guide: Risk-Based Queue System

### Quick Start for Testing

#### 1. Start the Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### 2. Run the Flutter App
```bash
flutter run
```

#### 3. Test the Complete Flow

##### Step A: Patient Registration & Triage
1. Login/Register as patient
2. Complete triage assessment
   - Select symptoms
   - Input vitals (BP, HR, Temp)
   - System calculates risk level (HIGH/MEDIUM/LOW)
3. Token generated with risk-based wait time

##### Step B: View Patient Queue Status
1. Navigate to "Patient Queue Status" screen
2. Verify:
   - Risk level badge (color-coded)
   - Token number
   - Queue position
   - **Live countdown timer** (updates every second)
   - Estimated wait time based on risk level

Example:
```
HIGH risk patient at position 1:
  - Estimated wait: 5 minutes (5 × 1)
  - Timer: 5:00 → 4:59 → 4:58 ...

LOW risk patient at position 1:
  - Estimated wait: 15 minutes (15 × 1)
  - Timer: 15:00 → 14:59 → 14:58 ...
```

##### Step C: Upload Medical Reports
1. On Patient Queue Status screen
2. Click "Upload Medical Report (PDF)"
3. Select a PDF file from device
4. Verify upload success notification
5. See report in uploaded reports list

##### Step D: Doctor Dashboard
1. Login as doctor
2. View "Next Patient Card"
   - Should show patient with HIGHEST risk level first
   - Example: If queue has HIGH + MEDIUM + LOW risk patients, HIGH shown first
3. See queue statistics breakdown

##### Step E: Call Next Patient
1. Doctor clicks "Call Next Patient"
2. System:
   - Selects highest priority patient (HIGH risk)
   - Changes token status to "in_progress"
   - Assigns doctor to token
   - Recalculates queue positions for remaining patients
3. Remaining patients' wait times update accordingly

---

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PATIENT SIDE                             │
│                                                             │
│ 1. Login → 2. Triage → 3. Risk Assessment (HIGH/MED/LOW)   │
│             (symptoms, vitals)                             │
│                        ↓                                    │
│            4. Token Generated (backend)                     │
│               ├─ Token #N                                   │
│               ├─ Risk Level: HIGH                           │
│               ├─ Queue Position: #1                         │
│               ├─ Est. Wait: 5 min (HIGH × position)         │
│               └─ Status: waiting                            │
│                        ↓                                    │
│     5. Patient Queue Status Screen (Flutter)               │
│     ├─ Show Risk Badge (RED for HIGH)                      │
│     ├─ Show Token #N                                       │
│     ├─ Live Timer: 5:00 → 4:59 → 4:58...                   │
│     └─ Upload PDF Medical Reports                          │
│                        ↓                                    │
│            6. Wait for doctor to call                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                           ↕ (Firestore)
┌─────────────────────────────────────────────────────────────┐
│                     DOCTOR SIDE                             │
│                                                             │
│ 1. Login as Doctor                                         │
│                        ↓                                    │
│ 2. View Dashboard                                          │
│    ├─ Queue Stats (Total: 5, High: 2, Med: 2, Low: 1)     │
│    ├─ **Next Patient Card** (NEW)                         │
│    │   ├─ Risk: HIGH 🔴                                    │
│    │   ├─ Token: #5                                        │
│    │   └─ Est. Wait: 5 min                                 │
│    └─ Waiting Patients List                                │
│                        ↓                                    │
│ 3. Click "Call Next Patient"                               │
│    (Selects: highest priority, usually HIGH risk)          │
│                        ↓                                    │
│ 4. Patient Details Screen                                  │
│    ├─ Risk Assessment                                       │
│    ├─ Medical Reports (uploaded PDFs)                      │
│    ├─ Vitals & Symptoms                                    │
│    └─ SHAP Explanation                                     │
│                        ↓                                    │
│ 5. Complete Consultation                                   │
│    └─ Mark token as "completed"                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                  ↓ Queue Positions Update ↓
         Remaining patients' wait times recalculated
```

---

### Wait Time Examples

#### Scenario: 5 Patients in Queue

| Position | Risk Level | Wait Per Patient | Total Wait | Status |
|----------|-----------|-----------------|-----------|--------|
| 1        | HIGH      | 5 min           | 5 min     | Next   |
| 2        | HIGH      | 5 min           | 10 min    | Waiting|
| 3        | MEDIUM    | 10 min          | 10 min    | Waiting|
| 4        | MEDIUM    | 10 min          | 20 min    | Waiting|
| 5        | LOW       | 15 min          | 15 min    | Waiting|

**When Doctor Calls Position #1 (HIGH):**
- Position 1: Removed (in_progress)
- Position 2 (was 2): NEW position 1, wait = 5 min
- Position 3 (was 3): NEW position 2, wait = 20 min (10 + 10)
- Position 4 (was 4): NEW position 3, wait = 30 min (10 + 10 + 10)
- Position 5 (was 5): NEW position 4, wait = 60 min (5 + 10 + 10 + 10 + 15... NO wait, recalculation)

**After recalculation with 4 remaining patients:**
| Position | Risk Level | Wait Per Patient | Total Wait |
|----------|-----------|-----------------|-----------|
| 1        | HIGH      | 5 min           | 5 min     |
| 2        | MEDIUM    | 10 min          | 10 min    |
| 3        | MEDIUM    | 10 min          | 20 min    |
| 4        | LOW       | 15 min          | 15 min    |

---

### Backend Processing

#### Token Generation Flow
```python
# 1. Triage completed, risk_level determined
risk_level = "HIGH"  # From ML model

# 2. Generate token
token = {
    'id': uuid.uuid4(),
    'tokenNumber': 5,
    'patientId': patient_id,
    'riskLevel': 'HIGH',
    'department': 'Emergency',
    'priority': calculate_priority('HIGH', now),  # 100050
    'status': 'waiting',
    'created_at': now,
    ...
}

# 3. Update queue positions (calls calculate_wait_time_by_risk)
def update_queue_positions(hospital_id, department):
    waiting_tokens = [...ordered by priority...]
    for i, token in enumerate(waiting_tokens):
        token['queue_position'] = i + 1
        token['estimated_wait_minutes'] = calculate_wait_time_by_risk(
            token['risk_level'],  # 'HIGH', 'MEDIUM', or 'LOW'
            i + 1                 # position 1, 2, 3, etc.
        )
        # HIGH: 1*5=5, 2*5=10, 3*5=15...
        # MEDIUM: 1*10=10, 2*10=20, 3*10=30...
        # LOW: 1*15=15, 2*15=30, 3*15=45...

# 4. Return to patient
return TokenResponse(
    tokenNumber=5,
    riskLevel='HIGH',
    queuePosition=1,
    estimatedWaitMinutes=5,  # Calculated from risk!
    ...
)
```

---

### Firebase Collections

#### tokens collection
```json
{
  "token_uuid": {
    "id": "token-uuid",
    "tokenNumber": 5,
    "patientId": "patient-uuid",
    "riskLevel": "HIGH",           // From triage
    "department": "Emergency",
    "hospitalId": "hospital-uuid",
    "queuePosition": 1,            // Updated when others leave queue
    "estimatedWaitMinutes": 5,     // HIGH * 1 = 5
    "status": "waiting",           // waiting → in_progress → completed
    "priority": 100050,            // Used for sorting
    "createdAt": "2024-02-15T10:30:00Z",
    "doctorId": null,              // Set when called
    "calledAt": null               // Set when called
  }
}
```

#### medical-reports storage
```
medical-reports/
  └── patient-uuid/
      ├── report_1707123456.pdf
      ├── report_1707124567.pdf
      └── report_1707125678.pdf

Metadata for each file:
- uploadedAt: 2024-02-15T10:30:00Z
- size: 2097152 bytes
- contentType: application/pdf
```

---

### Frontend State Management

#### Patient Queue Status Screen State
```dart
// In _PatientQueueStatusScreenState
Map<String, dynamic>? _patientProfile;
List<Map<String, dynamic>> _medicalReports = [];
bool _isUploading = false;

// Loads from:
// 1. Firebase Auth (currentUser.uid)
// 2. Firestore patients collection (patient profile)
// 3. Firebase Storage (medical reports list)
// 4. Firestore tokens collection (via listener in parent)
```

#### Wait Time Timer
```dart
// In _WaitTimeCardState
void _updateRemainingTime() {
  final createdAt = widget.token['createdAt'] as DateTime;
  final estimatedMinutes = widget.token['estimatedWaitMinutes'] as int;
  
  final expectedTime = createdAt.add(Duration(minutes: estimatedMinutes));
  final now = DateTime.now();
  
  _remainingTime = expectedTime.difference(now);
  
  // Update every second
  Future.delayed(Duration(seconds: 1), () {
    if (mounted) {
      setState(() => _updateRemainingTime());
    }
  });
}

// Displayed as "5:00" → "4:59" → "4:58"...
String _formatDuration(Duration duration) {
  final minutes = duration.inMinutes;
  final seconds = duration.inSeconds.remainder(60);
  return '$minutes:${seconds.toString().padLeft(2, '0')} min';
}
```

---

### Real-Time Updates

#### Patient Queue Updates via Firestore Listeners
```dart
// Doctor dashboard listens to tokens collection
FirebaseFirestore.instance
  .collection('tokens')
  .where('hospitalId', isEqualTo: hospitalId)
  .where('department', isEqualTo: department)
  .where('status', isEqualTo: 'waiting')
  .orderBy('priority', descending: true)
  .orderBy('createdAt')
  .limit(10)
  .snapshots()  // Real-time listener
  .listen((snapshot) {
    // Update UI with new queue data
  });

// When doctor calls patient:
// 1. Token status changes to "in_progress"
// 2. Firestore listener triggers
// 3. Next patient card updates automatically
// 4. Queue positions refresh
// 5. Remaining patients' wait times recalculate
```

---

### Error Handling

#### Patient Upload Failure
```
User clicks "Upload Medical Report"
  ↓
File picker opens (PDF only)
  ↓
File selected, validation:
  - ✓ Is PDF
  - ✓ Size < 10MB
  - ✗ Fails: "File too large"
      → Show error: "File size exceeds 10MB limit"
  ↓
If passes validation:
  - Upload to Firebase Storage
  - ✗ Fails: "Network error"
      → Show error: "Failed to upload report"
  - ✓ Success
      → Show snackbar: "Medical report uploaded successfully"
      → Refresh reports list
```

---

### Performance Considerations

1. **Wait Time Calculation**: O(n) on queue update
   - Recalculates all positions after each token change
   - Acceptable for typical queue sizes (< 100)

2. **Firestore Listeners**: Efficient with indexes
   ```firestore
   Index on: (hospitalId, department, status, priority, createdAt)
   ```

3. **Firebase Storage**: Medical reports cached locally after download

4. **Timer Updates**: UI only, no network calls per second
   - Just local duration calculation

---

### Troubleshooting

#### "No patients waiting" shown on doctor dashboard
- ✓ Check if any tokens with status="waiting" exist in Firestore
- ✓ Verify hospital_id and department match doctor's profile
- ✓ Check Firestore security rules allow read access

#### Timer not updating on patient screen
- ✓ Verify `createdAt` timestamp is correct in token
- ✓ Check device time is synchronized
- ✓ Verify Firestore listener connected (check logs)

#### Medical report upload fails
- ✓ Check Firebase Storage rules allow authenticated upload
- ✓ Verify file is PDF and < 10MB
- ✓ Check network connectivity
- ✓ Verify patient UID matches current user

#### Wait time wrong
- ✓ Verify risk_level is HIGH/MEDIUM/LOW (case-sensitive)
- ✓ Check queue position (position 1 = shortest wait)
- ✓ Verify backend wait time calculation is used

---

**Last Updated**: February 15, 2026

