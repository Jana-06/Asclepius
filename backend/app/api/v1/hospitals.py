"""
Hospital Management API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
import json

from app.core.database import get_db
from app.models import Hospital, DepartmentLoad
from app.schemas import (
    HospitalCreate, HospitalResponse, HospitalLoadResponse,
    DepartmentLoadResponse, AlternateHospitalRequest, HospitalSuggestion,
    MessageResponse
)
from app.services import load_balancer

router = APIRouter()


@router.get("/", response_model=List[HospitalResponse])
async def list_hospitals(
    state: Optional[str] = None,
    district: Optional[str] = None,
    hospital_type: Optional[str] = None,
    department: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List hospitals with optional filters"""

    query = select(Hospital).where(Hospital.is_active == True)

    if state:
        query = query.where(Hospital.state == state)
    if district:
        query = query.where(Hospital.district == district)
    if hospital_type:
        query = query.where(Hospital.hospital_type == hospital_type)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    hospitals = result.scalars().all()

    # Filter by department if specified
    if department:
        hospitals = [
            h for h in hospitals
            if department in (h.departments or [])
        ]

    return hospitals


@router.post("/", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    hospital_data: HospitalCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new hospital"""

    # Check for duplicate code
    result = await db.execute(
        select(Hospital).where(Hospital.code == hospital_data.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hospital code already exists"
        )

    hospital = Hospital(
        name=hospital_data.name,
        code=hospital_data.code,
        hospital_type=hospital_data.hospital_type,
        district=hospital_data.district,
        state=hospital_data.state,
        address=hospital_data.address,
        latitude=hospital_data.latitude,
        longitude=hospital_data.longitude,
        total_beds=hospital_data.total_beds,
        emergency_beds=hospital_data.emergency_beds,
        departments=hospital_data.departments,
        contact_phone=hospital_data.contact_phone
    )

    db.add(hospital)
    await db.commit()
    await db.refresh(hospital)

    return hospital


@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(
    hospital_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get hospital by ID"""

    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)
    )
    hospital = result.scalar_one_or_none()

    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    return hospital


@router.get("/{hospital_id}/load", response_model=HospitalLoadResponse)
async def get_hospital_load(
    hospital_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get real-time department load for a hospital"""

    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)
    )
    hospital = result.scalar_one_or_none()

    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    # Get load data from load balancer
    load_data = load_balancer.get_hospital_load(str(hospital_id))

    departments = [
        DepartmentLoadResponse(
            department=d["department"],
            current_patients=d["current_patients"],
            max_capacity=d["max_capacity"],
            load_percentage=d["load_percentage"],
            avg_wait_minutes=d["avg_wait_minutes"],
            status=d["status"]
        )
        for d in load_data["departments"]
    ]

    return HospitalLoadResponse(
        hospital_id=hospital_id,
        hospital_name=hospital.name,
        overall_load=load_data["overall_load"],
        departments=departments,
        timestamp=load_data["timestamp"]
    )


@router.post("/suggest", response_model=List[HospitalSuggestion])
async def suggest_alternate_hospitals(
    request: AlternateHospitalRequest,
    db: AsyncSession = Depends(get_db)
):
    """Get alternate hospital suggestions based on location and department"""

    # Get all active hospitals with required department
    result = await db.execute(
        select(Hospital).where(Hospital.is_active == True)
    )
    hospitals = result.scalars().all()

    hospital_dicts = [
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
        for h in hospitals
    ]

    suggestions = load_balancer.suggest_alternate_hospitals(
        patient_lat=request.patient_location_lat,
        patient_lng=request.patient_location_lng,
        required_department=request.required_department,
        hospitals=hospital_dicts,
        max_distance_km=request.max_distance_km,
        max_results=request.max_results
    )

    return [
        HospitalSuggestion(
            hospital_id=UUID(s["hospital_id"]),
            name=s["name"],
            distance_km=s["distance_km"],
            current_load=s["current_load"],
            estimated_wait_minutes=s["estimated_wait_minutes"],
            departments_available=s["departments_available"]
        )
        for s in suggestions
    ]


@router.put("/{hospital_id}/load")
async def update_department_load(
    hospital_id: UUID,
    department: str,
    current_patients: int,
    max_capacity: int,
    db: AsyncSession = Depends(get_db)
):
    """Update department load (for simulation/real-time updates)"""

    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id)
    )
    hospital = result.scalar_one_or_none()

    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    load_balancer.update_load(
        str(hospital_id), department, current_patients, max_capacity
    )

    return {"message": "Load updated successfully"}

