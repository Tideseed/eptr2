from datetime import datetime, timedelta


def format_date_epias_hour(date: str | datetime):
    """
    Desired format "2023-01-01T00:00:00+03:00"
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    date = date.strftime("%Y-%m-%dT00:00:00+03:00")

    return date


def preprocess_parameter(key, value):
    if key in ["start_date", "end_date", "date_time", "period"]:
        value = format_date_epias_hour(value)

    return value
