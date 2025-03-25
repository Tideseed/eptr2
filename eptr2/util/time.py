from datetime import datetime, timedelta, timezone
import pytz


def check_iso_format(
    val: str | datetime,
    strict_hour_format: bool = False,
    convert_to_hour_format: bool = False,
):
    """
    Check if a string is datetime in ISO format and convert if necessary.
    Hour formatted dt is like 2023-01-01T10:00:00+03:00 (no minute, second, microsecond, tz is UTC+3)
    """
    try:
        dt = datetime.fromisoformat(val) if isinstance(val, str) else val
        if convert_to_hour_format:
            dt = dt.replace(tzinfo=timezone(timedelta(seconds=10800)))
            dt = dt.replace(microsecond=0)
            dt = dt.replace(second=0)
            dt = dt.replace(minute=0)

            return dt
        elif strict_hour_format:
            if (
                dt.minute != 0
                or dt.second != 0
                or dt.microsecond != 0
                or dt.tzinfo == timezone(timedelta(seconds=10800))
            ):
                return None
        return dt
    except ValueError:
        return None
    except AttributeError:
        return None


def get_utc3_now():
    """
    Gets Turkey time (UTC +3)
    """
    return datetime.now(tz=pytz.timezone("Europe/Istanbul"))


def get_today_utc3():
    """
    Gets Turkey today (UTC +3)
    """
    return get_utc3_now().strftime("%Y-%m-%d")


def get_date_from_key(key):
    if key == "today":
        res = get_today_utc3()
    elif key == "start_of_month":
        res = get_utc3_now().strftime("%Y-%m-01")

    return res


def parse_dt_transparency_1(dt):
    ## Example 2023-07-01T00:00:00.000+0300
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")


def datetime_to_contract(
    dt, is_ts=False, root_only=False, block_hours: int | None = None
):
    if dt is None:
        return None

    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    if is_ts:
        dt = datetime.utcfromtimestamp(dt) + timedelta(hours=3)
    c_raw = dt.strftime("%y%m%d%H")
    if root_only:
        return c_raw
    elif block_hours is None:
        return "PH" + c_raw
    else:
        if block_hours > 24 or block_hours < 1:
            raise ValueError("block_hours must be between 1 and 24")

        return "PB" + c_raw + "-" + str(100 + block_hours)[1:]


def iso_to_contract(dt):
    return datetime_to_contract(check_iso_format(dt, convert_to_hour_format=True))


def contract_to_datetime(
    contract, timestamp: bool = False, localize: bool = True, to_str: bool = False
):
    dt_obj = datetime.strptime(
        contract[2:10] + ":00:00" + ("+03:00" if localize else ""), "%y%m%d%H:%M:%S%z"
    )

    if to_str:
        return dt_obj.isoformat(timespec="seconds")

    if timestamp:
        dt_obj = dt_obj.timestamp()
    return dt_obj


def get_hourly_date_range(start_date, end_date, return_str=False):
    l = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = (
        datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(hours=1)
    )
    t = 0
    while True:
        l.append(start_date + timedelta(hours=t))
        if l[-1] >= end_date:
            break
        t += 1

    if return_str:
        l = [str(x) for x in l]

    return l


def get_hourly_contract_range_list(start_date, end_date):
    l = [
        datetime_to_contract(x)
        for x in get_hourly_date_range(start_date, end_date, return_str=False)
    ]

    return l


def contract_to_hour(c):
    """
    Get the hour from a contract with the format PHyyMMDDHH or PByyMMDDHH-BB
    """
    return c[8:10]


def contract_to_day(c):
    """
    Get the day from a contract with the format PHyyMMDDHH or PByyMMDDHH-BB
    """
    return c[6:8]


def contract_to_wday(c):
    """
    Get the weekday from a contract with the format PHyyMMDDHH or PByyMMDDHH-BB
    """
    return contract_to_datetime(c).strftime("%w")


def contract_to_date_info(c, include_c=False):
    c_ts = contract_to_datetime(c, timestamp=True)
    d = {
        "wday": ts_to_day_of_week_utc3(c_ts),
        "hour": ts_to_hour_utc3(c_ts),
        "day": ts_to_day_utc3(c_ts),
    }

    if include_c:
        d["c"] = c

    return d


def ts_to_day_of_week_utc3(ts):
    """
    0: Sunday
    """
    return ts_to_format_utc3(ts=ts, format="%w")


def ts_to_format_utc3(ts, format="%Y-%m-%d"):
    return (datetime.fromtimestamp(ts, tz=pytz.timezone("Europe/Istanbul"))).strftime(
        format
    )


def ts_to_date_utc3(ts):
    """
    Convert timestamp to UTC3 - date
    """
    return ts_to_format_utc3(ts, format="%Y-%m-%d")


def ts_to_day_utc3(ts):
    """
    Convert timestamp to UTC3 and get the day
    """
    return ts_to_format_utc3(ts, format="%d")


def ts_to_hour_utc3(ts):
    """
    Convert timestamp to UTC3 and get the hour
    """
    return ts_to_format_utc3(ts, format="%H")


def calculate_active_contracts():

    now_dt = get_utc3_now()
    sod = now_dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)
    eod = now_dt.replace(hour=23, minute=0, second=0, microsecond=0)
    if now_dt.hour >= 18:
        eod += timedelta(days=1)

    l = [
        datetime_to_contract(sod + timedelta(hours=i))
        for i in range(int((eod - sod).total_seconds() // 3600) + 1)
    ]

    return l
