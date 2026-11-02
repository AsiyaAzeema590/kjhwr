import json
from pathlib import Path

from app.services.elexon import (
    fetch_actual_wind,
    fetch_wind_forecast,
)

from app.services.analysis import (
    prepare_actuals,
    prepare_forecasts,
    select_day_ahead_forecast,
    combine_actuals_and_forecast,
    calculate_metrics,
)


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "analysis.json"


def main():
    print("Fetching January 2026 actual wind data...")
    actual_rows = fetch_actual_wind()

    print("Fetching January 2026 forecast data...")
    forecast_rows = fetch_wind_forecast()

    print("Preparing analysis...")

    actuals = prepare_actuals(actual_rows)
    forecasts = prepare_forecasts(forecast_rows)

    day_ahead = select_day_ahead_forecast(
        forecasts
    )

    combined = combine_actuals_and_forecast(
        actuals,
        day_ahead,
    )

    metrics = calculate_metrics(combined)

    chart_data = []

    for _, row in combined.iterrows():
        chart_data.append(
            {
                "time": row["startTime"].isoformat(),
                "publishTime": row["publishTime"].isoformat(),
                "forecast": round(
                    float(row["forecast"]),
                    2,
                ),
                "actual": round(
                    float(row["actual"]),
                    2,
                ),
                "error": round(
                    float(row["error"]),
                    2,
                ),
            }
        )

    result = {
        "metrics": metrics,
        "count": len(chart_data),
        "data": chart_data,
    }

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            result,
            file,
            indent=2,
        )

    print()
    print("Analysis saved successfully!")
    print(f"File: {OUTPUT_FILE}")
    print(f"Records: {len(chart_data)}")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()