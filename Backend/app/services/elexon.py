import requests
import pandas as pd


BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"


def fetch_actual_wind(
    start_date: str = "2026-01-01T00:00:00Z",
    end_date: str = "2026-02-01T00:00:00Z",
):
    url = f"{BASE_URL}/datasets/AGWS/stream"

    params = {
        "publishDateTimeFrom": start_date,
        "publishDateTimeTo": end_date,
    }

    response = requests.get(
        url,
        params=params,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        data = data.get("data", [])

    wind_rows = []

    for row in data:
        psr_type = str(
            row.get("psrType", "")
        ).lower()

        if "wind" in psr_type:
            wind_rows.append(
                {
                    "dataset": "AGWS",
                    "publishTime": row.get(
                        "publishTime"
                    ),
                    "startTime": row.get(
                        "startTime"
                    ),
                    "settlementDate": row.get(
                        "settlementDate"
                    ),
                    "settlementPeriod": row.get(
                        "settlementPeriod"
                    ),
                    "fuelType": "WIND",
                    "generation": row.get(
                        "quantity"
                    ),
                }
            )

    return wind_rows


def fetch_wind_forecast(
    start_date: str = "2026-01-01T00:00:00Z",
    end_date: str = "2026-02-01T00:00:00Z",
):
    """
    Fetch wind forecast evolution for every
    delivery hour in the requested period.

    Elexon's evolution endpoint returns the
    forecast history for a delivery hour.
    """

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    all_rows = []

    current = start

    total_hours = int(
        (end - start).total_seconds() // 3600
    )

    completed = 0

    while current < end:

        url = (
            f"{BASE_URL}/forecast/"
            "generation/wind/evolution"
        )

        params = {
            "startTime": current.isoformat()
        }

        response = requests.get(
            url,
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        data = result.get("data", [])

        all_rows.extend(data)

        completed += 1

        print(
            f"Fetching forecast "
            f"{completed}/{total_hours} "
            f"({current.strftime('%Y-%m-%d %H:%M UTC')})"
        )

        current = current + pd.Timedelta(
            hours=1
        )

    return all_rows