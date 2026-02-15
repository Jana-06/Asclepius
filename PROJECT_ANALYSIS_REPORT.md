# SwasthyaFlow AI - Project Analysis & Execution Report

**Generated:** February 14, 2026  
**Project:** SwasthyaFlow AI - AI-Powered Public Healthcare Triage and Hospital Load Optimization System

---

## 📋 Executive Summary

SwasthyaFlow AI is a comprehensive full-stack healthcare platform designed for government hospital deployment in India. It leverages machine learning and AI to provide intelligent patient triage, risk-based token generation, and real-time hospital load optimization.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                                   │
├──────────────────────┬──────────────────────┬──────────────────────────┤
│   Flutter Mobile     │   React Admin        │   Flutter Web            │
│   App (Patient)      │   Dashboard          │   (Patient & Doctor)     │
│   Port: N/A          │   Port: 3000         │   Port: 5000             │
└──────────────────────┴──────────────────────┴──────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    API GATEWAY LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                    FastAPI (Python)                                      │
│                    Port: 8000                                            │
└─────────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                                  │
├──────────────────────┬──────────────────────┬──────────────────────────┤
│   Triage Engine      │   Load Balancer      │   Outbreak Detector      │
│   (ML + Rules)       │   (Hospital Capacity)│   (Cluster Analysis)     │
└──────────────────────┴──────────────────────┴──────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                            │
├──────────────────────┬──────────────────────┬──────────────────────────┤
│   Firebase Firestore │   PostgreSQL         │   Redis Cache            │
│   (Real-time NoSQL)  │   (Structured Data)  │   (Session & Realtime)   │
└──────────────────────┴──────────────────────┴──────────────────────────┘
```

---

## 📦 Project Structure

```
asclepius/
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── api/v1/                  # REST API Endpoints
│   │   │   ├── triage.py            # Triage classification endpoints
│   │   │   ├── hospitals.py         # Hospital management
│   │   │   ├── outbreak.py          # Disease outbreak detection
│   │   │   ├── admin.py             # Admin functionality
│   │   │   ├── patients.py          # Patient management
│   │   │   └── tokens.py            # Token generation
│   │   ├── core/                    # Core configuration
│   │   │   ├── config.py            # Settings management
│   │   │   ├── security.py          # Authentication
│   │   │   └── database.py          # DB connections
│   │   ├── models/                  # SQLAlchemy ORM
│   │   │   ├── patient.py           # Patient model
│   │   │   ├── doctor.py            # Doctor model
│   │   │   ├── hospital.py          # Hospital model
│   │   │   ├── triage_session.py    # Session tracking
│   │   │   └── token.py             # Token model
│   │   ├── schemas/                 # Pydantic validation
│   │   ├── services/                # Business logic
│   │   │   ├── auth_service.py      # Authentication
│   │   │   ├── triage_engine.py     # ML triage logic
│   │   │   ├── hospital_service.py  # Hospital operations
│   │   │   └── outbreak_service.py  # Outbreak detection
│   │   ├── ml/                      # ML Pipeline
│   │   │   ├── models.py            # Model definitions
│   │   │   ├── feature_engineering.py
│   │   │   ├── explainability.py    # SHAP/LIME
│   │   │   ├── fairness.py          # Bias detection
│   │   │   └── synthetic_data.py    # Data generation
│   │   └── main.py                  # Application entry
│   ├── requirements.txt              # Dependencies
│   └── Dockerfile
│
├── lib/                              # Flutter Mobile App
│   ├── main.dart                    # App entry point
│   ├── app/
│   │   ├── app.dart                 # App config & routes
│   │   └── constants.dart           # Constants
│   ├── core/
│   │   ├── theme/
│   │   │   └── app_theme.dart       # Theme configuration
│   │   ├── constants/               # App constants
│   │   └── utils/                   # Utility functions
│   ├── data/
│   │   ├── models/                  # Data models
│   │   └── services/                # API services
│   │       ├── auth_service.dart    # Authentication
│   │       ├── triage_service.dart  # Triage API calls
│   │       └── hospital_service.dart# Hospital API calls
│   ├── features/
│   │   ├── auth/                    # Authentication screens
│   │   │   ├── sign_up_screen.dart  # Patient registration
│   │   │   ├── sign_in_screen.dart  # Login
│   │   │   └── auth_provider.dart   # Auth state
│   │   ├── patient/                 # Patient features
│   │   │   ├── home_screen.dart
│   │   │   ├── triage_screen.dart
│   │   │   └── medical_history.dart
│   │   ├── doctor/                  # Doctor features
│   │   │   ├── dashboard.dart
│   │   │   ├── patient_list.dart
│   │   │   └── consultation.dart
│   │   └── admin/                   # Admin features
│   │       ├── dashboard.dart
│   │       ├── hospital_mgmt.dart
│   │       └── analytics.dart
│   └── shared/                      # Shared widgets
│
├── web-admin/                        # React Admin Dashboard
│   ├── src/
│   │   ├── App.tsx                  # Main app component
│   │   ├── index.css                # Tailwind styles
│   │   ├── components/
│   │   │   ├── Dashboard.tsx        # Main dashboard
│   │   │   ├── HospitalLoad.tsx     # Load monitoring
│   │   │   ├── Analytics.tsx        # Analytics page
│   │   │   ├── OutbreakMap.tsx      # Outbreak visualization
│   │   │   └── AdminPanel.tsx       # Administration
│   │   ├── services/
│   │   │   └── api.ts               # API client
│   │   └── types/
│   │       └── index.ts             # TypeScript types
│   ├── vite.config.ts               # Vite config
│   ├── tailwind.config.js           # Tailwind CSS
│   ├── package.json                 # Dependencies
│   └── public/                      # Static assets
│
├── pubspec.yaml                     # Flutter dependencies
├── pubspec.lock                     # Locked versions
├── firebase.json                    # Firebase config
├── docker-compose.yml               # Container orchestration
└── README.md                        # Documentation
```

---

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (primary), Firebase Firestore (real-time)
- **Caching:** Redis
- **Authentication:** Firebase Auth
- **ML Framework:** Scikit-learn
- **Explainability:** SHAP (SHapley Additive exPlanations), LIME
- **Data Processing:** Pandas, NumPy, SciPy

### Frontend (Flutter)
- **Framework:** Flutter (Dart)
- **State Management:** Provider
- **Firebase:** Cloud Firestore, Firebase Auth, Firebase Storage
- **HTTP Client:** http package
- **Local Storage:** shared_preferences

### Admin Dashboard (React)
- **Framework:** React 18.2
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Date Handling:** date-fns
- **Icons:** Lucide React

### Infrastructure
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **Web Server:** Nginx
- **Cloud:** Firebase (Auth, Firestore, Storage)

---

## 🎯 Core Features

### 1. **AI-Powered Triage System**
- Risk classification: Low, Medium, High
- Hybrid ML + Rule-based approach
- Features: Symptoms, vitals, medical history, demographics
- Output: Risk score, recommended department, urgency level

### 2. **Smart Hospital Finder**
- Real-time department load monitoring
- Capacity-based recommendations
- Alternative hospital suggestions
- Traffic prediction

### 3. **Explainable AI (XAI)**
- SHAP feature contribution analysis
- LIME local explanations
- Transparent decision-making for medical professionals
- Audit trails for compliance

### 4. **Outbreak Detection**
- Symptom cluster analysis (DBSCAN)
- Trend prediction
- Alert generation
- Geographic hotspot mapping

### 5. **Fairness Monitoring**
- Bias detection across demographics
- Gender and age group analysis
- Continuous monitoring dashboard
- Fairness metrics reporting

### 6. **Token-Based Queue Management**
- AI-generated risk-based tokens
- Priority-aware queueing
- Wait time estimation
- Real-time updates

---

## 🚀 Deployment & Running

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
**URL:** http://localhost:8000  
**Docs:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

### Flutter Web App
```bash
flutter pub get
flutter run -d chrome --web-port=5000
```
**URL:** http://localhost:5000

### React Admin Dashboard
```bash
cd web-admin
npm install
npm run dev
```
**URL:** http://localhost:3000

### Docker Deployment
```bash
docker-compose up -d
```

---

## 📊 Database Schema

### Firebase Firestore Collections

#### patients
```
{
  uid: string
  email: string
  name: string
  age: number
  gender: "M" | "F" | "OTHER"
  phone: string
  state: string
  preExistingConditions: string[]
  userType: "patient"
  createdAt: timestamp
  updatedAt: timestamp
}
```

#### triage_sessions
```
{
  id: string
  patientId: string
  symptoms: string[]
  vitals: {
    heartRate: number
    systolicBP: number
    diastolicBP: number
    temperature: number
    respiratoryRate: number
    oxygenSaturation: number
  }
  riskScore: number
  riskLevel: "LOW" | "MEDIUM" | "HIGH"
  recommendedDepartment: string
  explanations: {
    topFeatures: string[]
    topReasons: string[]
  }
  status: "PENDING" | "COMPLETED" | "REVIEWED"
  createdAt: timestamp
  updatedAt: timestamp
}
```

#### doctors
```
{
  uid: string
  email: string
  name: string
  department: string
  hospitalId: string
  specialization: string
  licenseNumber: string
  maxPatientsPerHour: number
  currentPatientCount: number
  isAvailable: boolean
  userType: "doctor"
  createdAt: timestamp
  updatedAt: timestamp
}
```

#### hospitals
```
{
  id: string
  name: string
  address: string
  city: string
  state: string
  latitude: number
  longitude: number
  departments: {
    [dept]: {
      capacity: number
      currentLoad: number
      avgWaitTime: number
      staffCount: number
    }
  }
  totalBeds: number
  occupiedBeds: number
  createdAt: timestamp
  updatedAt: timestamp
}
```

---

## 🔐 Authentication & Security

- **Firebase Authentication:** Email/password, social login
- **JWT Tokens:** Issued for API access
- **CORS:** Configured for frontend domains
- **Rate Limiting:** Endpoint protection
- **Input Validation:** Pydantic schemas
- **Database Security:** Firestore rules, row-level security

---

## 📈 API Endpoints

### Triage Endpoints
- `POST /api/v1/triage/classify` - Classify patient risk
- `GET /api/v1/triage/sessions/{id}` - Get session details
- `GET /api/v1/triage/explanations/{id}` - Get XAI explanation

### Hospital Endpoints
- `GET /api/v1/hospitals` - List hospitals
- `GET /api/v1/hospitals/{id}/load` - Get department load
- `POST /api/v1/hospitals/{id}/allocate` - Allocate patient

### Outbreak Endpoints
- `GET /api/v1/outbreak/alerts` - Get active alerts
- `GET /api/v1/outbreak/clusters` - Get symptom clusters
- `GET /api/v1/outbreak/trends` - Get trend predictions

### Admin Endpoints
- `GET /api/v1/admin/analytics` - System analytics
- `GET /api/v1/admin/fairness` - Fairness metrics
- `POST /api/v1/admin/settings` - Update settings

### Patient Endpoints
- `POST /api/v1/patients/register` - Patient registration
- `GET /api/v1/patients/{id}/history` - Medical history
- `POST /api/v1/patients/{id}/triage` - Start triage

---

## 🎓 Key Implementation Highlights

### 1. **Multi-Step Registration (Flutter)**
- **File:** `lib/features/auth/sign_up_screen.dart`
- **Features:**
  - 3-step stepper form (Personal Info → Health Info → Account Setup)
  - Input validation with error handling
  - Network error detection
  - Firebase integration
  - Responsive design

### 2. **ML Pipeline (Backend)**
- **Hybrid Approach:** ML models + clinical rule engine
- **Features:** Symptom severity scoring, vital sign analysis, medical history
- **Models:** Random Forest, Gradient Boosting, Neural Networks
- **Explainability:** SHAP + LIME for feature importance

### 3. **Real-time Updates (Firebase)**
- **Firestore Listeners:** Real-time data synchronization
- **Firebase Cloud Functions:** Automated triggers
- **Real-time Database:** For queue management

### 4. **Admin Dashboard (React)**
- **Charts:** Hospital load, patient flow, outbreak trends
- **Maps:** Geographic outbreak visualization
- **Analytics:** Fairness metrics, model performance

---

## 🧪 Testing & Quality Assurance

- **Unit Tests:** Pytest for backend
- **Widget Tests:** Flutter testing framework
- **Integration Tests:** End-to-end scenarios
- **ML Validation:** Cross-validation, fairness metrics
- **Performance:** Load testing, latency monitoring

---

## 📦 Dependencies Summary

### Backend (Top Packages)
- fastapi==0.109.0
- sqlalchemy==2.0.25
- firebase-admin==6.4.0
- scikit-learn==1.4.0
- pandas==2.2.0
- shap==0.44.1
- redis==5.0.1

### Frontend (Top Packages)
- flutter (SDK)
- firebase_core: ^3.8.1
- firebase_auth: ^5.3.4
- cloud_firestore: ^5.6.1
- provider: ^6.1.1

### Web Admin (Top Packages)
- react: ^18.2.0
- vite: ^5.0.11
- tailwindcss: ^3.4.1
- axios: ^1.6.5
- recharts: ^2.10.3

---

## 🚨 Current Status

### ✅ Completed
- [x] Project structure setup
- [x] Firebase integration
- [x] Backend API skeleton
- [x] Flutter app setup
- [x] React admin dashboard setup
- [x] Database schema design
- [x] Authentication system

### 🔄 In Progress
- [ ] Backend server startup (Port 8000) - **STARTING**
- [ ] Flutter web app (Port 5000) - **STARTING**
- [ ] React admin dashboard (Port 3000) - **REQUIRES NODE.JS**

### ⏸️ Not Started
- [ ] Node.js installation for web-admin
- [ ] Docker compose orchestration
- [ ] Production deployment

---

## 🔗 Service URLs (Once Running)

| Service | URL | Status |
|---------|-----|--------|
| Backend API | http://localhost:8000 | Starting... |
| API Docs | http://localhost:8000/docs | Starting... |
| Flutter App | http://localhost:5000 | Starting... |
| Admin Dashboard | http://localhost:3000 | Pending Node.js |
| Firebase | asclepius-f664c | Configured |

---

## 📝 Next Steps

1. **Backend Verification:** Ensure FastAPI server starts without errors
2. **Flutter Testing:** Test mobile app on web platform
3. **Node.js Installation:** Install for React admin dashboard
4. **Environment Variables:** Configure .env files for production
5. **Database Migration:** Run PostgreSQL migrations
6. **ML Model Training:** Train triage and outbreak detection models
7. **Integration Testing:** Test API endpoints
8. **Load Testing:** Verify performance under load
9. **Security Audit:** Conduct security review
10. **Deployment:** Set up Docker containers and cloud infrastructure

---

## 🤝 Project Contributors

SwasthyaFlow AI is developed to improve public healthcare delivery in India through AI and machine learning.

---

**Last Updated:** February 14, 2026  
**Project Status:** Development & Testing Phase

