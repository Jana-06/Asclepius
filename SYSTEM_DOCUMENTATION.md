# SwasthyaFlow AI - Smart Patient Triage System

## 🏥 AI-Powered Smart Patient Triage and Hospital Load Optimization

SwasthyaFlow AI is a full-stack healthcare solution that uses AI/ML to provide intelligent patient triage, risk-based token generation, and real-time hospital load optimization for government healthcare systems.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SwasthyaFlow AI Architecture                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  Flutter App    │    │  React Admin    │    │  Firebase Auth  │        │
│  │  (Patient &     │    │  Dashboard      │    │  & Firestore    │        │
│  │   Doctor)       │    │  (Hospital      │    │  (Real-time     │        │
│  │                 │    │   Admin)        │    │   Database)     │        │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘        │
│           │                      │                      │                  │
│           ▼                      ▼                      ▼                  │
│  ┌───────────────────────────────────────────────────────────────┐        │
│  │                     FastAPI Backend (Python)                   │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │        │
│  │  │ Triage API   │  │ Token API    │  │ Hospital API │        │        │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │        │
│  │  │ Outbreak API │  │ Admin API    │  │ Fairness API │        │        │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │        │
│  └───────────────────────────────────────────────────────────────┘        │
│                               │                                            │
│                               ▼                                            │
│  ┌───────────────────────────────────────────────────────────────┐        │
│  │                     ML/AI Engine                               │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │        │
│  │  │ Triage Model │  │ SHAP/LIME    │  │ Rule Engine  │        │        │
│  │  │ (Scikit-     │  │ Explainer    │  │ (Clinical    │        │        │
│  │  │  learn)      │  │              │  │  Rules)      │        │        │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │        │
│  │  │ Outbreak     │  │ Load         │  │ Fairness     │        │        │
│  │  │ Detector     │  │ Balancer     │  │ Monitor      │        │        │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │        │
│  └───────────────────────────────────────────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Firebase Firestore Schema

### Collections Structure

```
firestore/
├── patients/
│   └── {patientId}/
│       ├── uid: string
│       ├── email: string
│       ├── name: string
│       ├── age: number
│       ├── gender: "M" | "F" | "OTHER"
│       ├── phone: string
│       ├── district: string
│       ├── state: string
│       ├── preExistingConditions: string[]
│       ├── userType: "patient"
│       ├── createdAt: timestamp
│       └── updatedAt: timestamp
│
├── doctors/
│   └── {doctorId}/
│       ├── uid: string
│       ├── email: string
│       ├── name: string
│       ├── department: string
│       ├── hospitalId: string
│       ├── specialization: string
│       ├── licenseNumber: string
│       ├── maxPatientsPerHour: number
│       ├── currentPatientCount: number
│       ├── isAvailable: boolean
│       ├── unavailableUntil: timestamp
│       ├── unavailableReason: string
│       ├── userType: "doctor"
│       ├── createdAt: timestamp
│       └── updatedAt: timestamp
│
├── triage_sessions/
│   └── {sessionId}/
│       ├── id: string
│       ├── patientId: string
│       ├── symptoms: string[]
│       ├── vitals: {
│       │   ├── heartRate: number
│       │   ├── systolicBP: number
│       │   ├── diastolicBP: number
│       │   ├── spo2: number
│       │   ├── temperature: number
│       │   └── respiratoryRate: number
│       │   }
│       ├── preExistingConditions: string[]
│       ├── ehrFilePath: string
│       ├── status: "pending" | "processing" | "completed" | "error"
│       ├── riskLevel: "LOW" | "MEDIUM" | "HIGH"
│       ├── department: string
│       ├── confidenceScore: number
│       ├── explanation: {
│       │   ├── top_features: [{feature, value, contribution, direction}]
│       │   ├── shap_values: {feature: value}
│       │   ├── model_confidence: number
│       │   └── rule_triggered: string
│       │   }
│       ├── createdAt: timestamp
│       └── updatedAt: timestamp
│
├── tokens/
│   └── {tokenId}/
│       ├── id: string
│       ├── tokenNumber: number
│       ├── patientId: string
│       ├── sessionId: string
│       ├── riskLevel: "LOW" | "MEDIUM" | "HIGH"
│       ├── department: string
│       ├── hospitalId: string
│       ├── doctorId: string
│       ├── priority: number (calculated)
│       ├── status: "waiting" | "in_progress" | "completed" | "cancelled"
│       ├── queuePosition: number
│       ├── estimatedWaitMinutes: number
│       ├── createdAt: timestamp
│       ├── calledAt: timestamp
│       └── completedAt: timestamp
│
├── hospitals/
│   └── {hospitalId}/
│       ├── id: string
│       ├── name: string
│       ├── code: string
│       ├── hospitalType: "PHC" | "CHC" | "District" | "Tertiary"
│       ├── district: string
│       ├── state: string
│       ├── address: string
│       ├── latitude: number
│       ├── longitude: number
│       ├── totalBeds: number
│       ├── emergencyBeds: number
│       ├── departments: string[]
│       ├── contactPhone: string
│       ├── isActive: boolean
│       ├── createdAt: timestamp
│       └── updatedAt: timestamp
│
└── token_counters/
    └── {hospitalId-department-date}/
        ├── count: number
        └── date: string
```

---

## 🎯 Risk-Based Token Prioritization Algorithm

```python
def calculate_priority(risk_level: str, arrival_time: datetime) -> int:
    """
    Calculate priority score for queue ordering.
    Higher priority = seen first.
    
    Priority Formula:
    priority = (risk_weight * 1000) + time_factor
    
    Risk Weights:
    - HIGH: 100 (100,000 base priority)
    - MEDIUM: 50 (50,000 base priority)
    - LOW: 10 (10,000 base priority)
    
    Time Factor (0-14 points):
    - Earlier arrival within same risk = slightly higher priority
    - Ensures fairness: first-come-first-serve within same risk level
    """
    
    RISK_PRIORITY = {
        'HIGH': 100,
        'MEDIUM': 50,
        'LOW': 10,
    }
    
    base_priority = RISK_PRIORITY.get(risk_level, 10)
    
    # Time factor: earlier = higher (max ~14 points)
    minutes_since_midnight = arrival_time.hour * 60 + arrival_time.minute
    time_factor = (1440 - minutes_since_midnight) // 100
    
    return base_priority * 1000 + time_factor

# Queue Ordering Example:
# Patient A: HIGH risk, arrived 9:00 AM  → Priority: 100,005
# Patient B: HIGH risk, arrived 9:30 AM  → Priority: 100,002
# Patient C: MEDIUM risk, arrived 8:30 AM → Priority: 50,008
# Patient D: LOW risk, arrived 7:00 AM   → Priority: 10,015

# Queue Order: A → B → C → D
```

---

## 🤖 ML Training Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML Training Pipeline                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DATA GENERATION                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Synthetic Data Generator                                 │   │
│  │  • 10,000+ patient records                               │   │
│  │  • Realistic symptom combinations                         │   │
│  │  • Age/gender/condition distributions                     │   │
│  │  • Regional outbreak patterns                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  2. FEATURE ENGINEERING                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • Symptom encoding (multi-hot)                          │   │
│  │  • Vital signs normalization                             │   │
│  │  • Age group binning                                      │   │
│  │  • Condition risk scoring                                 │   │
│  │  • Symptom severity weighting                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  3. MODEL TRAINING                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Random Forest Classifier (Triage)                        │   │
│  │  • Input: symptoms, vitals, age, gender, conditions      │   │
│  │  • Output: LOW / MEDIUM / HIGH risk                      │   │
│  │                                                           │   │
│  │  Random Forest Classifier (Department)                    │   │
│  │  • Input: symptoms, risk level, conditions               │   │
│  │  • Output: Recommended department                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  4. EXPLAINABILITY LAYER                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  SHAP TreeExplainer                                       │   │
│  │  • Feature importance values                              │   │
│  │  • Per-prediction explanations                            │   │
│  │  • Direction of contribution (+ / -)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  5. RULE ENGINE OVERRIDE                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Clinical Safety Rules                                    │   │
│  │  • Chest pain + age > 40 → HIGH + Cardiology             │   │
│  │  • SpO2 < 90% → HIGH + Emergency                         │   │
│  │  • Seizures → HIGH + Neurology                           │   │
│  │  • Pregnancy + bleeding → HIGH + OB/GYN                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Folder Structure

```
asclepius/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/                   # API Endpoints
│   │   │   ├── admin.py
│   │   │   ├── hospitals.py
│   │   │   ├── outbreak.py
│   │   │   ├── patients.py
│   │   │   ├── tokens.py             # Token management
│   │   │   └── triage.py
│   │   ├── core/                     # Core config
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── ml/                       # ML modules
│   │   │   ├── explainer.py          # SHAP explanations
│   │   │   ├── inference.py          # Model inference
│   │   │   ├── synthetic_data.py     # Data generator
│   │   │   └── train.py              # Model training
│   │   ├── models/                   # Database models
│   │   ├── schemas/                  # Pydantic schemas
│   │   └── services/                 # Business logic
│   │       ├── fairness_monitor.py
│   │       ├── load_balancer.py
│   │       ├── outbreak_detector.py
│   │       └── triage_engine.py
│   ├── data/
│   │   ├── models/                   # Trained ML models
│   │   └── synthetic/                # Generated data
│   └── requirements.txt
│
├── lib/                              # Flutter Mobile App
│   ├── app/
│   │   ├── app.dart
│   │   └── routes.dart
│   ├── core/
│   │   ├── constants/
│   │   └── theme/
│   ├── data/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   │       ├── auth_service.dart
│   │       ├── doctor_availability_service.dart
│   │       ├── firebase_service.dart
│   │       ├── token_service.dart
│   │       └── triage_service.dart
│   └── features/
│       ├── auth/                     # Login/Register screens
│       ├── doctor_dashboard/         # Doctor portal
│       ├── hospital_finder/
│       ├── outbreak_alerts/
│       ├── patient_input/            # Patient portal
│       └── triage_result/
│
├── web-admin/                        # React Admin Dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── FairnessPage.tsx
│   │   │   ├── HospitalsPage.tsx
│   │   │   └── OutbreakPage.tsx
│   │   └── services/
│   └── package.json
│
└── docker-compose.yml
```

---

## 🔄 User Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PATIENT FLOW                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ Login/  │───▶│ Enter   │───▶│ Enter   │───▶│ Upload  │      │
│  │Register │    │Symptoms │    │ Vitals  │    │  EHR    │      │
│  └─────────┘    └─────────┘    └─────────┘    └────┬────┘      │
│                                                     │            │
│                                                     ▼            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ Track   │◀───│ Get     │◀───│ View    │◀───│   AI    │      │
│  │ Queue   │    │ Token   │    │ Result  │    │ Triage  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              REAL-TIME QUEUE STATUS                      │    │
│  │  • Token Number: 42                                      │    │
│  │  • Risk Level: MEDIUM                                    │    │
│  │  • Queue Position: #3                                    │    │
│  │  • Estimated Wait: 45 minutes                           │    │
│  │  • Doctor: Dr. Sharma (Available)                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DOCTOR FLOW                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐    ┌─────────────────────────────────────────┐     │
│  │ Login   │───▶│           DOCTOR DASHBOARD               │     │
│  │         │    │  ┌─────────────────────────────────┐    │     │
│  └─────────┘    │  │ Queue Overview                   │    │     │
│                 │  │ • Total Waiting: 15              │    │     │
│                 │  │ • High Risk: 3 🔴               │    │     │
│                 │  │ • Medium Risk: 7 🟡             │    │     │
│                 │  │ • Low Risk: 5 🟢                │    │     │
│                 │  └─────────────────────────────────┘    │     │
│                 │                                          │     │
│                 │  ┌─────────────────────────────────┐    │     │
│                 │  │ [Call Next Patient]              │    │     │
│                 │  └─────────────────────────────────┘    │     │
│                 └────────────────┬────────────────────────┘     │
│                                  │                               │
│                                  ▼                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              PATIENT DETAILS VIEW                        │    │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐   │    │
│  │  │ Patient Info    │  │ AI Explainability Panel     │   │    │
│  │  │ • Name: John    │  │ • Confidence: 87%           │   │    │
│  │  │ • Age: 45       │  │ • Top Factors:              │   │    │
│  │  │ • Gender: M     │  │   - chest_pain: +35%        │   │    │
│  │  │                 │  │   - age > 40: +20%          │   │    │
│  │  │ Vitals:         │  │   - hypertension: +15%      │   │    │
│  │  │ • BP: 150/95    │  │   - fever: -5%              │   │    │
│  │  │ • HR: 92        │  │                             │   │    │
│  │  │ • SpO2: 96%     │  │ [Feature Importance Chart]  │   │    │
│  │  └─────────────────┘  └─────────────────────────────┘   │    │
│  │                                                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ [Complete Consultation]                          │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/patients/register` | Register new patient |
| POST | `/api/v1/auth/login` | Login (patient/doctor) |

### Triage
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/triage/` | Submit triage assessment |
| GET | `/api/v1/triage/{session_id}` | Get triage result |
| GET | `/api/v1/triage/history/{patient_id}` | Get patient history |

### Tokens
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tokens/generate` | Generate risk-based token |
| GET | `/api/v1/tokens/queue/{hospital_id}/{department}` | Get queue |
| GET | `/api/v1/tokens/patient/{patient_id}` | Get patient's token |
| POST | `/api/v1/tokens/call-next/{doctor_id}/{hospital_id}/{department}` | Call next patient |
| POST | `/api/v1/tokens/complete/{token_id}` | Complete consultation |
| GET | `/api/v1/tokens/stats/{hospital_id}/{department}` | Queue statistics |

### Hospitals
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/hospitals/` | List all hospitals |
| GET | `/api/v1/hospitals/nearby` | Find nearby hospitals |
| GET | `/api/v1/hospitals/{hospital_id}/load` | Get hospital load |

### Outbreak Detection
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/outbreak/signals` | Get active outbreak signals |
| GET | `/api/v1/outbreak/trends` | Get symptom trends |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/fairness` | Get fairness audit |
| GET | `/api/v1/admin/stats` | Get system statistics |

---

## 🔒 Edge Case Handling

| Edge Case | Solution |
|-----------|----------|
| Duplicate patient registration | Firebase Auth enforces unique email; check before registration |
| Duplicate doctor accounts | Admin-controlled registration; email uniqueness |
| Same patient multiple tokens | Only allow one active token per patient |
| Doctor goes offline mid-consultation | Auto-reassign after timeout; patient notification |
| Network failure | Firestore offline persistence; sync on reconnect |
| Queue position disputes | Transparent priority algorithm; timestamp logging |
| ML model failure | Rule-based fallback system with clinical safety rules |
| High load on single hospital | Load balancer suggests alternate hospitals |
| Outbreak false positives | Configurable thresholds; manual verification |

---

## 📈 Scalability Strategy for Government Hospitals

### Horizontal Scaling
```
┌─────────────────────────────────────────────────────────────┐
│                   Load Balancer (Nginx)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ API     │    │ API     │    │ API     │
    │ Server 1│    │ Server 2│    │ Server 3│
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         ┌────▼────┐          ┌────▼────┐
         │Firebase │          │ Redis   │
         │Firestore│          │ Cache   │
         └─────────┘          └─────────┘
```

### Regional Deployment
- Deploy backend instances per state/district
- Use Firebase regional databases
- CDN for static assets
- Edge caching for hospital data

### Performance Optimizations
- ML model caching (load once, serve many)
- Database query optimization
- Batch updates for queue positions
- WebSocket for real-time updates

---

## 🏃 Running the Application

### Backend
```bash
cd backend
pip install -r requirements-local.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Web Admin
```bash
cd web-admin
npm install
npm run dev
```

### Flutter App
```bash
flutter pub get
flutter run -d chrome --web-port=8080  # Web
flutter run -d windows                  # Windows
flutter run                             # Connected device
```

---

## 📋 Hackathon File Requirements Checklist

- ✅ **Patient Input Module** - `lib/features/patient_input/`
- ✅ **AI Risk Classification Engine** - `backend/app/services/triage_engine.py`
- ✅ **Department Recommendation Engine** - `backend/app/ml/inference.py`
- ✅ **Explainability Layer** - `backend/app/ml/explainer.py` (SHAP)
- ✅ **Dashboard Interface** - `web-admin/` & `lib/features/doctor_dashboard/`
- ✅ **Firebase Authentication** - `lib/data/services/auth_service.dart`
- ✅ **Real-time Queue System** - `lib/data/services/token_service.dart`
- ✅ **Risk-based Token Algorithm** - `backend/app/api/v1/tokens.py`
- ✅ **Synthetic Data Generator** - `backend/app/ml/synthetic_data.py`
- ✅ **Fairness Monitoring** - `backend/app/services/fairness_monitor.py`
- ✅ **Outbreak Detection** - `backend/app/services/outbreak_detector.py`

---

## 📄 License

MIT License - Built for AI-Powered Smart Patient Triage Hackathon

