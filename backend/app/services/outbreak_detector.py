"""
Outbreak Detection Service
Detects symptom clusters and predicts outbreak trends
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from dataclasses import dataclass

from app.core.config import settings


@dataclass
class OutbreakSignal:
    """Outbreak signal data class"""
    id: str
    region: str
    symptom_cluster: List[str]
    case_count: int
    signal_strength: float
    trend: str
    predicted_condition: Optional[str]
    detected_at: datetime
    is_active: bool


class OutbreakDetector:
    """Detect symptom clusters and outbreak patterns"""

    # Known disease symptom patterns
    DISEASE_PATTERNS = {
        "dengue": {
            "symptoms": ["fever", "headache", "body_ache", "rash", "joint_pain", "fatigue"],
            "min_match": 4,
            "seasonality": ["monsoon", "post_monsoon"]
        },
        "influenza": {
            "symptoms": ["fever", "cough", "sore_throat", "body_ache", "fatigue", "headache"],
            "min_match": 4,
            "seasonality": ["winter"]
        },
        "gastroenteritis": {
            "symptoms": ["diarrhea", "vomiting", "abdominal_pain", "nausea", "fever"],
            "min_match": 3,
            "seasonality": ["summer", "monsoon"]
        },
        "respiratory_infection": {
            "symptoms": ["cough", "fever", "breathlessness", "chest_congestion", "sore_throat"],
            "min_match": 3,
            "seasonality": ["winter", "post_winter"]
        },
        "malaria": {
            "symptoms": ["fever", "chills", "headache", "body_ache", "fatigue", "nausea"],
            "min_match": 4,
            "seasonality": ["monsoon", "post_monsoon"]
        }
    }

    def __init__(self):
        # In-memory storage for demo
        self._case_data: Dict[str, List[Dict]] = defaultdict(list)
        self._active_signals: List[OutbreakSignal] = []
        self._last_analysis: Optional[datetime] = None

    def add_case(self, region: str, symptoms: List[str], timestamp: datetime):
        """Add a new case for outbreak monitoring"""

        self._case_data[region].append({
            "symptoms": symptoms,
            "timestamp": timestamp
        })

        # Trigger analysis if enough time has passed
        if (self._last_analysis is None or
            (datetime.utcnow() - self._last_analysis).total_seconds() > 3600):
            self.analyze_all_regions()

    def analyze_region(self, region: str) -> List[OutbreakSignal]:
        """Analyze cases in a region for outbreak patterns"""

        signals = []
        cases = self._case_data.get(region, [])

        if len(cases) < settings.OUTBREAK_CLUSTER_MIN_SIZE:
            return signals

        # Filter recent cases
        time_window = datetime.utcnow() - timedelta(hours=settings.OUTBREAK_TIME_WINDOW_HOURS)
        recent_cases = [c for c in cases if c["timestamp"] > time_window]

        if len(recent_cases) < settings.OUTBREAK_CLUSTER_MIN_SIZE:
            return signals

        # Count symptom frequencies
        symptom_counts = defaultdict(int)
        for case in recent_cases:
            for symptom in case["symptoms"]:
                symptom_counts[symptom] += 1

        # Find dominant symptom clusters
        total_cases = len(recent_cases)
        dominant_symptoms = [
            symptom for symptom, count in symptom_counts.items()
            if count / total_cases > 0.3  # Present in >30% of cases
        ]

        if len(dominant_symptoms) < 3:
            return signals

        # Match against known disease patterns
        predicted_condition = None
        best_match_score = 0

        for disease, pattern in self.DISEASE_PATTERNS.items():
            matching = set(dominant_symptoms) & set(pattern["symptoms"])
            if len(matching) >= pattern["min_match"]:
                match_score = len(matching) / len(pattern["symptoms"])
                if match_score > best_match_score:
                    best_match_score = match_score
                    predicted_condition = disease

        # Calculate signal strength
        signal_strength = self._calculate_signal_strength(
            case_count=len(recent_cases),
            symptom_overlap=len(dominant_symptoms),
            match_score=best_match_score
        )

        # Determine trend
        trend = self._calculate_trend(recent_cases)

        # Create signal if strength is significant
        if signal_strength > 0.3:
            signal = OutbreakSignal(
                id=f"{region}_{datetime.utcnow().strftime('%Y%m%d%H')}",
                region=region,
                symptom_cluster=dominant_symptoms,
                case_count=len(recent_cases),
                signal_strength=signal_strength,
                trend=trend,
                predicted_condition=predicted_condition,
                detected_at=datetime.utcnow(),
                is_active=True
            )
            signals.append(signal)

        return signals

    def _calculate_signal_strength(self, case_count: int,
                                    symptom_overlap: int,
                                    match_score: float) -> float:
        """Calculate outbreak signal strength (0-1)"""

        # Factors: case count, symptom overlap, disease pattern match
        count_factor = min(case_count / 50, 1.0)  # Normalize to 50 cases
        overlap_factor = min(symptom_overlap / 6, 1.0)  # Normalize to 6 symptoms

        # Weighted combination
        strength = (0.4 * count_factor +
                   0.3 * overlap_factor +
                   0.3 * match_score)

        return round(strength, 3)

    def _calculate_trend(self, cases: List[Dict]) -> str:
        """Calculate trend from case timeline"""

        if len(cases) < 5:
            return "STABLE"

        # Split into halves
        sorted_cases = sorted(cases, key=lambda x: x["timestamp"])
        mid = len(sorted_cases) // 2

        first_half = len(sorted_cases[:mid])
        second_half = len(sorted_cases[mid:])

        ratio = second_half / first_half if first_half > 0 else 1

        if ratio > 1.5:
            return "INCREASING"
        elif ratio < 0.7:
            return "DECREASING"
        else:
            return "STABLE"

    def analyze_all_regions(self) -> List[OutbreakSignal]:
        """Analyze all regions for outbreaks"""

        all_signals = []

        for region in self._case_data.keys():
            signals = self.analyze_region(region)
            all_signals.extend(signals)

        # Update active signals
        self._active_signals = all_signals
        self._last_analysis = datetime.utcnow()

        return all_signals

    def get_active_signals(self) -> List[Dict[str, Any]]:
        """Get all active outbreak signals"""

        return [
            {
                "id": s.id,
                "region": s.region,
                "symptom_cluster": s.symptom_cluster,
                "case_count": s.case_count,
                "signal_strength": s.signal_strength,
                "trend": s.trend,
                "predicted_condition": s.predicted_condition,
                "detected_at": s.detected_at.isoformat(),
                "is_active": s.is_active
            }
            for s in self._active_signals
        ]

    def get_summary(self) -> Dict[str, Any]:
        """Get outbreak summary"""

        active = [s for s in self._active_signals if s.is_active]

        # High priority regions (signal strength > 0.6)
        high_priority = [s.region for s in active if s.signal_strength > 0.6]

        # Top symptoms across all signals
        symptom_counts = defaultdict(int)
        for signal in active:
            for symptom in signal.symptom_cluster:
                symptom_counts[symptom] += 1

        top_symptoms = sorted(
            [{"symptom": s, "frequency": c} for s, c in symptom_counts.items()],
            key=lambda x: x["frequency"],
            reverse=True
        )[:10]

        # Trend data by date
        trend_data = self._generate_trend_data()

        return {
            "active_signals": len(active),
            "high_priority_regions": high_priority,
            "top_symptoms": top_symptoms,
            "trend_data": trend_data,
            "last_analysis": self._last_analysis.isoformat() if self._last_analysis else None
        }

    def _generate_trend_data(self) -> List[Dict[str, Any]]:
        """Generate trend data for visualization"""

        # Generate mock trend data for last 7 days
        trend_data = []
        base_date = datetime.utcnow()

        for i in range(7, 0, -1):
            date = base_date - timedelta(days=i)
            trend_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "total_cases": int(100 + np.random.normal(0, 20)),
                "high_risk_cases": int(20 + np.random.normal(0, 5)),
                "outbreak_signals": int(np.random.poisson(2))
            })

        return trend_data

    def simulate_outbreak_data(self, regions: List[str], days: int = 30):
        """Generate simulated outbreak data for demo"""

        for region in regions:
            for day in range(days):
                timestamp = datetime.utcnow() - timedelta(days=day)

                # Random number of cases per day
                n_cases = np.random.poisson(5)

                for _ in range(n_cases):
                    # Random symptoms with clustering
                    if np.random.random() < 0.3:  # 30% chance of outbreak-like cluster
                        pattern = np.random.choice(list(self.DISEASE_PATTERNS.keys()))
                        symptoms = list(np.random.choice(
                            self.DISEASE_PATTERNS[pattern]["symptoms"],
                            size=np.random.randint(3, 6),
                            replace=False
                        ))
                    else:
                        all_symptoms = ["fever", "cough", "headache", "body_ache",
                                       "fatigue", "nausea", "dizziness"]
                        symptoms = list(np.random.choice(
                            all_symptoms,
                            size=np.random.randint(2, 5),
                            replace=False
                        ))

                    self._case_data[region].append({
                        "symptoms": symptoms,
                        "timestamp": timestamp + timedelta(hours=np.random.randint(0, 24))
                    })

        self.analyze_all_regions()


# Singleton instance
outbreak_detector = OutbreakDetector()

