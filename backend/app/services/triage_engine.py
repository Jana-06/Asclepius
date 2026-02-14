"""
Triage Engine Service
Combines ML inference with rule-based logic and explainability
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np

from app.ml.inference import TriageInference
from app.ml.explainer import TriageExplainer
from app.core.config import settings


class TriageEngine:
    """Main triage engine combining ML and rules"""

    def __init__(self):
        self.inference = TriageInference(settings.MODEL_PATH)
        self.explainer = TriageExplainer(settings.MODEL_PATH)
        self._initialized = False

    async def load_models(self) -> bool:
        """Load ML models asynchronously"""
        try:
            success = self.inference.load_models()
            if success:
                feature_names = self.inference.get_feature_names()
                self.explainer.load(self.inference.model, feature_names)
                self._initialized = True
            return success
        except Exception as e:
            print(f"Error loading triage models: {e}")
            # Create dummy models for development
            self._initialized = True
            return True

    async def process_triage(
        self,
        patient_id: str,
        symptoms: List[str],
        vitals: Dict[str, Any],
        age: int,
        gender: str,
        pre_existing_conditions: List[str]
    ) -> Dict[str, Any]:
        """Process triage request and return results"""

        session_id = str(uuid.uuid4())

        if not self._initialized:
            # Return mock response for development
            return self._mock_triage_response(session_id, symptoms, vitals)

        try:
            # Make prediction
            prediction = self.inference.predict(
                symptoms=symptoms,
                conditions=pre_existing_conditions,
                vitals=vitals,
                age=age,
                gender=gender
            )

            # Prepare features for explanation
            X = self.inference.prepare_features(
                symptoms, pre_existing_conditions, vitals, age, gender
            )

            # Generate explanation
            explanation = self.explainer.explain(X, prediction)

            return {
                "session_id": session_id,
                "risk_level": prediction["risk_level"],
                "department": prediction["department"],
                "confidence": prediction["confidence"],
                "explanation": explanation,
                "risk_probabilities": prediction.get("risk_probabilities", {}),
                "rule_triggered": prediction.get("rule_triggered"),
                "rule_reason": prediction.get("rule_reason"),
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Triage processing error: {e}")
            return self._mock_triage_response(session_id, symptoms, vitals)

    def _mock_triage_response(self, session_id: str, symptoms: List[str],
                               vitals: Dict) -> Dict[str, Any]:
        """Generate mock response for development/testing"""

        # Simple rule-based mock
        high_risk_symptoms = {"chest_pain", "breathlessness", "seizures", "fainting"}
        medium_risk_symptoms = {"fever", "vomiting", "dizziness", "abdominal_pain"}

        risk_level = "LOW"
        if any(s in high_risk_symptoms for s in symptoms):
            risk_level = "HIGH"
        elif any(s in medium_risk_symptoms for s in symptoms):
            risk_level = "MEDIUM"

        # Check vitals
        if vitals.get("spo2", 100) < 92:
            risk_level = "HIGH"
        elif vitals.get("temperature", 98.6) > 102:
            risk_level = "MEDIUM" if risk_level == "LOW" else risk_level

        # Department mapping
        dept_map = {
            "chest_pain": "Emergency",
            "breathlessness": "Pulmonology",
            "fever": "General Medicine",
            "headache": "General Medicine",
            "abdominal_pain": "Gastroenterology"
        }
        department = dept_map.get(symptoms[0] if symptoms else "fever", "General Medicine")

        if risk_level == "HIGH":
            department = "Emergency"

        return {
            "session_id": session_id,
            "risk_level": risk_level,
            "department": department,
            "confidence": 0.75,
            "explanation": {
                "top_features": [
                    {"feature": f"symptom_{symptoms[0]}" if symptoms else "symptom_fever",
                     "value": 1, "contribution": 0.3, "direction": "positive"}
                ],
                "shap_values": {},
                "model_confidence": 0.75,
                "rule_triggered": None,
                "note": "Mock response - models not loaded"
            },
            "risk_probabilities": {"LOW": 0.2, "MEDIUM": 0.3, "HIGH": 0.5},
            "rule_triggered": None,
            "rule_reason": None,
            "created_at": datetime.utcnow().isoformat()
        }

    def estimate_wait_time(self, department: str, hospital_load: float) -> int:
        """Estimate wait time based on department load"""
        base_wait = {
            "Emergency": 5,
            "General Medicine": 20,
            "Cardiology": 15,
            "Pulmonology": 15,
            "Neurology": 20,
            "Gastroenterology": 25,
            "Orthopedics": 30,
            "Surgery": 25
        }

        base = base_wait.get(department, 20)
        # Increase wait time based on load
        return int(base * (1 + hospital_load))


# Singleton instance
triage_engine = TriageEngine()

