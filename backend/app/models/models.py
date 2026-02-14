"""
SQLAlchemy Database Models
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base
from app.core.config import settings


class Gender(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "OTHER"


class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


def generate_uuid():
    return str(uuid.uuid4())


class Patient(Base):
    """Patient information table"""
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    aadhaar_hash = Column(String(64), unique=True, nullable=True, index=True)
    phone_hash = Column(String(64), unique=True, nullable=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    pre_existing_conditions = Column(JSON, default=list)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    triage_sessions = relationship("TriageSession", back_populates="patient")


class TriageSession(Base):
    """Individual triage session records"""
    __tablename__ = "triage_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    symptoms = Column(JSON, nullable=False)  # List of symptom codes
    vitals = Column(JSON, nullable=False)  # BP, HR, SpO2, Temp
    ehr_file_path = Column(String(500), nullable=True)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    recommended_department = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    shap_values = Column(JSON, nullable=True)  # Feature importance values
    top_features = Column(JSON, nullable=True)  # Top contributing features
    hospital_id = Column(String(36), ForeignKey("hospitals.id"), nullable=True)
    estimated_wait_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="triage_sessions")
    hospital = relationship("Hospital")


class Hospital(Base):
    """Government hospital information"""
    __tablename__ = "hospitals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)  # Hospital code
    hospital_type = Column(String(50), nullable=False)  # PHC, CHC, District, Tertiary
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    total_beds = Column(Integer, default=0)
    emergency_beds = Column(Integer, default=0)
    departments = Column(JSON, default=list)  # List of available departments
    contact_phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department_loads = relationship("DepartmentLoad", back_populates="hospital")


class DepartmentLoad(Base):
    """Real-time department load tracking"""
    __tablename__ = "department_load"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    hospital_id = Column(String(36), ForeignKey("hospitals.id"), nullable=False)
    department = Column(String(100), nullable=False)
    current_patients = Column(Integer, default=0)
    max_capacity = Column(Integer, nullable=False)
    avg_wait_minutes = Column(Integer, default=0)
    load_percentage = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    hospital = relationship("Hospital", back_populates="department_loads")


class OutbreakSignal(Base):
    """Detected outbreak signals from symptom clustering"""
    __tablename__ = "outbreak_signals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    symptom_cluster = Column(JSON, nullable=False)  # Symptoms in cluster
    region = Column(String(100), nullable=False)  # District/State
    signal_strength = Column(Float, nullable=False)  # 0.0 to 1.0
    case_count = Column(Integer, default=0)
    trend = Column(String(20), nullable=True)  # INCREASING, STABLE, DECREASING
    predicted_condition = Column(String(100), nullable=True)  # e.g., "Dengue-like"
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)


class FairnessAudit(Base):
    """Fairness and bias monitoring audit records"""
    __tablename__ = "fairness_audits"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_version = Column(String(50), nullable=False)
    audit_date = Column(DateTime, default=datetime.utcnow)
    demographic = Column(String(50), nullable=False)  # gender, age_group
    demographic_value = Column(String(50), nullable=False)  # M, F, 0-18, 19-45, etc.
    metric_name = Column(String(50), nullable=False)  # demographic_parity, equalized_odds
    metric_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=True)
    disparity_detected = Column(Boolean, default=False)
    details = Column(JSON, nullable=True)


class EHRDocument(Base):
    """Electronic Health Record document metadata"""
    __tablename__ = "ehr_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # PDF, IMAGE, DICOM
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False)
    extracted_text = Column(Text, nullable=True)  # OCR extracted text
    extracted_data = Column(JSON, nullable=True)  # Parsed medical data
    uploaded_at = Column(DateTime, default=datetime.utcnow)

