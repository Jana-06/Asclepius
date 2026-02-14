"""
Admin API Endpoints
Fairness monitoring, system management
"""

from fastapi import APIRouter, Depends
from typing import List

from app.schemas import FairnessReportResponse, FairnessMetric
from app.services import fairness_monitor
from app.core.security import require_admin

router = APIRouter()


@router.get("/fairness-report", response_model=FairnessReportResponse)
async def get_fairness_report():
    """Get latest fairness monitoring report"""

    report = fairness_monitor.get_latest_report()

    metrics = []
    for m in report.get("metrics", []):
        # Flatten values for each demographic value
        for value, metric_value in m.get("values", {}).items():
            if isinstance(metric_value, dict):
                # Handle equalized odds with TPR/FPR
                metrics.append(FairnessMetric(
                    demographic=m["demographic"],
                    demographic_value=value,
                    metric_name=f"{m['metric_name']}_tpr",
                    metric_value=metric_value.get("tpr", 0),
                    baseline_value=0.5,
                    disparity_detected=m.get("disparity_detected", False)
                ))
            else:
                metrics.append(FairnessMetric(
                    demographic=m["demographic"],
                    demographic_value=value,
                    metric_name=m["metric_name"],
                    metric_value=metric_value,
                    baseline_value=0.33,  # Expected for 3 risk levels
                    disparity_detected=m.get("disparity_detected", False)
                ))

    return FairnessReportResponse(
        model_version=report.get("model_version", "1.0.0"),
        audit_date=report.get("audit_date"),
        overall_fairness_score=report.get("overall_fairness_score", 1.0),
        metrics=metrics,
        recommendations=report.get("recommendations", [])
    )


@router.get("/fairness-history")
async def get_fairness_history(limit: int = 10):
    """Get fairness audit history"""

    history = fairness_monitor.get_audit_history(limit=limit)

    return {
        "total_audits": len(history),
        "audits": [
            {
                "audit_date": h.get("audit_date"),
                "overall_fairness_score": h.get("overall_fairness_score"),
                "total_predictions": h.get("total_predictions"),
                "recommendations_count": len(h.get("recommendations", []))
            }
            for h in history
        ]
    }


@router.post("/fairness/generate-mock-data")
async def generate_mock_fairness_data(n_predictions: int = 500):
    """Generate mock prediction data for fairness testing"""

    fairness_monitor.generate_mock_data(n_predictions=n_predictions)

    return {
        "message": f"Generated {n_predictions} mock predictions",
        "total_predictions": len(fairness_monitor._predictions)
    }


@router.post("/fairness/run-audit")
async def run_fairness_audit(model_version: str = "1.0.0"):
    """Manually trigger a fairness audit"""

    report = fairness_monitor.run_audit(model_version=model_version)

    return {
        "message": "Fairness audit completed",
        "overall_score": report.get("overall_fairness_score"),
        "total_predictions_analyzed": report.get("total_predictions"),
        "recommendations": report.get("recommendations", [])
    }


@router.get("/system/health")
async def system_health():
    """Get system health status"""

    return {
        "status": "healthy",
        "components": {
            "triage_engine": "operational",
            "load_balancer": "operational",
            "outbreak_detector": "operational",
            "fairness_monitor": "operational",
            "database": "connected"
        },
        "metrics": {
            "predictions_logged": len(fairness_monitor._predictions),
            "active_outbreak_signals": len([
                s for s in fairness_monitor._predictions
            ]) if hasattr(fairness_monitor, '_predictions') else 0
        }
    }


@router.get("/symptoms/reference")
async def get_symptom_reference():
    """Get reference list of all symptoms"""

    from app.ml.synthetic_data import SYMPTOMS

    return [
        {
            "code": code,
            "name": code.replace("_", " ").title(),
            "severity_weight": info["weight"],
            "related_departments": info["departments"]
        }
        for code, info in SYMPTOMS.items()
    ]


@router.get("/departments/reference")
async def get_department_reference():
    """Get reference list of all departments"""

    from app.ml.synthetic_data import DEPARTMENTS

    return [
        {"code": dept.lower().replace(" ", "_").replace("&", "and"), "name": dept}
        for dept in DEPARTMENTS
    ]

