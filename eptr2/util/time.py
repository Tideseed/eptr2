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


def contract_close_time(c, to_timestamp=False, delta=3600):
    """
    Get the close time of a contract with the format PHyyMMDDHH or PByyMMDDHH-BB
    """
    dt = contract_to_datetime(c) - timedelta(seconds=delta)

    if to_timestamp:
        ts = dt.timestamp()
        return ts

    return dt


def time_to_contract_close(c, dt_then: datetime | str = None, ts_then: float = None):
    """
    Get the time to close of a contract with the format PHyyMMDDHH or PByyMMDDHH-BB
    """
    dt_close = contract_close_time(c, to_timestamp=True)
    if ts_then is not None:
        now_ts = ts_then
    elif dt_then is None:
        now_ts = get_utc3_now().timestamp()
    elif isinstance(dt_then, datetime):
        now_ts = dt_then.timestamp()
    elif isinstance(dt_then, str):
        try:
            now_ts = datetime.fromisoformat(dt_then).timestamp()
        except ValueError:
            print("Invalid datetime string format. ISO format expected.")
            return None

    return dt_close - now_ts


def get_time_min_max_price_map():

    map_l = [
        {
            "date": "2025-04-05",
            "min": 0,
            "max": 3400.0,
            "idm_min": 0,
            "idm_max": 3502.0,
        },
        {
            "date": "2024-06-01",
            "min": 0,
            "max": 3000.0,
            "idm_min": 0,
            "idm_max": 3090.0,
        },
        {
            "date": "2023-07-04",
            "min": 0,
            "max": 2700.0,
            "idm_min": 0,
            "idm_max": 2781.0,
        },
        {
            "date": "2023-04-01",
            "min": 0,
            "max": 2600.0,
            "idm_min": 0,
            "idm_max": 2678.0,
        },
        {
            "date": "2023-03-01",
            "min": 0,
            "max": 3050.0,
            "idm_min": 0,
            "idm_max": 3141.5,
        },
        {
            "date": "2023-02-01",
            "min": 0,
            "max": 3650.0,
            "idm_min": 0,
            "idm_max": 3759.5,
        },
        {
            "date": "2023-01-01",
            "min": 0,
            "max": 4200.0,
            "idm_min": 0,
            "idm_max": 4326.0,
        },
        {
            "date": "2022-09-02",
            "min": 0,
            "max": 4800.0,
            "idm_min": 0,
            "idm_max": 4944.0,
        },
    ]

    ## Sort the map by date

    map_l = sorted(map_l, key=lambda x: x["date"], reverse=True)

    return map_l


def contract_to_floor_ceil_prices(c):
    """
    Given a contract return the min and max prices
    """

    the_date = contract_to_datetime(c).date()
    mm_map = get_time_min_max_price_map()
    for x in mm_map:
        if the_date >= datetime.strptime(x["date"], "%Y-%m-%d").date():
            return x

    return None


def get_probable_settlement_date(x: str | None = None, settlement_day=15):
    """
    This function calculates the next probable settlement date based on certain criteria.
    """

    now_dt = get_utc3_now()

    if x is None:
        x = now_dt

    elif isinstance(x, str):
        x: datetime = datetime.strptime(x, "%Y-%m-%d")

    probable_settlement_date = x.replace(
        month=x.month + 1,
        day=settlement_day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    return probable_settlement_date


def check_date_for_settlement(x: str | datetime, settlement_day=15):
    """
    Check if the settlement date for a given date has already occured.
    """

    now_dt = get_utc3_now()
    probable_settlement_date = get_probable_settlement_date(
        x=x, settlement_day=settlement_day
    )

    if now_dt >= probable_settlement_date:
        return True

    return False
