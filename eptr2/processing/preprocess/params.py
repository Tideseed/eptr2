from datetime import datetime, timedelta


def format_date_epias_hour(date: str | datetime, transform: str | None = None):
    """
    Desired format "2023-01-01T00:00:00+03:00"
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    date = date.strftime("%Y-%m-%dT00:00:00+03:00")

    return date


def preprocess_parameter(key, value):
    if key in [
        "start_date",
        "end_date",
        "date",
        "period",
        "se_date",
        "period_start_date",
        "period_end_date",
        "version_start_date",
        "version_end_date",
    ]:
        value = format_date_epias_hour(value)

    elif key in ["region"]:
        value = "TR1" if value is None else value

    elif key in ["region_id"]:
        value = "1" if value is None else value

    elif key in ["price_type"]:
        value = "SMP" if value is None else value
        if value not in ["MCP", "SMP"]:
            raise Exception("Price type must be either MCP or SMP")

    elif key in ["point_type"]:
        if value not in ["INPUT", "OUTPUT"]:
            raise Exception("Point type must be either INPUT or OUTPUT")

    elif key in ["intl_direction"]:
        # value = "TRGR" if value is None else value
        val_list = ["TRGR", "GRTR", "TRBG", "BGTR"]
        if value not in val_list:
            raise Exception(
                "International direction (intl_direction) type should be one of "
                + ", ".join(val_list)
                + "."
            )

    elif key in ["order_type"]:
        value = "BOTH_REGULATIONS" if value is None else value
        if value not in ["UP_REGULATION", "DOWN_REGULATION", "BOTH_REGULATIONS"]:
            raise Exception(
                "Order type must be either UP_REGULATION, DOWN_REGULATION or BOTH_REGULATIONS"
            )

    elif key in ["load_type"]:
        value = "Baz" if value is None else value
        if value not in ["Baz", "Puant", "Puant Dışı"]:
            raise Exception("Load type must be either Baz, Puant or Puant Dışı")

    return value
