import json
from pathlib import Path

from fastapi import APIRouter

from app.services.elexon import (
    fetch_actual_wind,
    fetch_wind_forecast,
)


router = APIRouter()


# Saved analysis file
DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "analysis.json"
)


@router.get("/status")
def status():
    return {
        "application": "UK Wind Forecast Dashboard",
        "status": "running",
    }


@router.get("/data/actual")
def actual_wind():
    data = fetch_actual_wind()

    return {
        "count": len(data),
        "data": data[:10],
    }


@router.get("/data/forecast")
def wind_forecast():
    data = fetch_wind_forecast()

    return {
        "count": len(data),
        "data": data[:10],
    }


@router.get("/analysis")
def analysis():

    if not DATA_FILE.exists():
        return {
            "error": (
                "Analysis data has not been generated yet. "
                "Run 'python save_analysis.py' first."
            )
        }

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)