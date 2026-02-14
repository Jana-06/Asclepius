"""
Explainability Module using SHAP
Provides feature importance and model explanation
"""

import pickle
import numpy as np
from typing import Dict, List, Any, Optional
import json

# Optional SHAP import
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    shap = None


class TriageExplainer:
    """Generate SHAP explanations for triage predictions"""

    def __init__(self, model_dir: str = "data/models"):
        self.model_dir = model_dir
        self.shap_explainer = None
        self.model = None
        self.feature_names = None
        self._loaded = False

    def load(self, model, feature_names: List[str]) -> bool:
        """Load or create SHAP explainer"""
        try:
            self.model = model
            self.feature_names = feature_names

            if not SHAP_AVAILABLE:
                print("SHAP not available, using fallback explanations")
                self._loaded = True
                return True

            # Try to load pre-computed explainer
            try:
                with open(f"{self.model_dir}/shap_explainer.pkl", 'rb') as f:
                    self.shap_explainer = pickle.load(f)
            except FileNotFoundError:
                # Create new explainer
                self.shap_explainer = shap.TreeExplainer(model)

            self._loaded = True
            return True
        except Exception as e:
            print(f"Error loading explainer: {e}")
            self._loaded = True  # Allow fallback
            return True

    def explain(self, X: np.ndarray, prediction: Dict) -> Dict[str, Any]:
        """Generate SHAP explanation for a prediction"""

        if not self._loaded or not SHAP_AVAILABLE or self.shap_explainer is None:
            return self._fallback_explanation(X, prediction)

        try:
            # Get SHAP values
            shap_values = self.shap_explainer.shap_values(X)

            # For multi-class, get values for predicted class
            risk_level = prediction.get("risk_level", "MEDIUM")
            class_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
            class_idx = class_map.get(risk_level, 1)

            if isinstance(shap_values, list):
                values = shap_values[class_idx][0]
            else:
                values = shap_values[0]

            # Create feature contributions
            contributions = []
            for i, (name, value, shap_val) in enumerate(
                zip(self.feature_names, X[0], values)
            ):
                if abs(shap_val) > 0.01:  # Filter insignificant
                    contributions.append({
                        "feature": name,
                        "value": float(value) if isinstance(value, (int, float, np.number)) else str(value),
                        "contribution": float(shap_val),
                        "direction": "positive" if shap_val > 0 else "negative"
                    })

            # Sort by absolute contribution
            contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)

            # Build explanation
            return {
                "top_features": contributions[:10],
                "shap_values": {
                    self.feature_names[i]: float(v)
                    for i, v in enumerate(values)
                    if abs(v) > 0.001
                },
                "model_confidence": prediction.get("confidence", 0.0),
                "rule_triggered": prediction.get("rule_triggered"),
                "base_value": float(self.shap_explainer.expected_value[class_idx])
                    if hasattr(self.shap_explainer.expected_value, '__iter__')
                    else float(self.shap_explainer.expected_value)
            }
        except Exception as e:
            print(f"SHAP explanation error: {e}")
            return self._fallback_explanation(X, prediction)

    def _fallback_explanation(self, X: np.ndarray, prediction: Dict) -> Dict[str, Any]:
        """Provide fallback explanation when SHAP fails"""

        # Use feature importance from model if available
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            contributions = []

            for i, (name, importance) in enumerate(
                zip(self.feature_names or [f"feature_{i}" for i in range(len(importances))],
                    importances)
            ):
                if importance > 0.01:
                    contributions.append({
                        "feature": name,
                        "value": float(X[0][i]) if i < len(X[0]) else 0,
                        "contribution": float(importance),
                        "direction": "positive"
                    })

            contributions.sort(key=lambda x: x["contribution"], reverse=True)

            return {
                "top_features": contributions[:10],
                "shap_values": {},
                "model_confidence": prediction.get("confidence", 0.0),
                "rule_triggered": prediction.get("rule_triggered"),
                "note": "Using feature importance (SHAP unavailable)"
            }

        return {
            "top_features": [],
            "shap_values": {},
            "model_confidence": prediction.get("confidence", 0.0),
            "rule_triggered": prediction.get("rule_triggered"),
            "note": "Explanation unavailable"
        }

    def explain_batch(self, X: np.ndarray, predictions: List[Dict]) -> List[Dict]:
        """Generate explanations for multiple predictions"""
        return [self.explain(X[i:i+1], pred) for i, pred in enumerate(predictions)]


# Singleton instance
explainer = TriageExplainer()

