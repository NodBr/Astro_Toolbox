"""
Progressed Chart Page
Collects user data to generate a secondary progressed chart based on the day-for-a-year method.
"""

import streamlit as st
import pandas as pd
import datetime as dt
import pytz

from ui.display import build_aspect_matrix
from controller.astro import generate_progressed_chart
from services.geolocation import get_location_data
from controller.time_utils import dt_to_jd, jd_to_dt, get_solar_year
from config.init_session import init_session_state

st.title("Progressed Chart")

# User input for progressed date and time
st.subheader("Enter your progressed data")

date_col, hour_col, minute_col = st.columns([2, 1, 1])

# Collect progressed date
st.session_state.progressed_date = date_col.date_input(
    label="Progressed Date",
    value=st.session_state.progressed_date,
    min_value=dt.date(1, 1, 1),
    max_value=dt.date(2999, 12, 31),
    format="DD/MM/YYYY"
)

# Collect progressed time
st.session_state.progressed_hour = hour_col.number_input(
    label='Hour (Local Time)',
    min_value=0,
    max_value=23,
    value=st.session_state.progressed_hour,
    step=1,
    key='progr_hour'
)

st.session_state.progressed_minute = minute_col.number_input(
    label='Minute',
    min_value=0,
    max_value=59,
    value=st.session_state.progressed_minute,
    step=1,
    key='progr_minute'
)

# Collect progressed location
st.session_state.progressed_location = st.text_input(
    label="Progressed Location",
    value=st.session_state.progressed_location,
    placeholder="City, Country"
)

if st.button('Generate Progressed Chart'):
    latitude, longitude, timezone = get_location_data(st.session_state.progressed_location)
    st.session_state.progressed_latitude = latitude
    st.session_state.progressed_longitude = longitude
    st.session_state.progressed_timezone = timezone

    # Create a timezone-aware datetime object
    tz = pytz.timezone(st.session_state.progressed_timezone)

    naive_progressed_dt = dt.datetime.combine(
        st.session_state.progressed_date,
        dt.time(hour=st.session_state.progressed_hour, minute=st.session_state.progressed_minute)
    )
    progressed_localized_dt = tz.localize(naive_progressed_dt)
    progressed_utc_dt = progressed_localized_dt.astimezone(pytz.utc)

    st.session_state.progressed_dt = progressed_utc_dt
    st.session_state.progressed_jd = dt_to_jd(progressed_utc_dt)

    st.write("Progressed datetime (UTC):", st.session_state.progressed_dt)

    # Calculate equivalent target day using solar year ratio
    time_period = st.session_state.progressed_jd - st.session_state.birth_jd
    st.write("Time period (days):", time_period)

    solar_year_length = get_solar_year(st.session_state.birth_jd)
    st.write("Solar year length (days):", solar_year_length)

    target_jd = st.session_state.birth_jd + time_period / solar_year_length
    target_dt = jd_to_dt(target_jd)
    st.write(f"Target datetime (UTC): {target_dt}")

    # Generate progressed chart
    houses, planets, aspects = generate_progressed_chart(
        progressed_jd=target_jd,
        latitude=latitude,
        longitude=longitude,
        natal_jd=st.session_state.birth_jd
    )

    # Display chart data
    planets_col, houses_col = st.columns([2, 1])

    planets_df = pd.DataFrame(planets)[[
        'Symbol', 'Name', 'Direction', 'Longitude', 'House'
    ]]
    houses_df = pd.DataFrame(houses)[[
        'House', 'Longitude'
    ]]

    planets_col.subheader("Planets")
    planets_col.dataframe(planets_df, use_container_width=True, hide_index=True)

    houses_col.subheader("Houses")
    houses_col.dataframe(houses_df, use_container_width=True, hide_index=True, height=450)

    aspect_matrix = build_aspect_matrix(planets, aspects)

    st.subheader("Aspect Matrix")
    st.dataframe(aspect_matrix, use_container_width=True, hide_index=False)
