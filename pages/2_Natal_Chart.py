"""
Birth Chart Page
Displays the natal (birth) chart information based on user input: planets, houses, and aspect matrix.
"""

import streamlit as st
from ui.display import build_aspect_matrix
from controller.astro import generate_chart
import pandas as pd

st.title('Birth Chart')

st.subheader('Personal Data')

# Show user's birth information
st.write(f'Name: {st.session_state.first_name} {st.session_state.last_name}')
st.write(f'Born on: {st.session_state.birth_date} at {st.session_state.birth_hour}:{st.session_state.birth_minute}')
st.write(f'Location: {st.session_state.birth_location} (Lat: {st.session_state.latitude}, Lon: {st.session_state.longitude})')

# Generate chart data
houses, planets, aspects = generate_chart(
    jd=st.session_state.birth_jd,
    latitude=st.session_state.latitude,
    longitude=st.session_state.longitude
)

# Organize data into tables
planets_col, houses_col = st.columns([2, 1])

planets_df = pd.DataFrame(planets)[[
    'Symbol', 'Name', 'Direction', 'Longitude', 'House'
]]

houses_df = pd.DataFrame(houses)[[
    'House', 'Longitude'
]]

# Display planetary positions
planets_col.subheader("Planets")
planets_col.dataframe(planets_df, use_container_width=True, hide_index=True)

# Display house cusps
houses_col.subheader("Houses")
houses_col.dataframe(houses_df, use_container_width=True, hide_index=True, height=450)

# Generate and display aspect matrix
aspect_matrix = build_aspect_matrix(planets, aspects)

st.subheader("Aspect Matrix")
st.dataframe(aspect_matrix, use_container_width=True, hide_index=False)
