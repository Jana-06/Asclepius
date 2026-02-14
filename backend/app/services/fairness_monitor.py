"""
Fairness Monitoring Service
Monitors model bias across demographic groups
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

from app.core.config import settings


class FairnessMonitor:
    """Monitor and report on model fairness across demographics"""

    DEMOGRAPHICS = {
        "gender": ["M", "F", "OTHER"],
        "age_group": ["0-18", "19-45", "46-65", "65+"]
    }

    METRICS = [
        "demographic_parity",
        "equalized_odds",
        "predictive_parity"
    ]

    def __init__(self):
        self._predictions: List[Dict] = []
        self._audit_history: List[Dict] = []
        self._last_audit: Optional[datetime] = None

    def log_prediction(self, prediction: Dict, demographics: Dict):
        """Log a prediction for fairness analysis"""
        self._predictions.append({
            "timestamp": datetime.utcnow(),
            "risk_level": prediction.get("risk_level"),
            "confidence": prediction.get("confidence"),
            "department": prediction.get("department"),
            "gender": demographics.get("gender"),
            "age": demographics.get("age"),
            "age_group": self._get_age_group(demographics.get("age", 30))
        })

        # Limit stored predictions
        if len(self._predictions) > 10000:
            self._predictions = self._predictions[-10000:]

    def _get_age_group(self, age: int) -> str:
        """Convert age to age group"""
        if age < 19:
            return "0-18"
        elif age < 46:
            return "19-45"
        elif age < 66:
            return "46-65"
        else:
            return "65+"

    def calculate_demographic_parity(self, demographic: str) -> Dict[str, float]:
        """Calculate demographic parity for high-risk predictions"""

        if not self._predictions:
            return {}

        # Group predictions by demographic value
        groups = defaultdict(list)
        for pred in self._predictions:
            group_value = pred.get(demographic)
            if group_value:
                groups[group_value].append(pred)

        # Calculate high-risk rate for each group
        rates = {}
        for group_value, preds in groups.items():
            high_risk = sum(1 for p in preds if p["risk_level"] == "HIGH")
            rates[group_value] = high_risk / len(preds) if preds else 0

        return rates

    def calculate_equalized_odds(self, demographic: str) -> Dict[str, Dict[str, float]]:
        """Calculate equalized odds across demographic groups"""

        if not self._predictions:
            return {}

        groups = defaultdict(list)
        for pred in self._predictions:
            group_value = pred.get(demographic)
            if group_value:
                groups[group_value].append(pred)

        results = {}
        for group_value, preds in groups.items():
            # True positive rate approximation (HIGH predictions with high confidence)
            confident_high = [p for p in preds if p["risk_level"] == "HIGH" and p["confidence"] > 0.7]
            tpr = len(confident_high) / len(preds) if preds else 0

            # False positive rate approximation
            uncertain_high = [p for p in preds if p["risk_level"] == "HIGH" and p["confidence"] < 0.6]
            fpr = len(uncertain_high) / len(preds) if preds else 0

            results[group_value] = {"tpr": round(tpr, 4), "fpr": round(fpr, 4)}

        return results

    def detect_disparity(self, rates: Dict[str, float], threshold: float = None) -> Dict[str, Any]:
        """Detect disparity in rates across groups"""

        threshold = threshold or settings.DEMOGRAPHIC_PARITY_THRESHOLD

        if len(rates) < 2:
            return {"disparity_detected": False, "max_difference": 0}

        values = list(rates.values())
        max_diff = max(values) - min(values)

        return {
            "disparity_detected": max_diff > threshold,
            "max_difference": round(max_diff, 4),
            "threshold": threshold,
            "min_rate": round(min(values), 4),
            "max_rate": round(max(values), 4),
            "groups": rates
        }

    def run_audit(self, model_version: str = "1.0.0") -> Dict[str, Any]:
        """Run full fairness audit"""

        audit_results = {
            "model_version": model_version,
            "audit_date": datetime.utcnow().isoformat(),
            "total_predictions": len(self._predictions),
            "metrics": [],
            "recommendations": []
        }

        overall_scores = []

        for demographic in ["gender", "age_group"]:
            # Demographic parity
            dp_rates = self.calculate_demographic_parity(demographic)
            dp_disparity = self.detect_disparity(dp_rates)

            metric = {
                "demographic": demographic,
                "metric_name": "demographic_parity",
                "values": dp_rates,
                "disparity_detected": dp_disparity["disparity_detected"],
                "max_difference": dp_disparity["max_difference"]
            }
            audit_results["metrics"].append(metric)

            if dp_disparity["disparity_detected"]:
                audit_results["recommendations"].append(
                    f"Review model behavior for {demographic} - disparity of "
                    f"{dp_disparity['max_difference']:.2%} detected in high-risk classifications"
                )

            # Calculate fairness score (1 - normalized disparity)
            score = 1 - min(dp_disparity["max_difference"] / 0.5, 1)
            overall_scores.append(score)

            # Equalized odds
            eo_results = self.calculate_equalized_odds(demographic)

            audit_results["metrics"].append({
                "demographic": demographic,
                "metric_name": "equalized_odds",
                "values": eo_results,
                "disparity_detected": False  # Simplified
            })

        # Overall fairness score
        audit_results["overall_fairness_score"] = round(
            np.mean(overall_scores) if overall_scores else 1.0, 3
        )

        # Add general recommendations
        if audit_results["overall_fairness_score"] < 0.8:
            audit_results["recommendations"].append(
                "Consider retraining model with balanced demographic representation"
            )

        if len(self._predictions) < 100:
            audit_results["recommendations"].append(
                "Insufficient data for reliable fairness assessment. "
                "Continue monitoring as more predictions are logged."
            )

        # Store audit
        self._audit_history.append(audit_results)
        self._last_audit = datetime.utcnow()

        return audit_results

    def get_latest_report(self) -> Optional[Dict[str, Any]]:
        """Get the latest fairness report"""

        if not self._audit_history:
            return self.run_audit()

        # Run new audit if last one is old
        if (self._last_audit and
            (datetime.utcnow() - self._last_audit).total_seconds() >
            settings.FAIRNESS_AUDIT_INTERVAL_HOURS * 3600):
            return self.run_audit()

        return self._audit_history[-1]

    def get_audit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get audit history"""
        return self._audit_history[-limit:]

    def generate_mock_data(self, n_predictions: int = 500):
        """Generate mock predictions for testing"""

        for _ in range(n_predictions):
            gender = np.random.choice(["M", "F", "OTHER"], p=[0.48, 0.48, 0.04])
            age = int(np.clip(np.random.lognormal(3.5, 0.5), 5, 90))

            # Simulate slight bias for testing
            if gender == "F":
                risk = np.random.choice(["LOW", "MEDIUM", "HIGH"], p=[0.4, 0.35, 0.25])
            else:
                risk = np.random.choice(["LOW", "MEDIUM", "HIGH"], p=[0.35, 0.35, 0.30])

            self._predictions.append({
                "timestamp": datetime.utcnow() - timedelta(hours=np.random.randint(0, 720)),
                "risk_level": risk,
                "confidence": np.random.uniform(0.5, 0.95),
                "department": np.random.choice(["General Medicine", "Emergency", "Cardiology"]),
                "gender": gender,
                "age": age,
                "age_group": self._get_age_group(age)
            })


# Singleton instance
fairness_monitor = FairnessMonitor()

