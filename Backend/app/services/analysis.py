import numpy as np
import pandas as pd


DAY_AHEAD_CUTOFF_HOUR_UTC = 17


def prepare_actuals(rows: list) -> pd.DataFrame:
    """
    Convert AGWS wind actuals into hourly total wind generation.

    AGWS provides separate Wind Onshore and Wind Offshore
    records for each settlement period.

    We first sum onshore + offshore for each half-hour,
    then calculate the hourly average.
    """

    df = pd.DataFrame(rows)

    if df.empty:
        return pd.DataFrame(
            columns=["startTime", "actual"]
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"],
        utc=True,
        errors="coerce",
    )

    df["generation"] = pd.to_numeric(
        df["generation"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "startTime",
            "generation",
        ]
    )

    # Combine Wind Onshore + Wind Offshore
    # for each half-hour.
    half_hourly = (
        df.groupby(
            "startTime",
            as_index=False,
        )["generation"]
        .sum()
    )

    # Convert half-hourly values to hourly average MW.
    half_hourly["hour"] = (
        half_hourly["startTime"].dt.floor("h")
    )

    hourly = (
        half_hourly
        .groupby(
            "hour",
            as_index=False,
        )["generation"]
        .mean()
    )

    return hourly.rename(
        columns={
            "hour": "startTime",
            "generation": "actual",
        }
    )


def prepare_forecasts(rows: list) -> pd.DataFrame:
    """
    Convert raw Elexon WINDFOR records
    into a clean forecast DataFrame.
    """

    df = pd.DataFrame(rows)

    if df.empty:
        return pd.DataFrame(
            columns=[
                "startTime",
                "publishTime",
                "forecast",
            ]
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"],
        utc=True,
        errors="coerce",
    )

    df["publishTime"] = pd.to_datetime(
        df["publishTime"],
        utc=True,
        errors="coerce",
    )

    df["generation"] = pd.to_numeric(
        df["generation"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "startTime",
            "publishTime",
            "generation",
        ]
    )

    return df[
        [
            "startTime",
            "publishTime",
            "generation",
        ]
    ].rename(
        columns={
            "generation": "forecast",
        }
    )


def select_day_ahead_forecast(
    forecast_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Select the latest forecast available by the
    day-ahead 18:00 Brussels-time procurement cutoff.

    January is CET (UTC+1), so 18:00 Brussels
    corresponds to 17:00 UTC.

    For delivery date D, eligible forecasts are
    published before or at 17:00 UTC on D-1.

    The latest eligible publishTime is selected
    independently for each delivery hour.
    """

    if forecast_df.empty:
        return forecast_df.copy()

    df = forecast_df.copy()

    # Delivery date of each forecasted hour.
    df["delivery_date"] = df["startTime"].dt.date

    # Day before the delivery date.
    df["decision_date"] = (
        pd.to_datetime(df["delivery_date"])
        - pd.Timedelta(days=1)
    ).dt.date

    # January is CET, so 18:00 Brussels = 17:00 UTC.
    df["cutoff"] = pd.to_datetime(
        df["decision_date"].astype(str)
        + f" {DAY_AHEAD_CUTOFF_HOUR_UTC:02d}:00:00",
        utc=True,
    )

    # Keep forecasts available by the procurement cutoff.
    eligible = df[
        df["publishTime"] <= df["cutoff"]
    ].copy()

    if eligible.empty:
        return pd.DataFrame(
            columns=[
                "startTime",
                "publishTime",
                "forecast",
            ]
        )

    # For each delivery hour, select the latest
    # forecast that was available before the cutoff.
    eligible = (
        eligible
        .sort_values(
            [
                "startTime",
                "publishTime",
            ]
        )
        .drop_duplicates(
            subset=["startTime"],
            keep="last",
        )
    )

    return (
        eligible[
            [
                "startTime",
                "publishTime",
                "forecast",
            ]
        ]
        .sort_values("startTime")
    )


def combine_actuals_and_forecast(
    actuals: pd.DataFrame,
    forecasts: pd.DataFrame,
) -> pd.DataFrame:
    """
    Match hourly forecast values with hourly
    actual wind generation.
    """

    if actuals.empty or forecasts.empty:
        return pd.DataFrame(
            columns=[
                "startTime",
                "publishTime",
                "forecast",
                "actual",
                "error",
            ]
        )

    merged = pd.merge(
        forecasts,
        actuals,
        on="startTime",
        how="inner",
    )

    merged["error"] = (
        merged["forecast"]
        - merged["actual"]
    )

    return merged.sort_values(
        "startTime"
    )


def calculate_metrics(
    df: pd.DataFrame,
) -> dict:
    """
    Calculate forecast accuracy metrics.

    Error convention:

        forecast - actual

    Positive bias = over-forecasting.
    Negative bias = under-forecasting.
    """

    if df.empty:
        return {
            "mae": 0,
            "rmse": 0,
            "mape": 0,
            "bias": 0,
            "records": 0,
        }

    working = df.copy()

    working["error"] = (
        working["forecast"]
        - working["actual"]
    )

    absolute_error = (
        working["error"].abs()
    )

    mae = absolute_error.mean()

    rmse = np.sqrt(
        (working["error"] ** 2).mean()
    )

    non_zero = (
        working["actual"] != 0
    )

    if non_zero.any():
        mape = (
            (
                working.loc[
                    non_zero,
                    "error",
                ].abs()
                /
                working.loc[
                    non_zero,
                    "actual",
                ].abs()
            ).mean()
            * 100
        )
    else:
        mape = 0

    bias = working["error"].mean()

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2),
        "bias": round(float(bias), 2),
        "records": int(len(working)),
    }