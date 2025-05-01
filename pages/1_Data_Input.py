"""
Data Input Page for Astrological Toolbox
This page collects user's personal and birth information to initialize the astrological chart.
"""

import streamlit as st
import datetime as dt
from services.geolocation import get_location_data
from controller.time_utils import dt_to_jd
import pytz

from config.init_session import init_session_state

init_session_state()

st.subheader("Enter your name")
first_name_col , last_name_col = st.columns(2)

# Collect first and last name
st.session_state.first_name = first_name_col.text_input(
    label="First Name",
    value=st.session_state.first_name,
    placeholder="Enter your first name"
)

st.session_state.last_name = last_name_col.text_input(
    label="Last Name",
    value=st.session_state.last_name,
    placeholder="Enter your last name"
)

st.subheader("Enter your birth data")

date_col, hour_col, minute_col = st.columns([2, 1, 1])

# Collect birth date
st.session_state.birth_date = date_col.date_input(
    label="Birth Date",
    value=st.session_state.birth_date,
    min_value=dt.date(1, 1, 1),
    max_value=dt.date(2999, 12, 31),
    format="DD/MM/YYYY"
)

# Collect birth time
st.session_state.birth_hour = hour_col.number_input(
    label="Hour (Local Time)",
    min_value=0,
    max_value=23,
    value=st.session_state.birth_hour,
    step=1
)

st.session_state.birth_minute = minute_col.number_input(
    label="Minute",
    min_value=0,
    max_value=59,
    value=st.session_state.birth_minute,
    step=1
)

# Collect birth location
st.session_state.birth_location = st.text_input(
    label="Birth Location",
    value=st.session_state.birth_location,
    placeholder="City, Country"
)

if st.button('Save'):
    latitude, longitude, timezone = get_location_data(st.session_state.birth_location)
    st.session_state.latitude = latitude
    st.session_state.longitude = longitude
    st.session_state.timezone = timezone

    # Create a timezone-aware datetime object for the given birth time
    tz = pytz.timezone(st.session_state.timezone)

    naive_dt = dt.datetime.combine(
        st.session_state.birth_date,
        dt.time(hour=st.session_state.birth_hour, minute=st.session_state.birth_minute)
    )
    localized_dt = tz.localize(naive_dt)  # Make the datetime timezone-aware
    utc_dt = localized_dt.astimezone(pytz.utc)

    st.session_state.birth_dt = utc_dt
    st.session_state.birth_jd = dt_to_jd(st.session_state.birth_dt)

    st.success("Data saved successfully!")
