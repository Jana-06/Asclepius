"""
Pydantic Schemas for API Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums
class GenderEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "OTHER"


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Patient Schemas
class PatientCreate(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    gender: GenderEnum
    pre_existing_conditions: List[str] = Field(default_factory=list)
    district: Optional[str] = None
    state: Optional[str] = None
    aadhaar_last_four: Optional[str] = Field(None, min_length=4, max_length=4)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{9,14}$")


class PatientResponse(BaseModel):
    id: UUID
    age: int
    gender: GenderEnum
    pre_existing_conditions: List[str]
    district: Optional[str]
    state: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Vitals Schema
class VitalsInput(BaseModel):
    bp_systolic: int = Field(..., ge=60, le=250, description="Systolic blood pressure")
    bp_diastolic: int = Field(..., ge=40, le=150, description="Diastolic blood pressure")
    heart_rate: int = Field(..., ge=30, le=220, description="Heart rate in BPM")
    temperature: float = Field(..., ge=90.0, le=110.0, description="Body temperature in Fahrenheit")
    spo2: int = Field(..., ge=50, le=100, description="Oxygen saturation percentage")
    respiratory_rate: Optional[int] = Field(None, ge=5, le=60)


# Triage Schemas
class TriageRequest(BaseModel):
    patient_id: UUID
    symptoms: List[str] = Field(..., min_length=1, description="List of symptom codes")
    vitals: VitalsInput
    ehr_file_id: Optional[UUID] = None
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None


class FeatureContribution(BaseModel):
    feature: str
    value: Any
    contribution: float
    direction: str  # "positive" or "negative"


class ExplanationOutput(BaseModel):
    top_features: List[FeatureContribution]
    shap_values: Dict[str, float]
    model_confidence: float
    rule_triggered: Optional[str] = None


class HospitalSuggestion(BaseModel):
    hospital_id: UUID
    name: str
    distance_km: Optional[float]
    current_load: float
    estimated_wait_minutes: int
    departments_available: List[str]


class TriageResponse(BaseModel):
    session_id: UUID
    risk_level: RiskLevelEnum
    department: str
    confidence: float
    explanation: ExplanationOutput
    primary_hospital: Optional[HospitalSuggestion]
    alternate_hospitals: List[HospitalSuggestion]
    estimated_wait_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True


class TriageHistoryItem(BaseModel):
    session_id: UUID
    risk_level: RiskLevelEnum
    department: str
    symptoms: List[str]
    created_at: datetime


# Hospital Schemas
class HospitalBase(BaseModel):
    name: str
    code: str
    hospital_type: str
    district: str
    state: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    total_beds: int
    emergency_beds: int
    departments: List[str]
    contact_phone: Optional[str]


class HospitalCreate(HospitalBase):
    pass


class HospitalResponse(HospitalBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DepartmentLoadResponse(BaseModel):
    department: str
    current_patients: int
    max_capacity: int
    load_percentage: float
    avg_wait_minutes: int
    status: str  # "normal", "busy", "critical"


class HospitalLoadResponse(BaseModel):
    hospital_id: UUID
    hospital_name: str
    overall_load: float
    departments: List[DepartmentLoadResponse]
    timestamp: datetime


class AlternateHospitalRequest(BaseModel):
    patient_location_lat: float
    patient_location_lng: float
    required_department: str
    max_distance_km: float = 50.0
    max_results: int = 5


# Outbreak Schemas
class OutbreakTrendResponse(BaseModel):
    id: UUID
    region: str
    symptom_cluster: List[str]
    predicted_condition: Optional[str]
    signal_strength: float
    case_count: int
    trend: str
    detected_at: datetime
    is_active: bool


class OutbreakSummary(BaseModel):
    active_signals: int
    high_priority_regions: List[str]
    top_symptoms: List[Dict[str, Any]]
    trend_data: List[Dict[str, Any]]


# Fairness Schemas
class FairnessMetric(BaseModel):
    demographic: str
    demographic_value: str
    metric_name: str
    metric_value: float
    baseline_value: float
    disparity_detected: bool


class FairnessReportResponse(BaseModel):
    model_version: str
    audit_date: datetime
    overall_fairness_score: float
    metrics: List[FairnessMetric]
    recommendations: List[str]


# EHR Schemas
class EHRUploadResponse(BaseModel):
    document_id: UUID
    file_name: str
    file_type: str
    extracted_conditions: List[str]
    uploaded_at: datetime


# Symptom Reference
class SymptomInfo(BaseModel):
    code: str
    name: str
    category: str
    severity_weight: float
    related_departments: List[str]


# Generic Response
class MessageResponse(BaseModel):
    message: str
    success: bool = True

