from datetime import datetime, timedelta, timezone
import pytz
from typing import Literal, Union


def contract_duration(
    contract: str, return_type: Literal["hours", "minutes", "seconds"] = "seconds"
) -> float:
    """
    Calculate the duration of a contract from its opening to closing time.

    The contract opens at 18:00 (6 PM) the day before and closes at the contract hour.

    Args:
        contract: Contract string in format 'PHyyMMDDHH'
        return_type: Unit for the returned duration. Options: 'seconds', 'minutes', 'hours'

    Returns:
        Duration as a float in the specified unit

    Raises:
        ValueError: If return_type is not one of the valid options

    Example:
        >>> contract_duration("PH24072914", "hours")
        20.0  # 18:00 day before to 14:00 = 20 hours
    """
    close_dt = contract_close_time(contract)
    open_dt = close_dt.replace(hour=18) - timedelta(days=1)
    duration = close_dt - open_dt
    seconds = duration.total_seconds()
    if return_type == "seconds":
        return seconds
    elif return_type == "minutes":
        return seconds / 60
    elif return_type == "hours":
        return seconds / 3600
    else:
        raise ValueError(
            f"Invalid return type {return_type}. Use one of ['seconds', 'minutes', 'hours']"
        )


def check_iso_format(
    val: str | datetime,
    strict_hour_format: bool = False,
    convert_to_hour_format: bool = False,
):
    """
    Validate and optionally convert a datetime string to ISO format with hour precision.

    Hour-formatted datetime has the pattern: YYYY-MM-DDTHH:00:00+03:00
    (minutes, seconds, and microseconds are zero, timezone is UTC+3)

    Args:
        val: A datetime string in ISO format or a datetime object
        strict_hour_format: If True, validate that datetime has zero minutes/seconds/microseconds
                          and UTC+3 timezone. Returns None if validation fails.
        convert_to_hour_format: If True, convert the datetime to hour format
                               (zero out minutes/seconds/microseconds, set timezone to UTC+3)

    Returns:
        datetime object if valid, or None if validation fails

    Example:
        >>> check_iso_format("2024-07-29T14:30:00+03:00", convert_to_hour_format=True)
        datetime(2024, 7, 29, 14, 0, 0, tzinfo=timezone(timedelta(seconds=10800)))
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
    Get the current datetime in Turkey timezone (UTC+3).

    Returns:
        datetime: Current time in Europe/Istanbul timezone

    Example:
        >>> now = get_utc3_now()
        >>> print(now.tzinfo)
        Europe/Istanbul
    """
    return datetime.now(tz=pytz.timezone("Europe/Istanbul"))


def get_today_utc3():
    """
    Get today's date in Turkey timezone (UTC+3) as a string.

    Returns:
        str: Current date in 'YYYY-MM-DD' format

    Example:
        >>> get_today_utc3()
        '2024-07-29'
    """
    return get_utc3_now().strftime("%Y-%m-%d")


def transform_date(
    date_val: Union[str, datetime, None] = None,
    key: Literal[
        "today",
        "start_of_month",
        "end_of_month",
        "next_day",
        "previous_day",
        "start_of_year",
        "end_of_year",
    ] = "today",
    to_str: bool = True,
):
    """
    Transform a date according to the specified key operation.

    Args:
        date_val: Date to transform (string in 'YYYY-MM-DD' format, datetime object, or None for today)
        key: Transformation operation to perform:
            - 'today': Return the date as-is
            - 'next_day': Add one day
            - 'previous_day': Subtract one day
            - 'start_of_month': First day of the month
            - 'end_of_month': Last day of the month
            - 'start_of_year': January 1st of the year
            - 'end_of_year': December 31st of the year
        to_str: If True, return as 'YYYY-MM-DD' string; if False, return datetime object

    Returns:
        str or datetime: Transformed date in the requested format

    Raises:
        ValueError: If key is not one of the valid options

    Example:
        >>> transform_date("2024-07-15", key="start_of_month")
        '2024-07-01'
        >>> transform_date("2024-07-15", key="end_of_year")
        '2024-12-31'
    """

    if date_val is None:
        date_val = get_utc3_now()
    elif isinstance(date_val, str):
        date_val = datetime.strptime(date_val, "%Y-%m-%d")

    if key == "today":
        res = date_val
    elif key == "next_day":
        res = date_val + timedelta(days=1)
    elif key == "previous_day":
        res = date_val - timedelta(days=1)
    elif key == "start_of_month":
        res = date_val.replace(day=1)
    elif key == "end_of_month":
        res = (date_val.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(
            days=1
        )
    elif key == "start_of_year":
        res = date_val.replace(month=1, day=1)
    elif key == "end_of_year":
        res = date_val.replace(month=12, day=31)
    else:
        raise ValueError(f"Invalid key: {key}")

    if to_str:
        return res.strftime("%Y-%m-%d")
    return res


def parse_dt_transparency_1(dt):
    """
    Parse a datetime string in EPIAS Transparency Platform format.

    Args:
        dt: Datetime string in format 'YYYY-MM-DDTHH:MM:SS.fff+ZZZZ'

    Returns:
        datetime: Parsed datetime object with timezone information

    Example:
        >>> parse_dt_transparency_1("2023-07-01T00:00:00.000+0300")
        datetime(2023, 7, 1, 0, 0, 0, tzinfo=timezone(timedelta(seconds=10800)))
    """
    ## Example 2023-07-01T00:00:00.000+0300
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")


def datetime_to_contract(
    dt, is_ts=False, root_only=False, block_hours: int | None = None
):
    """
    Convert a datetime to a Turkish electricity market contract string.

    Args:
        dt: Datetime object, string in ISO format, or Unix timestamp (if is_ts=True)
        is_ts: If True, treat dt as Unix timestamp and convert from UTC to UTC+3
        root_only: If True, return only the raw contract format 'yyMMDDHH' without prefix
        block_hours: If provided (1-24), create a block contract 'PByyMMDDHH-BB'
                    If None, create hourly contract 'PHyyMMDDHH'

    Returns:
        str: Contract string in one of these formats:
            - 'PHyyMMDDHH' (hourly contract, default)
            - 'PByyMMDDHH-BB' (block contract, BB = block_hours formatted as 2 digits)
            - 'yyMMDDHH' (raw format if root_only=True)

    Raises:
        ValueError: If block_hours is not between 1 and 24

    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2024, 7, 29, 14, 0, 0)
        >>> datetime_to_contract(dt)
        'PH24072914'
        >>> datetime_to_contract(dt, block_hours=3)
        'PB24072914-03'
    """
    if dt is None:
        return None

    if isinstance(dt, str):
        dt = check_iso_format(val=dt)
        if dt is None:
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
    """
    Convert an ISO format datetime string to a contract string.

    Convenience function that combines check_iso_format and datetime_to_contract.
    Automatically converts to hour format (zeros out minutes/seconds).

    Args:
        dt: Datetime string in ISO format

    Returns:
        str: Contract string in 'PHyyMMDDHH' format

    Example:
        >>> iso_to_contract("2024-07-29T14:30:00+03:00")
        'PH24072914'
    """
    return datetime_to_contract(check_iso_format(dt, convert_to_hour_format=True))


def contract_to_datetime(
    contract, timestamp: bool = False, localize: bool = True, to_str: bool = False
):
    """
    Convert a contract string to a datetime object or timestamp.

    Args:
        contract: Contract string in format 'PHyyMMDDHH'
        timestamp: If True, return Unix timestamp instead of datetime object
        localize: If True, include UTC+3 timezone info in the datetime
        to_str: If True, return ISO format string instead of datetime object

    Returns:
        datetime, float, or str: Depending on timestamp and to_str flags:
            - datetime object with timezone (default)
            - Unix timestamp (if timestamp=True)
            - ISO format string (if to_str=True)

    Example:
        >>> contract_to_datetime("PH24072914")
        datetime(2024, 7, 29, 14, 0, 0, tzinfo=timezone(timedelta(seconds=10800)))
        >>> contract_to_datetime("PH24072914", timestamp=True)
        1722250800.0
        >>> contract_to_datetime("PH24072914", to_str=True)
        '2024-07-29T14:00:00+03:00'
    """
    dt_obj = datetime.strptime(
        contract[2:10] + ":00:00" + ("+03:00" if localize else ""), "%y%m%d%H:%M:%S%z"
    )

    if to_str:
        return dt_obj.isoformat(timespec="seconds")

    if timestamp:
        dt_obj = dt_obj.timestamp()
    return dt_obj


def get_hourly_date_range(start_date, end_date, return_str=False):
    """
    Generate a list of hourly datetime objects between start and end dates (inclusive).

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (inclusive)
        return_str: If True, return list of strings; if False, return datetime objects

    Returns:
        list: Hourly datetime objects or strings from start_date 00:00 to end_date 23:00

    Example:
        >>> dates = get_hourly_date_range("2024-07-29", "2024-07-29")
        >>> len(dates)
        24
        >>> dates = get_hourly_date_range("2024-07-29", "2024-07-30")
        >>> len(dates)
        48
    """
    l = []  # noqa: E741
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
        l = [str(x) for x in l]  # noqa: E741

    return l


def get_hourly_contract_range_list(start_date, end_date):
    """
    Generate a list of hourly contract strings between start and end dates (inclusive).

    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (inclusive)

    Returns:
        list: Contract strings in 'PHyyMMDDHH' format for each hour in the range

    Example:
        >>> contracts = get_hourly_contract_range_list("2024-07-29", "2024-07-29")
        >>> len(contracts)
        24
        >>> contracts[0]
        'PH24072900'
        >>> contracts[-1]
        'PH24072923'
    """
    l = [  # noqa: E741
        datetime_to_contract(x)
        for x in get_hourly_date_range(start_date, end_date, return_str=False)
    ]

    return l


def contract_to_hour(c):
    """
    Extract the hour component from a contract string.

    Args:
        c: Contract string in format 'PHyyMMDDHH'

    Returns:
        str: Hour as a two-digit string ('00' to '23')

    Example:
        >>> contract_to_hour("PH24072914")
        '14'
        >>> contract_to_hour("PB24072914-03")
        '14'
    """
    return c[8:10]


def contract_to_day(c):
    """
    Extract the day component from a contract string.

    Args:
        c: Contract string in format 'PHyyMMDDHH'

    Returns:
        str: Day as a two-digit string ('01' to '31')

    Example:
        >>> contract_to_day("PH24072914")
        '29'
        >>> contract_to_day("PB24072914-03")
        '29'
    """
    return c[6:8]


def change_wday_name_to_tr(wday_name):
    """
    Convert English weekday abbreviation to Turkish abbreviation.

    Args:
        wday_name: English weekday abbreviation ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    Returns:
        str: Turkish weekday abbreviation or original string if not found
            - Mon → Pzt (Pazartesi)
            - Tue → Sal (Salı)
            - Wed → Çar (Çarşamba)
            - Thu → Per (Perşembe)
            - Fri → Cum (Cuma)
            - Sat → Cmt (Cumartesi)
            - Sun → Paz (Pazar)

    Example:
        >>> change_wday_name_to_tr("Mon")
        'Pzt'
        >>> change_wday_name_to_tr("Fri")
        'Cum'
    """
    days_tr = {
        "Mon": "Pzt",
        "Tue": "Sal",
        "Wed": "Çar",
        "Thu": "Per",
        "Fri": "Cum",
        "Sat": "Cmt",
        "Sun": "Paz",
    }
    return days_tr.get(wday_name, wday_name)


def contract_to_wday(c, named=False, tr_name=False):
    """
    Extract the weekday from a contract string.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        named: If True, return weekday name abbreviation (e.g., 'Mon', 'Tue')
        tr_name: If True, return Turkish weekday name abbreviation (e.g., 'Pzt', 'Sal')

    Returns:
        str: Weekday as:
            - Number string '0'-'6' (0=Sunday) if named=False and tr_name=False
            - English abbreviation if named=True
            - Turkish abbreviation if tr_name=True

    Example:
        >>> contract_to_wday("PH24072914")  # Monday
        '1'
        >>> contract_to_wday("PH24072914", named=True)
        'Mon'
        >>> contract_to_wday("PH24072914", tr_name=True)
        'Pzt'
    """
    x = contract_to_datetime(c).strftime("%a" if named or tr_name else "%w")
    if tr_name:
        x = change_wday_name_to_tr(x)

    return x


def contract_to_date_info(c, include_c=False):
    """
    Extract comprehensive date information from a contract string.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        include_c: If True, include the contract string in the returned dictionary

    Returns:
        dict: Dictionary containing:
            - 'wday': Weekday number as string ('0'-'6', 0=Sunday)
            - 'hour': Hour as string ('00'-'23')
            - 'day': Day of month as string ('01'-'31')
            - 'c': Contract string (only if include_c=True)

    Example:
        >>> contract_to_date_info("PH24072914")
        {'wday': '1', 'hour': '14', 'day': '29'}
        >>> contract_to_date_info("PH24072914", include_c=True)
        {'wday': '1', 'hour': '14', 'day': '29', 'c': 'PH24072914'}
    """
    c_ts = contract_to_datetime(c, timestamp=True)
    d = {
        "wday": ts_to_day_of_week_utc3(c_ts),
        "hour": ts_to_hour_utc3(c_ts),
        "day": ts_to_day_utc3(c_ts),
    }

    if include_c:
        d["c"] = c

    return d


def contract_to_day_ahead_time(
    c: str, da_hour: int = 11, da_minutes: int = 0, as_ts=True
):
    """
    Calculate the day-ahead market decision/gate closure time for a contract.

    The day-ahead market typically closes at 11:00 (or specified time) on the day
    before the delivery day.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        da_hour: Hour of day-ahead market closure (default: 11 for 11:00 AM)
        da_minutes: Minutes of day-ahead market closure (default: 0)
        as_ts: If True, return Unix timestamp; if False, return datetime object

    Returns:
        float or datetime: Day-ahead decision time as timestamp or datetime

    Example:
        >>> # For contract on 2024-07-29, gate closes on 2024-07-28 at 11:00
        >>> contract_to_day_ahead_time("PH24072914")
        1722157200.0
        >>> contract_to_day_ahead_time("PH24072914", as_ts=False)
        datetime(2024, 7, 28, 11, 0, 0, tzinfo=timezone(timedelta(seconds=10800)))
    """
    c_dt = contract_to_datetime(c, timestamp=False)
    da_dt = c_dt.replace(
        hour=da_hour, minute=da_minutes, second=0, microsecond=0
    ) - timedelta(days=1)

    if as_ts:
        da_ts = da_dt.timestamp()
        return da_ts

    return da_dt


def ts_to_day_of_week_utc3(ts, named=False, tr_name=False):
    """
    Convert a Unix timestamp to weekday in UTC+3 timezone.

    Args:
        ts: Unix timestamp (seconds since epoch)
        named: If True, return weekday name abbreviation (e.g., 'Mon', 'Tue')
        tr_name: If True, return Turkish weekday name abbreviation (e.g., 'Pzt', 'Sal')

    Returns:
        str: Weekday as:
            - Number string '0'-'6' (0=Sunday) if named=False and tr_name=False
            - English abbreviation if named=True
            - Turkish abbreviation if tr_name=True

    Example:
        >>> ts_to_day_of_week_utc3(1722250800)  # 2024-07-29 14:00
        '1'  # Monday
        >>> ts_to_day_of_week_utc3(1722250800, named=True)
        'Mon'
        >>> ts_to_day_of_week_utc3(1722250800, tr_name=True)
        'Pzt'
    """
    x = ts_to_format_utc3(ts=ts, format="%a" if named or tr_name else "%w")
    if tr_name:
        x = change_wday_name_to_tr(x)
    return x


def ts_to_format_utc3(ts, format="%Y-%m-%d"):
    """
    Convert a Unix timestamp to a formatted string in UTC+3 timezone.

    Args:
        ts: Unix timestamp (seconds since epoch)
        format: strftime format string (default: '%Y-%m-%d')

    Returns:
        str: Formatted datetime string in Europe/Istanbul timezone

    Example:
        >>> ts_to_format_utc3(1722250800)
        '2024-07-29'
        >>> ts_to_format_utc3(1722250800, format='%Y-%m-%d %H:%M:%S')
        '2024-07-29 14:00:00'
    """
    return (datetime.fromtimestamp(ts, tz=pytz.timezone("Europe/Istanbul"))).strftime(
        format
    )


def ts_to_date_utc3(ts):
    """
    Convert a Unix timestamp to a date string in UTC+3 timezone.

    Args:
        ts: Unix timestamp (seconds since epoch)

    Returns:
        str: Date string in 'YYYY-MM-DD' format

    Example:
        >>> ts_to_date_utc3(1722250800)
        '2024-07-29'
    """
    return ts_to_format_utc3(ts, format="%Y-%m-%d")


def ts_to_day_utc3(ts):
    """
    Extract the day of month from a Unix timestamp in UTC+3 timezone.

    Args:
        ts: Unix timestamp (seconds since epoch)

    Returns:
        str: Day of month as two-digit string ('01'-'31')

    Example:
        >>> ts_to_day_utc3(1722250800)
        '29'
    """
    return ts_to_format_utc3(ts, format="%d")


def ts_to_hour_utc3(ts):
    """
    Extract the hour from a Unix timestamp in UTC+3 timezone.

    Args:
        ts: Unix timestamp (seconds since epoch)

    Returns:
        str: Hour as two-digit string ('00'-'23')

    Example:
        >>> ts_to_hour_utc3(1722250800)
        '14'
    """
    return ts_to_format_utc3(ts, format="%H")


def calculate_active_contracts():
    """
    Calculate currently active electricity market contracts.

    Active contracts are those from 2 hours ahead of the current time until the end
    of the trading day. If current time is after 18:00, includes next day's contracts.

    Returns:
        list: List of contract strings in 'PHyyMMDDHH' format, sorted chronologically

    Example:
        >>> # If called at 2024-07-29 10:00
        >>> contracts = calculate_active_contracts()
        >>> contracts[0]
        'PH24072912'  # First contract is at 12:00 (10:00 + 2 hours)
        >>> contracts[-1]
        'PH24072923'  # Last contract is at 23:00 same day

        >>> # If called at 2024-07-29 20:00 (after 18:00)
        >>> contracts = calculate_active_contracts()
        >>> contracts[-1]
        'PH24073023'  # Last contract extends to next day
    """
    now_dt = get_utc3_now()
    sod = now_dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)
    eod = now_dt.replace(hour=23, minute=0, second=0, microsecond=0)
    if now_dt.hour >= 18:
        eod += timedelta(days=1)

    l = [  # noqa: E741
        datetime_to_contract(sod + timedelta(hours=i))
        for i in range(int((eod - sod).total_seconds() // 3600) + 1)
    ]

    return l


def contract_close_time(c, to_timestamp=False, delta=3600):
    """
    Calculate the gate closure time for a contract (when trading stops).

    By default, the gate closes 1 hour (3600 seconds) before the delivery hour.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        to_timestamp: If True, return Unix timestamp; if False, return datetime object
        delta: Seconds before delivery hour when gate closes (default: 3600 = 1 hour)

    Returns:
        datetime or float: Gate closure time as datetime or Unix timestamp

    Example:
        >>> # For delivery at 14:00, gate closes at 13:00
        >>> contract_close_time("PH24072914")
        datetime(2024, 7, 29, 13, 0, 0, tzinfo=timezone(timedelta(seconds=10800)))
        >>> contract_close_time("PH24072914", to_timestamp=True)
        1722247200.0
    """
    dt = contract_to_datetime(c) - timedelta(seconds=delta)

    if to_timestamp:
        ts = dt.timestamp()
        return ts

    return dt


def time_to_contract_close(c, dt_then: datetime | str = None, ts_then: float = None):
    """
    Calculate the remaining time (in seconds) until a contract's gate closes.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        dt_then: Reference datetime (datetime object or ISO string). If None, uses current time.
        ts_then: Reference timestamp. Takes precedence over dt_then if both provided.

    Returns:
        float or None: Seconds until gate closure (positive if gate is still open,
                      negative if gate has closed). Returns None if dt_then is invalid.

    Example:
        >>> # If current time is 2024-07-29 10:00 and gate closes at 13:00
        >>> time_to_contract_close("PH24072914")
        10800.0  # 3 hours = 10800 seconds remaining

        >>> # Using a specific reference time
        >>> from datetime import datetime
        >>> ref_time = datetime(2024, 7, 29, 12, 30, 0)
        >>> time_to_contract_close("PH24072914", dt_then=ref_time)
        1800.0  # 30 minutes = 1800 seconds remaining
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
    """
    Get historical price floor and ceiling limits for Turkish electricity markets.

    Returns a list of price limit periods, sorted by date (most recent first).
    Each period specifies minimum and maximum prices for day-ahead market (DAM)
    and intraday market (IDM).

    Returns:
        list: List of dictionaries, each containing:
            - 'date': Start date of the price limit period (YYYY-MM-DD)
            - 'min': Minimum DAM price (TL/MWh)
            - 'max': Maximum DAM price (TL/MWh)
            - 'idm_min': Minimum IDM price (TL/MWh)
            - 'idm_max': Maximum IDM price (TL/MWh)

    Note:
        - List is sorted by date in descending order (most recent first)
        - Used to validate and cap price values in market operations
        - IDM limits are typically ~3% higher than DAM limits

    Example:
        >>> price_map = get_time_min_max_price_map()
        >>> price_map[0]  # Most recent limits
        {'date': '2025-04-05', 'min': 0, 'max': 3400.0, 'idm_min': 0, 'idm_max': 3502.0}
    """
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


def contract_to_floor_ceil_prices(c: str | None = None):
    """
    Get the price floor and ceiling limits applicable to a specific contract.

    Finds the appropriate price limits based on the contract's delivery date by
    matching against historical price limit periods.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
           If None, returns the most recent (current) price limits.

    Returns:
        dict or None: Dictionary containing:
            - 'date': Start date of the applicable price limit period
            - 'min': Minimum DAM price (TL/MWh)
            - 'max': Maximum DAM price (TL/MWh)
            - 'idm_min': Minimum IDM price (TL/MWh)
            - 'idm_max': Maximum IDM price (TL/MWh)
        Returns None if no matching period found (shouldn't happen for valid contracts).

    Example:
        >>> contract_to_floor_ceil_prices("PH24072914")
        {'date': '2024-06-01', 'min': 0, 'max': 3000.0, 'idm_min': 0, 'idm_max': 3090.0}

        >>> contract_to_floor_ceil_prices()  # No contract = current limits
        {'date': '2025-04-05', 'min': 0, 'max': 3400.0, 'idm_min': 0, 'idm_max': 3502.0}
    """

    ### Min max price map is always sorted by date descending
    mm_map = get_time_min_max_price_map()

    ### If contract is not given return the latest
    if c is None:
        return mm_map[0]

    the_date = contract_to_datetime(c).date()

    for x in mm_map:
        if the_date >= datetime.strptime(x["date"], "%Y-%m-%d").date():
            return x

    return None


def get_probable_settlement_date(x: str | None = None, settlement_day=15):
    """
    Calculate the next probable settlement date for electricity market transactions.

    Settlement typically occurs on a fixed day (default: 15th) of the month following
    the delivery month. This function calculates when settlement is expected to occur.

    Args:
        x: Reference date as string ('YYYY-MM-DD') or datetime object.
           If None, uses current date.
        settlement_day: Day of month when settlement occurs (default: 15)

    Returns:
        datetime: The probable settlement datetime (at 00:00:00) for transactions
                 in the given month

    Example:
        >>> # For July 2024 delivery, settlement is on August 15, 2024
        >>> get_probable_settlement_date("2024-07-29")
        datetime(2024, 8, 15, 0, 0, 0)

        >>> # For December 2024 delivery, settlement is on January 15, 2025
        >>> get_probable_settlement_date("2024-12-15")
        datetime(2025, 1, 15, 0, 0, 0)
    """

    now_dt = get_utc3_now()

    if x is None:
        x = now_dt

    elif isinstance(x, str):
        x: datetime = datetime.strptime(x, "%Y-%m-%d")

    if x.month == 12:
        # If the month is December, we set the next month to January of the next year
        x = x.replace(day=settlement_day, year=x.year + 1, month=1)
    else:
        # Otherwise, we just increment the month by 1
        x = x.replace(day=settlement_day, month=x.month + 1)

    probable_settlement_date = x.replace(
        # day=settlement_day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    return probable_settlement_date


def check_date_for_settlement(x: str | datetime, settlement_day=15):
    """
    Check if the settlement date for a given delivery date has already occurred.

    Determines whether the financial settlement for transactions in a given month
    has been completed (i.e., whether we're past the settlement date).

    Args:
        x: Delivery date as string ('YYYY-MM-DD') or datetime object
        settlement_day: Day of month when settlement occurs (default: 15)

    Returns:
        bool: True if current time is on or after the settlement date,
              False if settlement hasn't occurred yet

    Example:
        >>> # If today is 2024-08-20 and checking July 2024 delivery
        >>> check_date_for_settlement("2024-07-15")
        True  # Settlement was on August 15, which has passed

        >>> # If today is 2024-08-10 and checking July 2024 delivery
        >>> check_date_for_settlement("2024-07-15")
        False  # Settlement is on August 15, which hasn't occurred yet
    """

    now_dt = get_utc3_now()
    probable_settlement_date = get_probable_settlement_date(
        x=x, settlement_day=settlement_day
    )

    if now_dt.timestamp() >= probable_settlement_date.timestamp():
        return True

    return False


def date_str_to_datetime(date_str: str, fmt: str = "%Y-%m-%d"):
    """
    Convert a date string to a timezone-aware datetime object in UTC+3.

    Args:
        date_str: Date string to parse
        fmt: strftime format string (default: '%Y-%m-%d')

    Returns:
        datetime or None: Localized datetime object at 00:00:00 in Europe/Istanbul timezone,
                         or None if parsing fails

    Example:
        >>> dt = date_str_to_datetime("2024-07-29")
        >>> print(dt)
        2024-07-29 00:00:00+03:00
        >>> print(dt.tzinfo)
        Europe/Istanbul
    """
    try:
        return pytz.timezone("Europe/Istanbul").localize(
            datetime.strptime(date_str, fmt)
        )
    except ValueError:
        print(f"Invalid date format: {date_str}. Expected format: {fmt}.")
        return None


def offset_date_by_n_days(date_str: str, fmt: str = "%Y-%m-%d", n: int = 1):
    """
    Offset a date by a specified number of days (forward or backward).

    Args:
        date_str: Date string to offset
        fmt: strftime format string (default: '%Y-%m-%d')
        n: Number of days to offset (positive = forward, negative = backward)

    Returns:
        str or None: Offset date in the same format as input, or None if parsing fails

    Example:
        >>> offset_date_by_n_days("2024-07-29", n=1)
        '2024-07-30'
        >>> offset_date_by_n_days("2024-07-29", n=-1)
        '2024-07-28'
        >>> offset_date_by_n_days("2024-07-29", n=7)
        '2024-08-05'
    """
    dt = date_str_to_datetime(date_str, fmt)
    if dt:
        offset_day = dt + timedelta(days=n)
        return offset_day.strftime(fmt)
    return None


def get_previous_day(date_str: str | None = None, fmt: str = "%Y-%m-%d"):
    """
    Get the previous day from a given date string.

    Convenience function commonly used for intraday market (IDM) queries,
    where you often need to query the previous day's data.

    Args:
        date_str: Date string to get previous day from. If None, uses current date.
        fmt: strftime format string (default: '%Y-%m-%d')

    Returns:
        str or None: Previous day in the same format, or None if parsing fails

    Example:
        >>> get_previous_day("2024-07-29")
        '2024-07-28'
        >>> get_previous_day()  # If today is 2024-07-29
        '2024-07-28'
    """

    if date_str is None:
        date_str = get_today_utc3()

    return offset_date_by_n_days(str(date_str), fmt, n=-1)


def get_start_end_dates_period(period: str):
    """
    Get the first and last dates of the month for a given date.

    Useful for querying full month data when you have any date in that month.

    Args:
        period: Date string in 'YYYY-MM-DD' format (any day of the target month)

    Returns:
        tuple: (start_date, end_date) where:
            - start_date: First day of the month ('YYYY-MM-01')
            - end_date: Last day of the month ('YYYY-MM-DD')

    Example:
        >>> get_start_end_dates_period("2024-07-15")
        ('2024-07-01', '2024-07-31')
        >>> get_start_end_dates_period("2024-02-15")  # Leap year
        ('2024-02-01', '2024-02-29')
    """

    dt = pytz.timezone("Europe/Istanbul").localize(
        datetime.strptime(period, "%Y-%m-%d")
    )

    start_date = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    return start_date, end_date


def contract_remaining_time_formatted(
    contract: str,
    day_label="D",
    hour_label="H",
    minute_label="m",
    second_label="s",
    no_time_label="-",
) -> str:
    """
    Format the remaining time until a contract's gate closes as a human-readable string.

    Based on: https://stackoverflow.com/a/68321739/3608936

    Args:
        contract: Contract string in format 'PHyyMMDDHH'
        day_label: Label for days (default: 'D')
        hour_label: Label for hours (default: 'H')
        minute_label: Label for minutes (default: 'm')
        second_label: Label for seconds (default: 's')
        no_time_label: Label when gate is closed or time is invalid (default: '-')

    Returns:
        str: Formatted time string showing largest relevant units, or no_time_label if closed

    Example:
        >>> # If 2 days, 5 hours, 30 minutes, 15 seconds remaining
        >>> contract_remaining_time_formatted("PH24073114")
        '02D 05H 30m 15s'

        >>> # If only 30 minutes, 15 seconds remaining
        >>> contract_remaining_time_formatted("PH24072914")
        '30m 15s'

        >>> # If gate is closed
        >>> contract_remaining_time_formatted("PH24072814")
        '-'
    """
    seconds = time_to_contract_close(contract)
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return "{:02d}{} {:02d}{} {:02d}{} {:02d}{}".format(
                d, day_label, h, hour_label, m, minute_label, s, second_label
            )
        elif h > 0:
            return "{:02d}{} {:02d}{} {:02d}{}".format(
                h, hour_label, m, minute_label, s, second_label
            )
        elif m > 0:
            return "{:02d}{} {:02d}{}".format(m, minute_label, s, second_label)
        elif s > 0:
            return "{:02d}{}".format(s, second_label)
    return no_time_label


def get_previous_contracts(c: str, n: int = 1, include_current: bool = False):
    """
    Get a list of contracts before a given contract.

    Args:
        c: Reference contract string in format 'PHyyMMDDHH'
        n: Number of previous contracts to retrieve (must be non-negative)
        include_current: If True, include the reference contract at the end of the list

    Returns:
        list: Sorted list of contract strings (oldest to newest)

    Raises:
        ValueError: If n is negative

    Example:
        >>> get_previous_contracts("PH24072914", n=3)
        ['PH24072911', 'PH24072912', 'PH24072913']

        >>> get_previous_contracts("PH24072914", n=3, include_current=True)
        ['PH24072911', 'PH24072912', 'PH24072913', 'PH24072914']
    """

    if n > 0:
        c_dt = contract_to_datetime(c)
        l = [datetime_to_contract(c_dt - timedelta(hours=x + 1)) for x in range(n)]  # noqa: E741
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    if include_current:
        l = l + [c]  # noqa: E741

    l.sort()
    return l


def get_next_contracts(c: str, n: int = 1, include_current: bool = False):
    """
    Get a list of contracts after a given contract.

    Args:
        c: Reference contract string in format 'PHyyMMDDHH'
        n: Number of next contracts to retrieve (must be non-negative)
        include_current: If True, include the reference contract at the start of the list

    Returns:
        list: Sorted list of contract strings (earliest to latest)

    Raises:
        ValueError: If n is negative

    Example:
        >>> get_next_contracts("PH24072914", n=3)
        ['PH24072915', 'PH24072916', 'PH24072917']

        >>> get_next_contracts("PH24072914", n=3, include_current=True)
        ['PH24072914', 'PH24072915', 'PH24072916', 'PH24072917']
    """

    if n > 0:
        c_dt = contract_to_datetime(c)
        l = [datetime_to_contract(c_dt + timedelta(hours=x + 1)) for x in range(n)]  # noqa: E741
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    if include_current:
        l = [c] + l  # noqa: E741

    l.sort()

    return l


def get_contract_range_from_center(c: str, n_before: int = 1, n_after: int = 1):
    """
    Get a range of contracts centered around a given contract.

    The reference contract is always included in the middle of the returned list.

    Args:
        c: Center contract string in format 'PHyyMMDDHH'
        n_before: Number of contracts before the center (default: 1)
        n_after: Number of contracts after the center (default: 1)

    Returns:
        list: Sorted list of contract strings with the reference contract in the middle

    Example:
        >>> get_contract_range_from_center("PH24072914", n_before=2, n_after=2)
        ['PH24072912', 'PH24072913', 'PH24072914', 'PH24072915', 'PH24072916']

        >>> get_contract_range_from_center("PH24072914", n_before=1, n_after=1)
        ['PH24072913', 'PH24072914', 'PH24072915']
    """

    l_before = get_previous_contracts(c=c, n=n_before, include_current=False)
    l_after = get_next_contracts(c=c, n=n_after, include_current=False)

    l = l_before + [c] + l_after  # noqa: E741
    l.sort()

    return l


def date_str_to_contract(date_str: str, hour: int | str = 0) -> str:
    """
    Convert a date string and hour to a contract string.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format
        hour: Hour (0-23) as integer or string (default: 0)

    Returns:
        str: Contract string in 'PHyyMMDDHH' format

    Raises:
        ValueError: If hour is not between 0 and 23

    Example:
        >>> date_str_to_contract("2024-07-29", hour=14)
        'PH24072914'
        >>> date_str_to_contract("2024-07-29", hour="09")
        'PH24072909'
        >>> date_str_to_contract("2024-07-29")  # Default hour=0
        'PH24072900'
    """

    if isinstance(hour, str):
        hour = int(hour)
    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23.")

    hour = f"{hour:02d}"  # Ensure hour is two digits

    dt = datetime.strptime(date_str, "%Y-%m-%d").strftime(f"PH%y%m%d{hour}")
    return dt


def contract_open_time(c, to_timestamp=False, start_hour=18):
    """
    Calculate the gate opening time for a contract (when trading starts).

    The gate typically opens at the start of the delivery hour.

    Args:
        c: Contract string in format 'PHyyMMDDHH'
        to_timestamp: If True, return Unix timestamp; if False, return datetime object
        start_hour: Hour when the gate opens (default: 18 for 18:00 previous day)
    Returns:
        datetime or float: Gate opening time as datetime or Unix timestamp
    """
    dt = contract_to_datetime(c)
    dt = dt.replace(minute=0, second=0, microsecond=0, hour=start_hour) - timedelta(
        days=1
    )

    if to_timestamp:
        return dt.timestamp()
    return dt
