import streamlit as st
import json

def load_json_file(file_path):
    """
    Load data from a JSON file with error handling.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict or list: Parsed data from the JSON file if successful.

    Raises:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If the file cannot be decoded.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON in file: {file_path}")


def initiate_houses():
    """
    Loads house data into Streamlit's session state from 'data/houses.json'.
    """
    if 'houses' not in st.session_state:
        houses_data = load_json_file('data/houses.json')
        st.session_state.houses = {
            house['id']: {
                'name': house['name'],
                'symbol': house['symbol'],
                'roman': house['roman_numeral']
            } for house in houses_data
        }


def initiate_signs():
    """
    Loads zodiac sign data into session state from 'data/signs.json'.
    """
    if 'signs' not in st.session_state:
        signs_data = load_json_file('data/signs.json')
        st.session_state.signs = {
            sign['id']: {
                'name': sign['name'],
                'symbol': sign['symbol'],
                'element': sign['element'],
                'modality': sign['modality'],
                'color': sign['color'],
                'rgb_color': sign['rgb_color']
            } for sign in signs_data
        }


def initiate_planets():
    """
    Loads planet data into session state from 'data/planets.json'.
    """
    if 'planets' not in st.session_state:
        planets_data = load_json_file('data/planets.json')
        st.session_state.planets = {
            planet['id']: {
                'name': planet['name'],
                'symbol': planet['symbol'],
                'type': planet['type']
            } for planet in planets_data
        }


def initiate_aspects():
    """
    Loads aspect data into session state from 'data/aspects.json'.
    """
    if 'aspects' not in st.session_state:
        aspects_data = load_json_file('data/aspects.json')
        st.session_state.aspects = {
            aspect['id']: {
                'name': aspect['name'],
                'symbol': aspect['symbol'],
                'angle': aspect['angle'],
                'orb': aspect['orb']
            } for aspect in aspects_data
        }
