"""
Triage API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models import Patient, TriageSession, Hospital, RiskLevel
from app.schemas import (
    TriageRequest, TriageResponse, TriageHistoryItem,
    HospitalSuggestion, ExplanationOutput, FeatureContribution
)
from app.services import triage_engine, load_balancer, outbreak_detector, fairness_monitor

router = APIRouter()


@router.post("/", response_model=TriageResponse)
async def submit_triage(
    triage_data: TriageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Submit patient symptoms for triage assessment"""

    # Get patient information
    result = await db.execute(
        select(Patient).where(Patient.id == triage_data.patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Process triage
    triage_result = await triage_engine.process_triage(
        patient_id=str(patient.id),
        symptoms=triage_data.symptoms,
        vitals=triage_data.vitals.model_dump(),
        age=patient.age,
        gender=patient.gender.value,
        pre_existing_conditions=patient.pre_existing_conditions or []
    )

    # Log for fairness monitoring
    fairness_monitor.log_prediction(
        prediction=triage_result,
        demographics={"gender": patient.gender.value, "age": patient.age}
    )

    # Log for outbreak detection
    outbreak_detector.add_case(
        region=patient.district or patient.state or "Unknown",
        symptoms=triage_data.symptoms,
        timestamp=datetime.utcnow()
    )

    # Get hospital suggestions
    hospitals_result = await db.execute(select(Hospital).where(Hospital.is_active == True).limit(20))
    hospitals = [
        {
            "id": str(h.id),
            "name": h.name,
            "hospital_type": h.hospital_type,
            "departments": h.departments or [],
            "latitude": h.latitude,
            "longitude": h.longitude,
            "address": h.address,
            "contact_phone": h.contact_phone
        }
        for h in hospitals_result.scalars().all()
    ]

    # Get alternate hospitals if needed
    primary_hospital = None
    alternate_hospitals = []
    estimated_wait = 15

    if hospitals and triage_data.location_latitude and triage_data.location_longitude:
        suggestions = load_balancer.suggest_alternate_hospitals(
            patient_lat=triage_data.location_latitude,
            patient_lng=triage_data.location_longitude,
            required_department=triage_result["department"],
            hospitals=hospitals,
            max_results=5
        )

        if suggestions:
            primary_hospital = HospitalSuggestion(
                hospital_id=UUID(suggestions[0]["hospital_id"]),
                name=suggestions[0]["name"],
                distance_km=suggestions[0]["distance_km"],
                current_load=suggestions[0]["current_load"],
                estimated_wait_minutes=suggestions[0]["estimated_wait_minutes"],
                departments_available=suggestions[0]["departments_available"]
            )
            estimated_wait = suggestions[0]["estimated_wait_minutes"]

            alternate_hospitals = [
                HospitalSuggestion(
                    hospital_id=UUID(s["hospital_id"]),
                    name=s["name"],
                    distance_km=s["distance_km"],
                    current_load=s["current_load"],
                    estimated_wait_minutes=s["estimated_wait_minutes"],
                    departments_available=s["departments_available"]
                )
                for s in suggestions[1:]
            ]

    # Build explanation
    explanation = ExplanationOutput(
        top_features=[
            FeatureContribution(**f) for f in triage_result["explanation"].get("top_features", [])
        ],
        shap_values=triage_result["explanation"].get("shap_values", {}),
        model_confidence=triage_result["confidence"],
        rule_triggered=triage_result.get("rule_triggered")
    )

    # Save triage session
    session = TriageSession(
        patient_id=patient.id,
        symptoms=triage_data.symptoms,
        vitals=triage_data.vitals.model_dump(),
        risk_level=RiskLevel(triage_result["risk_level"]),
        recommended_department=triage_result["department"],
        confidence_score=triage_result["confidence"],
        shap_values=triage_result["explanation"].get("shap_values"),
        top_features=triage_result["explanation"].get("top_features"),
        estimated_wait_minutes=estimated_wait
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return TriageResponse(
        session_id=session.id,
        risk_level=triage_result["risk_level"],
        department=triage_result["department"],
        confidence=triage_result["confidence"],
        explanation=explanation,
        primary_hospital=primary_hospital,
        alternate_hospitals=alternate_hospitals,
        estimated_wait_minutes=estimated_wait,
        created_at=session.created_at
    )


@router.get("/{session_id}/explain")
async def get_explanation(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed explanation for a triage session"""

    result = await db.execute(
        select(TriageSession).where(TriageSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Triage session not found"
        )

    return {
        "session_id": session.id,
        "risk_level": session.risk_level.value,
        "department": session.recommended_department,
        "confidence": session.confidence_score,
        "top_features": session.top_features or [],
        "shap_values": session.shap_values or {},
        "symptoms": session.symptoms,
        "vitals": session.vitals,
        "created_at": session.created_at.isoformat()
    }


@router.get("/history/{patient_id}", response_model=List[TriageHistoryItem])
async def get_triage_history(
    patient_id: UUID,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get triage history for a patient"""

    result = await db.execute(
        select(TriageSession)
        .where(TriageSession.patient_id == patient_id)
        .order_by(TriageSession.created_at.desc())
        .limit(limit)
    )
    sessions = result.scalars().all()

    return [
        TriageHistoryItem(
            session_id=s.id,
            risk_level=s.risk_level.value,
            department=s.recommended_department,
            symptoms=s.symptoms,
            created_at=s.created_at
        )
        for s in sessions
    ]

