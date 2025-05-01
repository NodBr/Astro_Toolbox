import swisseph as swe
import datetime

import swisseph as swe
import datetime

def get_solar_year(tjd):
    """
    Calculates the mean solar year length (in days) for a given Julian Day.

    Based on the formula by Simon et al. (1994) as used in Swiss Ephemeris and Astro.com.

    Args:
        tjd (float): Julian Day.

    Returns:
        float: Length of the mean solar year in days.
    """
    J2000 = 2451545.0  # Julian Day for Jan 1, 2000, 12h UT
    t = (tjd - J2000) / 365250.0
    t2, t3, t4, t5 = t*t, t*t*t, t*t*t*t, t*t*t*t*t

    # Derivative of velocity in arcseconds per millennium
    dvel = (
        1296027711.03429 +
        2 * 109.15809 * t +
        3 * 0.07207 * t2 -
        4 * 0.23530 * t3 -
        5 * 0.00180 * t4 +
        6 * 0.00020 * t5
    )

    dvel /= 3600.0  # Convert arcseconds to degrees

    # Convert degrees to days
    dcycle = 360.0 * 365250.0 / dvel
    return dcycle

def dt_to_jd(date):
    """
    Converts a Python datetime object to Julian Day.

    Args:
        date (datetime): A timezone-aware or naive datetime object.

    Returns:
        float: The corresponding Julian Day.
    """
    year, month, day = date.year, date.month, date.day
    hour = getattr(date, 'hour', 0)
    minute = getattr(date, 'minute', 0)
    second = getattr(date, 'second', 0)
    microsecond = getattr(date, 'microsecond', 0)

    hour_float = hour + minute / 60 + second / 3600 + microsecond / 3_600_000_000
    return swe.julday(year, month, day, hour_float)

def jd_to_dt(jd):
    """
    Converts a Julian Day to a Python datetime object (naive, no timezone).

    Args:
        jd (float): Julian Day.

    Returns:
        datetime: The corresponding datetime object.
    """
    year, month, day, hour = swe.revjul(jd)
    hour_int = int(hour)
    minute_int = int((hour - hour_int) * 60)
    second_int = int((hour - hour_int - minute_int / 60) * 3600)
    return datetime.datetime(year, month, day, hour_int, minute_int, second_int)
