"""
Settings Page
Allows the user to customize aspect orb values for astrological calculations.
"""

import streamlit as st
from config.loaders import initiate_aspects

# Initialize session state and load default aspect data
initiate_aspects()

# User input for orb values per aspect
st.subheader('Aspect Orbs')

for aspect_id, aspect in st.session_state.aspects.items():
    title_col, orb_col, deg_col = st.columns(3)

    # Display aspect name
    title_col.write(aspect['name'])

    # Input field for orb value
    st.session_state.aspects[aspect_id]['orb'] = orb_col.number_input(
        label=f'{aspect["name"]}_orb',
        min_value=0,
        max_value=15,
        value=st.session_state.aspects[aspect_id]['orb'],
        step=1,
        key=f'{aspect["name"]}_orb',
        label_visibility='collapsed'
    )

    deg_col.write('degrees')

# Save button
if st.button('Save settings'):
    st.info('Settings saved.', icon="🖋️")
