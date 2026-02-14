"""
ML Inference Module for SwasthyaFlow AI
Handles model loading and predictions
"""

import pickle
import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import os


class TriageInference:
    """Handle ML model inference for triage classification"""

    def __init__(self, model_dir: str = "data/models"):
        self.model_dir = model_dir
        self.model = None
        self.dept_model = None
        self.symptom_encoder = None
        self.condition_encoder = None
        self.label_encoder = None
        self.dept_encoder = None
        self.scaler = None
        self.rules = None
        self._loaded = False

    def load_models(self) -> bool:
        """Load all model artifacts"""
        try:
            with open(f"{self.model_dir}/triage_model.pkl", 'rb') as f:
                self.model = pickle.load(f)

            with open(f"{self.model_dir}/symptom_encoder.pkl", 'rb') as f:
                self.symptom_encoder = pickle.load(f)

            with open(f"{self.model_dir}/condition_encoder.pkl", 'rb') as f:
                self.condition_encoder = pickle.load(f)

            with open(f"{self.model_dir}/label_encoder.pkl", 'rb') as f:
                self.label_encoder = pickle.load(f)

            with open(f"{self.model_dir}/scaler.pkl", 'rb') as f:
                self.scaler = pickle.load(f)

            with open(f"{self.model_dir}/department_model.pkl", 'rb') as f:
                self.dept_model = pickle.load(f)

            with open(f"{self.model_dir}/department_encoder.pkl", 'rb') as f:
                self.dept_encoder = pickle.load(f)

            with open(f"{self.model_dir}/rule_engine.json", 'r') as f:
                self.rules = json.load(f)

            self._loaded = True
            return True
        except FileNotFoundError as e:
            print(f"Model file not found: {e}")
            return False
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

    def check_rules(self, symptoms: List[str], vitals: Dict,
                    age: int) -> Optional[Dict]:
        """Check clinical rules for overrides"""

        if not self.rules:
            return None

        for rule_name, rule in self.rules.items():
            rule_symptoms = rule.get("symptoms", [])
            min_match = rule.get("min_match", len(rule_symptoms))

            # Check symptom match
            matching_symptoms = [s for s in rule_symptoms if s in symptoms]
            if len(matching_symptoms) < min_match:
                continue

            # Check age conditions
            age_cond = rule.get("age", {})
            if "gt" in age_cond and age <= age_cond["gt"]:
                continue
            if "lt" in age_cond and age >= age_cond["lt"]:
                continue

            # Check vital conditions
            vital_conds = rule.get("vitals", {})
            vitals_match = True
            for vital_name, conditions in vital_conds.items():
                vital_value = vitals.get(vital_name)
                if vital_value is None:
                    vitals_match = False
                    break
                if "lt" in conditions and vital_value >= conditions["lt"]:
                    vitals_match = False
                    break
                if "gt" in conditions and vital_value <= conditions["gt"]:
                    vitals_match = False
                    break

            if not vitals_match:
                continue

            # Rule matched
            return {
                "rule_name": rule_name,
                "action": rule["action"],
                "department": rule["department"],
                "reason": rule["reason"]
            }

        return None

    def prepare_features(self, symptoms: List[str], conditions: List[str],
                        vitals: Dict, age: int, gender: str) -> np.ndarray:
        """Prepare feature vector for prediction"""

        # Encode symptoms
        symptom_features = self.symptom_encoder.transform([symptoms])

        # Encode conditions
        condition_features = self.condition_encoder.transform([conditions])

        # Numeric features
        numeric = np.array([[
            age,
            vitals.get('bp_systolic', 120),
            vitals.get('bp_diastolic', 80),
            vitals.get('heart_rate', 72),
            vitals.get('temperature', 98.6),
            vitals.get('spo2', 98),
            vitals.get('respiratory_rate', 16)
        ]])
        numeric_scaled = self.scaler.transform(numeric)

        # Gender encoding
        gender_features = np.zeros((1, 3))
        gender_map = {'F': 0, 'M': 1, 'OTHER': 2}
        gender_features[0, gender_map.get(gender, 1)] = 1

        # Combine features
        X = np.hstack([symptom_features, condition_features,
                       numeric_scaled, gender_features])

        return X

    def predict(self, symptoms: List[str], conditions: List[str],
                vitals: Dict, age: int, gender: str) -> Dict[str, Any]:
        """Make triage prediction with rule override check"""

        if not self._loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")

        # Check clinical rules first
        rule_result = self.check_rules(symptoms, vitals, age)

        # Prepare features
        X = self.prepare_features(symptoms, conditions, vitals, age, gender)

        # ML prediction
        risk_proba = self.model.predict_proba(X)[0]
        risk_pred = self.model.predict(X)[0]
        risk_label = self.label_encoder.inverse_transform([risk_pred])[0]

        # Department prediction
        dept_proba = self.dept_model.predict_proba(X)[0]
        dept_pred = self.dept_model.predict(X)[0]
        dept_label = self.dept_encoder.inverse_transform([dept_pred])[0]

        # Get confidence
        confidence = float(max(risk_proba))

        # Apply rule override if present
        final_risk = risk_label
        final_dept = dept_label
        rule_triggered = None

        if rule_result:
            final_risk = rule_result["action"]
            final_dept = rule_result["department"]
            rule_triggered = rule_result["rule_name"]
            confidence = 0.95  # High confidence for rule-based decisions

        return {
            "risk_level": final_risk,
            "department": final_dept,
            "confidence": confidence,
            "risk_probabilities": {
                self.label_encoder.inverse_transform([i])[0]: float(p)
                for i, p in enumerate(risk_proba)
            },
            "department_probabilities": {
                self.dept_encoder.inverse_transform([i])[0]: float(p)
                for i, p in enumerate(dept_proba)
            },
            "rule_triggered": rule_triggered,
            "rule_reason": rule_result["reason"] if rule_result else None
        }

    def get_feature_names(self) -> List[str]:
        """Get feature names for explainability"""
        symptom_names = [f"symptom_{s}" for s in self.symptom_encoder.classes_]
        condition_names = [f"condition_{c}" for c in self.condition_encoder.classes_]
        numeric_names = ['age', 'bp_systolic', 'bp_diastolic', 'heart_rate',
                        'temperature', 'spo2', 'respiratory_rate']
        gender_names = ['gender_F', 'gender_M', 'gender_OTHER']

        return symptom_names + condition_names + numeric_names + gender_names


# Singleton instance
inference_engine = TriageInference()

