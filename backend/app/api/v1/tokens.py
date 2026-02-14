"""
Token Management API Endpoints
Risk-based dynamic token generation and queue management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

from app.core.database import get_db

router = APIRouter()


# Pydantic Models
class TokenRequest(BaseModel):
    patient_id: str
    session_id: str
    risk_level: str
    department: str
    hospital_id: str
    doctor_id: Optional[str] = None


class TokenResponse(BaseModel):
    id: str
    token_number: int
    patient_id: str
    session_id: str
    risk_level: str
    department: str
    hospital_id: str
    doctor_id: Optional[str]
    priority: int
    status: str
    queue_position: int
    estimated_wait_minutes: int
    created_at: datetime


class QueueStatsResponse(BaseModel):
    total_waiting: int
    high_risk: int
    medium_risk: int
    low_risk: int
    estimated_wait_minutes: int


# Risk level priority weights
RISK_PRIORITY = {
    'HIGH': 100,
    'MEDIUM': 50,
    'LOW': 10,
}

# In-memory token storage (use Redis/Firestore in production)
tokens_db = {}
token_counters = {}


def calculate_priority(risk_level: str, arrival_time: datetime) -> int:
    """Calculate priority score based on risk level and arrival time"""
    base_priority = RISK_PRIORITY.get(risk_level, 10)

    # Add time-based factor (earlier arrival = slightly higher priority within same risk)
    minutes_since_midnight = arrival_time.hour * 60 + arrival_time.minute
    time_factor = (1440 - minutes_since_midnight) // 100  # Max ~14 points

    return base_priority * 1000 + time_factor


def get_next_token_number(hospital_id: str, department: str, date: datetime) -> int:
    """Get next token number for the day"""
    date_str = date.strftime('%Y-%m-%d')
    key = f"{hospital_id}-{department}-{date_str}"

    if key not in token_counters:
        token_counters[key] = 0

    token_counters[key] += 1
    return token_counters[key]


def update_queue_positions(hospital_id: str, department: str):
    """Update queue positions for all waiting tokens in a department"""
    # Get all waiting tokens for this department
    waiting_tokens = [
        t for t in tokens_db.values()
        if t['hospital_id'] == hospital_id
        and t['department'] == department
        and t['status'] == 'waiting'
    ]

    # Sort by priority (descending) and creation time
    waiting_tokens.sort(key=lambda x: (-x['priority'], x['created_at']))

    # Update positions
    for i, token in enumerate(waiting_tokens):
        token['queue_position'] = i + 1
        token['estimated_wait_minutes'] = (i + 1) * 15  # 15 min per patient


@router.post("/generate", response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    """Generate a risk-based token for a patient"""

    now = datetime.utcnow()
    token_number = get_next_token_number(request.hospital_id, request.department, now)
    priority = calculate_priority(request.risk_level, now)

    token = {
        'id': str(uuid4()),
        'token_number': token_number,
        'patient_id': request.patient_id,
        'session_id': request.session_id,
        'risk_level': request.risk_level,
        'department': request.department,
        'hospital_id': request.hospital_id,
        'doctor_id': request.doctor_id,
        'priority': priority,
        'status': 'waiting',
        'queue_position': 0,
        'estimated_wait_minutes': 0,
        'created_at': now,
        'called_at': None,
        'completed_at': None,
    }

    tokens_db[token['id']] = token

    # Update queue positions
    update_queue_positions(request.hospital_id, request.department)

    return TokenResponse(
        id=token['id'],
        token_number=token['token_number'],
        patient_id=token['patient_id'],
        session_id=token['session_id'],
        risk_level=token['risk_level'],
        department=token['department'],
        hospital_id=token['hospital_id'],
        doctor_id=token['doctor_id'],
        priority=token['priority'],
        status=token['status'],
        queue_position=token['queue_position'],
        estimated_wait_minutes=token['estimated_wait_minutes'],
        created_at=token['created_at'],
    )


@router.get("/queue/{hospital_id}/{department}", response_model=List[TokenResponse])
async def get_queue(hospital_id: str, department: str):
    """Get the waiting queue for a department"""

    waiting_tokens = [
        t for t in tokens_db.values()
        if t['hospital_id'] == hospital_id
        and t['department'] == department
        and t['status'] == 'waiting'
    ]

    # Sort by priority (descending) and creation time
    waiting_tokens.sort(key=lambda x: (-x['priority'], x['created_at']))

    return [
        TokenResponse(
            id=t['id'],
            token_number=t['token_number'],
            patient_id=t['patient_id'],
            session_id=t['session_id'],
            risk_level=t['risk_level'],
            department=t['department'],
            hospital_id=t['hospital_id'],
            doctor_id=t['doctor_id'],
            priority=t['priority'],
            status=t['status'],
            queue_position=t['queue_position'],
            estimated_wait_minutes=t['estimated_wait_minutes'],
            created_at=t['created_at'],
        )
        for t in waiting_tokens
    ]


@router.get("/patient/{patient_id}", response_model=Optional[TokenResponse])
async def get_patient_token(patient_id: str):
    """Get current token for a patient"""

    active_tokens = [
        t for t in tokens_db.values()
        if t['patient_id'] == patient_id
        and t['status'] in ['waiting', 'in_progress']
    ]

    if not active_tokens:
        return None

    # Return most recent token
    token = max(active_tokens, key=lambda x: x['created_at'])

    return TokenResponse(
        id=token['id'],
        token_number=token['token_number'],
        patient_id=token['patient_id'],
        session_id=token['session_id'],
        risk_level=token['risk_level'],
        department=token['department'],
        hospital_id=token['hospital_id'],
        doctor_id=token['doctor_id'],
        priority=token['priority'],
        status=token['status'],
        queue_position=token['queue_position'],
        estimated_wait_minutes=token['estimated_wait_minutes'],
        created_at=token['created_at'],
    )


@router.post("/call-next/{doctor_id}/{hospital_id}/{department}", response_model=Optional[TokenResponse])
async def call_next_patient(doctor_id: str, hospital_id: str, department: str):
    """Call the next patient in queue (for doctors)"""

    waiting_tokens = [
        t for t in tokens_db.values()
        if t['hospital_id'] == hospital_id
        and t['department'] == department
        and t['status'] == 'waiting'
    ]

    if not waiting_tokens:
        return None

    # Sort by priority (descending) and creation time
    waiting_tokens.sort(key=lambda x: (-x['priority'], x['created_at']))

    # Get highest priority token
    token = waiting_tokens[0]
    token['status'] = 'in_progress'
    token['doctor_id'] = doctor_id
    token['called_at'] = datetime.utcnow()

    # Update queue positions
    update_queue_positions(hospital_id, department)

    return TokenResponse(
        id=token['id'],
        token_number=token['token_number'],
        patient_id=token['patient_id'],
        session_id=token['session_id'],
        risk_level=token['risk_level'],
        department=token['department'],
        hospital_id=token['hospital_id'],
        doctor_id=token['doctor_id'],
        priority=token['priority'],
        status=token['status'],
        queue_position=0,
        estimated_wait_minutes=0,
        created_at=token['created_at'],
    )


@router.post("/complete/{token_id}")
async def complete_token(token_id: str):
    """Mark a token as completed"""

    if token_id not in tokens_db:
        raise HTTPException(status_code=404, detail="Token not found")

    token = tokens_db[token_id]
    token['status'] = 'completed'
    token['completed_at'] = datetime.utcnow()

    return {"message": "Token completed", "id": token_id}


@router.post("/cancel/{token_id}")
async def cancel_token(token_id: str):
    """Cancel a token"""

    if token_id not in tokens_db:
        raise HTTPException(status_code=404, detail="Token not found")

    token = tokens_db[token_id]
    old_hospital = token['hospital_id']
    old_department = token['department']

    token['status'] = 'cancelled'

    # Update queue positions
    update_queue_positions(old_hospital, old_department)

    return {"message": "Token cancelled", "id": token_id}


@router.get("/stats/{hospital_id}/{department}", response_model=QueueStatsResponse)
async def get_queue_stats(hospital_id: str, department: str):
    """Get queue statistics for a department"""

    waiting_tokens = [
        t for t in tokens_db.values()
        if t['hospital_id'] == hospital_id
        and t['department'] == department
        and t['status'] == 'waiting'
    ]

    high_risk = sum(1 for t in waiting_tokens if t['risk_level'] == 'HIGH')
    medium_risk = sum(1 for t in waiting_tokens if t['risk_level'] == 'MEDIUM')
    low_risk = sum(1 for t in waiting_tokens if t['risk_level'] == 'LOW')

    return QueueStatsResponse(
        total_waiting=len(waiting_tokens),
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        estimated_wait_minutes=len(waiting_tokens) * 15,
    )

