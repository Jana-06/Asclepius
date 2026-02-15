# SwasthyaFlow AI

**AI-Powered Public Healthcare Triage and Hospital Load Optimization System**

A comprehensive full-stack healthcare platform designed for government hospital deployment in India. SwasthyaFlow AI uses machine learning to classify patient risk levels, recommend appropriate departments, and optimize hospital resource allocation.

---

## 🏥 System Overview

### Key Features

- **AI-Powered Triage**: Classify patients into Low/Medium/High risk using hybrid ML + rule-based models
- **Explainable AI**: SHAP-based feature contribution analysis for transparent decision-making
- **Smart Hospital Finder**: Real-time department load monitoring with alternate hospital suggestions
- **Outbreak Detection**: Symptom cluster analysis and trend prediction using DBSCAN clustering
- **Fairness Monitoring**: Continuous bias detection across gender and age demographics

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
├─────────────────────────────┬───────────────────────────────────────────────┤
│     Flutter Mobile App      │           React Admin Dashboard                │
│  (Patient-facing triage)    │    (Hospital management & monitoring)          │
└─────────────────────────────┴───────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY (FastAPI)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  /api/v1/patients  │  /api/v1/triage  │  /api/v1/hospitals  │  /api/v1/admin │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
┌───────────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐
│    Triage Engine      │  │   Load Balancer     │  │   Outbreak Detector     │
│  (ML + Rule Engine)   │  │ (Hospital capacity) │  │  (Cluster analysis)     │
└───────────────────────┘  └─────────────────────┘  └─────────────────────────┘
            │                         │                         │
            └─────────────────────────┼─────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               DATA LAYER                                     │
├─────────────────────┬─────────────────────┬─────────────────────────────────┤
│   PostgreSQL        │      Redis          │           MinIO                  │
│  (Structured data)  │  (Cache & realtime) │     (EHR documents)             │
└─────────────────────┴─────────────────────┴─────────────────────────────────┘
```

---

## 📁 Project Structure

```
swasthyaflow-ai/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── api/v1/            # REST API endpoints
│   │   ├── core/              # Configuration & security
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic validation
│   │   ├── services/          # Business logic
│   │   └── ml/                # Machine Learning pipeline
│   ├── data/
│   │   ├── models/            # Trained model artifacts
│   │   └── synthetic/         # Generated datasets
│   ├── requirements.txt
│   └── Dockerfile
│
├── lib/                        # Flutter Mobile App
│   ├── app/                   # App configuration & routes
│   ├── core/                  # Theme, constants, utils
│   ├── data/                  # Models, services
│   └── features/              # Feature modules
│
├── web-admin/                  # React Admin Dashboard
│   └── src/
│
└── docker-compose.yml          # Container orchestration
```

---

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.ml.synthetic_data  # Generate data
python -m app.ml.train           # Train models
uvicorn app.main:app --reload
```

### Flutter App
```bash
flutter pub get
flutter run
```

### React Admin
```bash
cd web-admin
npm install
npm run dev
```

### Docker
```bash
docker-compose up -d
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/patients` | POST | Register patient |
| `/api/v1/triage` | POST | Submit triage |
| `/api/v1/triage/{id}/explain` | GET | Get AI explanation |
| `/api/v1/hospitals` | GET | List hospitals |
| `/api/v1/hospitals/suggest` | POST | Get suggestions |
| `/api/v1/outbreak/trends` | GET | Outbreak signals |
| `/api/v1/admin/fairness-report` | GET | Fairness metrics |

---

## 🤖 ML Pipeline

- **Model**: Random Forest + Clinical Rule Engine
- **Explainability**: SHAP TreeExplainer
- **Outbreak Detection**: DBSCAN clustering
- **Fairness**: Demographic parity monitoring

---

**Built with ❤️ for public healthcare in India**
