import streamlit as st
import datetime as dt
from config.loaders import initiate_houses, initiate_signs, initiate_planets

def init_session_state():
    """
    Initializes default values in Streamlit's session state for both natal and progressed charts.
    Also loads core astrological data (houses, signs, planets) if not already loaded.
    """
    # Load reference data
    initiate_houses()
    initiate_signs()
    initiate_planets()
    
    # Initialize natal data
    if 'birth_date' not in st.session_state:
        st.session_state.birth_date = dt.date.today()
    if 'birth_hour' not in st.session_state:
        st.session_state.birth_hour = 0
    if 'birth_minute' not in st.session_state:
        st.session_state.birth_minute = 0
    if 'first_name' not in st.session_state:
        st.session_state.first_name = ''
    if 'last_name' not in st.session_state:
        st.session_state.last_name = ''
    if 'birth_location' not in st.session_state:
        st.session_state.birth_location = ''

    # Initialize progressed data
    if 'progressed_date' not in st.session_state:
        st.session_state.progressed_date = dt.date.today()
    if 'progressed_hour' not in st.session_state:
        st.session_state.progressed_hour = 0
    if 'progressed_minute' not in st.session_state:
        st.session_state.progressed_minute = 0
    if 'progressed_location' not in st.session_state:
        st.session_state.progressed_location = st.session_state.birth_location
