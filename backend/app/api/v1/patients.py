"""
Patient Management API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
import hashlib

from app.core.database import get_db
from app.models import Patient, Gender
from app.schemas import PatientCreate, PatientResponse, MessageResponse

router = APIRouter()


def hash_identifier(value: str) -> str:
    """Create SHA256 hash of sensitive identifier"""
    return hashlib.sha256(value.encode()).hexdigest()


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new patient"""

    # Check for existing patient by phone or aadhaar
    existing = None
    if patient_data.phone:
        phone_hash = hash_identifier(patient_data.phone)
        result = await db.execute(
            select(Patient).where(Patient.phone_hash == phone_hash)
        )
        existing = result.scalar_one_or_none()

    if existing:
        # Return existing patient
        return existing

    # Create new patient
    patient = Patient(
        age=patient_data.age,
        gender=Gender(patient_data.gender.value),
        pre_existing_conditions=patient_data.pre_existing_conditions,
        district=patient_data.district,
        state=patient_data.state,
        phone_hash=hash_identifier(patient_data.phone) if patient_data.phone else None,
        aadhaar_hash=hash_identifier(patient_data.aadhaar_last_four) if patient_data.aadhaar_last_four else None
    )

    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get patient by ID"""

    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: UUID,
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update patient information"""

    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient.age = patient_data.age
    patient.gender = Gender(patient_data.gender.value)
    patient.pre_existing_conditions = patient_data.pre_existing_conditions
    patient.district = patient_data.district
    patient.state = patient_data.state

    await db.commit()
    await db.refresh(patient)

    return patient


@router.delete("/{patient_id}", response_model=MessageResponse)
async def delete_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a patient record"""

    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    await db.delete(patient)
    await db.commit()

    return MessageResponse(message="Patient deleted successfully")

