from datetime import datetime, timedelta


def preprocess_date(date_val: datetime | str):
    if isinstance(date_val, datetime):
        return date_val
    elif isinstance(date_val, str):
        return datetime.fromisoformat(date_val)
    else:
        raise Exception("Date value must be either datetime or string")
