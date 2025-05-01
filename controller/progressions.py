import pytz
from datetime import datetime, timedelta

import pytz
from datetime import datetime, timedelta

def calculate_progressed_datetime(birth_date, birth_hour, birth_minute,
                                   target_date, target_hour, target_minute,
                                   timezone_name):
    """
    Calculates the progressed datetime in UTC using the day-for-a-year principle.

    This function determines how many days have passed in the native's life 
    (from birth to a target date), and adds that same number of days to 
    the birth datetime to get the progressed datetime.

    Args:
        birth_date (date): Date of birth.
        birth_hour (int): Hour of birth (local time).
        birth_minute (int): Minute of birth (local time).
        target_date (date): Target date for the progression (local time).
        target_hour (int): Hour on the target date (local time).
        target_minute (int): Minute on the target date (local time).
        timezone_name (str): Timezone name (e.g., 'America/Sao_Paulo').

    Returns:
        datetime: Timezone-aware datetime in UTC representing the progressed chart's time.
    """
    tz = pytz.timezone(timezone_name)

    birth_local = tz.localize(datetime.combine(
        birth_date, datetime.min.time()
    ) + timedelta(hours=birth_hour, minutes=birth_minute))

    target_local = tz.localize(datetime.combine(
        target_date, datetime.min.time()
    ) + timedelta(hours=target_hour, minutes=target_minute))

    # Compute number of days lived (day-for-a-year method)
    delta_days = (target_local - birth_local).total_seconds() / 86400

    # Add that number of days to birth time to get progressed datetime
    progressed_local = birth_local + timedelta(days=delta_days)

    return progressed_local.astimezone(pytz.utc)
