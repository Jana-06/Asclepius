"""
Outbreak Detection API Endpoints
"""

from fastapi import APIRouter, Query
from typing import List, Optional

from app.schemas import OutbreakTrendResponse, OutbreakSummary
from app.services import outbreak_detector

router = APIRouter()


@router.get("/trends", response_model=List[OutbreakTrendResponse])
async def get_outbreak_trends(
    region: Optional[str] = None,
    active_only: bool = True,
    limit: int = Query(default=20, le=100)
):
    """Get current outbreak trends and signals"""

    signals = outbreak_detector.get_active_signals()

    if region:
        signals = [s for s in signals if s["region"] == region]

    if active_only:
        signals = [s for s in signals if s["is_active"]]

    # Sort by signal strength
    signals.sort(key=lambda x: x["signal_strength"], reverse=True)

    return [
        OutbreakTrendResponse(
            id=s["id"],
            region=s["region"],
            symptom_cluster=s["symptom_cluster"],
            predicted_condition=s.get("predicted_condition"),
            signal_strength=s["signal_strength"],
            case_count=s["case_count"],
            trend=s["trend"],
            detected_at=s["detected_at"],
            is_active=s["is_active"]
        )
        for s in signals[:limit]
    ]


@router.get("/summary", response_model=OutbreakSummary)
async def get_outbreak_summary():
    """Get outbreak monitoring summary"""

    summary = outbreak_detector.get_summary()

    return OutbreakSummary(
        active_signals=summary["active_signals"],
        high_priority_regions=summary["high_priority_regions"],
        top_symptoms=summary["top_symptoms"],
        trend_data=summary["trend_data"]
    )


@router.post("/simulate")
async def simulate_outbreak_data(
    regions: List[str] = ["Delhi_North", "Mumbai", "Chennai"],
    days: int = 30
):
    """Generate simulated outbreak data for testing"""

    outbreak_detector.simulate_outbreak_data(regions=regions, days=days)

    return {
        "message": f"Simulated {days} days of outbreak data for {len(regions)} regions",
        "regions": regions
    }


@router.get("/regions")
async def get_monitored_regions():
    """Get list of regions being monitored"""

    signals = outbreak_detector.get_active_signals()
    regions = list(set(s["region"] for s in signals))

    region_stats = []
    for region in regions:
        region_signals = [s for s in signals if s["region"] == region]
        region_stats.append({
            "region": region,
            "active_signals": len([s for s in region_signals if s["is_active"]]),
            "total_cases": sum(s["case_count"] for s in region_signals),
            "max_signal_strength": max((s["signal_strength"] for s in region_signals), default=0)
        })

    region_stats.sort(key=lambda x: x["max_signal_strength"], reverse=True)

    return region_stats

