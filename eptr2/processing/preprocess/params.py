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

    elif key in ["region"]:
        value = "TR1" if value is None else value

    elif key in ["price_type"]:
        value = "SMP" if value is None else value
        if value not in ["MCP", "SMP"]:
            raise Exception("Price type must be either MCP or SMP")

    elif key in ["order_type"]:
        value = "BOTH_REGULATIONS" if value is None else value
        if value not in ["UP_REGULATION", "DOWN_REGULATION", "BOTH_REGULATIONS"]:
            raise Exception(
                "Order type must be either UP_REGULATION, DOWN_REGULATION or BOTH_REGULATIONS"
            )

    return value
