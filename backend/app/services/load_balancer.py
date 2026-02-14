"""
Hospital Load Balancer Service
Manages real-time hospital capacity and suggests alternatives
"""

import math
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

from app.core.config import settings


class HospitalLoadBalancer:
    """AI-driven hospital load balancing engine"""

    def __init__(self):
        # In-memory cache for demo (use Redis in production)
        self._hospital_loads: Dict[str, Dict] = {}
        self._last_update: Dict[str, datetime] = {}

    def calculate_distance(self, lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat/2)**2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def get_hospital_load(self, hospital_id: str) -> Dict[str, Any]:
        """Get current load for a hospital"""

        # Simulate real-time load data
        if hospital_id not in self._hospital_loads:
            self._hospital_loads[hospital_id] = self._simulate_hospital_load()

        return self._hospital_loads[hospital_id]

    def _simulate_hospital_load(self) -> Dict[str, Any]:
        """Simulate hospital department load for demo"""

        departments = [
            {"name": "Emergency", "capacity": 20},
            {"name": "General Medicine", "capacity": 50},
            {"name": "Cardiology", "capacity": 15},
            {"name": "Pulmonology", "capacity": 15},
            {"name": "Neurology", "capacity": 10},
            {"name": "Gastroenterology", "capacity": 15},
            {"name": "Orthopedics", "capacity": 20},
            {"name": "Surgery", "capacity": 25}
        ]

        dept_loads = []
        total_patients = 0
        total_capacity = 0

        for dept in departments:
            # Random load between 30% and 95%
            load_pct = random.uniform(0.3, 0.95)
            current = int(dept["capacity"] * load_pct)

            status = "normal"
            if load_pct > settings.CRITICAL_LOAD_THRESHOLD:
                status = "critical"
            elif load_pct > settings.HIGH_LOAD_THRESHOLD:
                status = "busy"

            dept_loads.append({
                "department": dept["name"],
                "current_patients": current,
                "max_capacity": dept["capacity"],
                "load_percentage": round(load_pct * 100, 1),
                "avg_wait_minutes": int(20 * load_pct + random.randint(5, 15)),
                "status": status
            })

            total_patients += current
            total_capacity += dept["capacity"]

        return {
            "departments": dept_loads,
            "overall_load": round((total_patients / total_capacity) * 100, 1),
            "total_patients": total_patients,
            "total_capacity": total_capacity,
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_department_load(self, hospital_id: str, department: str) -> Dict[str, Any]:
        """Get load for specific department"""

        hospital_load = self.get_hospital_load(hospital_id)

        for dept in hospital_load["departments"]:
            if dept["department"] == department:
                return dept

        # Default if department not found
        return {
            "department": department,
            "current_patients": 0,
            "max_capacity": 20,
            "load_percentage": 0,
            "avg_wait_minutes": 15,
            "status": "normal"
        }

    def suggest_alternate_hospitals(
        self,
        patient_lat: float,
        patient_lng: float,
        required_department: str,
        hospitals: List[Dict],
        max_distance_km: float = 50.0,
        max_results: int = 5,
        exclude_hospital_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Suggest alternate hospitals based on load and distance"""

        candidates = []

        for hospital in hospitals:
            if hospital.get("id") == exclude_hospital_id:
                continue

            # Check if department is available
            if required_department not in hospital.get("departments", []):
                continue

            # Calculate distance
            h_lat = hospital.get("latitude", 0)
            h_lng = hospital.get("longitude", 0)

            if h_lat and h_lng:
                distance = self.calculate_distance(patient_lat, patient_lng, h_lat, h_lng)
            else:
                distance = random.uniform(5, max_distance_km)

            if distance > max_distance_km:
                continue

            # Get hospital load
            load_data = self.get_hospital_load(str(hospital["id"]))
            dept_load = self.get_department_load(str(hospital["id"]), required_department)

            # Calculate score (lower is better)
            # Weight: 40% distance, 40% load, 20% wait time
            distance_score = distance / max_distance_km
            load_score = dept_load["load_percentage"] / 100
            wait_score = min(dept_load["avg_wait_minutes"] / 60, 1.0)

            total_score = 0.4 * distance_score + 0.4 * load_score + 0.2 * wait_score

            candidates.append({
                "hospital_id": hospital["id"],
                "name": hospital["name"],
                "hospital_type": hospital.get("hospital_type", "General"),
                "distance_km": round(distance, 1),
                "current_load": dept_load["load_percentage"],
                "estimated_wait_minutes": dept_load["avg_wait_minutes"],
                "status": dept_load["status"],
                "departments_available": hospital.get("departments", []),
                "address": hospital.get("address", ""),
                "contact_phone": hospital.get("contact_phone", ""),
                "score": total_score
            })

        # Sort by score and return top results
        candidates.sort(key=lambda x: x["score"])

        return candidates[:max_results]

    def should_suggest_alternate(self, hospital_id: str, department: str) -> bool:
        """Check if alternate hospital should be suggested"""

        dept_load = self.get_department_load(hospital_id, department)
        load_pct = dept_load["load_percentage"] / 100

        return load_pct > settings.HIGH_LOAD_THRESHOLD

    def update_load(self, hospital_id: str, department: str,
                    patient_count: int, capacity: int):
        """Update department load (for real-time simulation)"""

        if hospital_id not in self._hospital_loads:
            self._hospital_loads[hospital_id] = self._simulate_hospital_load()

        for dept in self._hospital_loads[hospital_id]["departments"]:
            if dept["department"] == department:
                dept["current_patients"] = patient_count
                dept["max_capacity"] = capacity
                dept["load_percentage"] = round((patient_count / capacity) * 100, 1)

                if dept["load_percentage"] > 95:
                    dept["status"] = "critical"
                elif dept["load_percentage"] > 80:
                    dept["status"] = "busy"
                else:
                    dept["status"] = "normal"
                break

        self._last_update[hospital_id] = datetime.utcnow()


# Singleton instance
load_balancer = HospitalLoadBalancer()

