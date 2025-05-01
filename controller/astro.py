import swisseph as swe
import streamlit as st
from backend.ephemeris import calculate_houses, find_house, angle_difference

def calculate_sign(longitude):
    """
    Calculate the zodiac sign for a given planetary longitude.

    Args:
        longitude (float): Longitude of the planet in degrees.

    Returns:
        int: The zodiac sign corresponding to the longitude (0-11).
    """
    return int(longitude // 30)

def sign_string(lon):
    """
    Converts a celestial longitude into a formatted string representing its zodiac sign and position.

    Args:
        lon (float): Longitude in degrees (0° to 360°).

    Returns:
        str: A string in the format "♈︎ 12° 34' 56″", indicating the sign and exact position.
    """

    # Determine which zodiac sign the longitude falls in (0–11)
    sign_index = calculate_sign(lon)
    sign_symbol = st.session_state.signs[sign_index]['symbol']

    # Convert longitude to degree-minute-second format within the sign
    relative_degree = lon % 30
    deg = int(relative_degree)
    minutes = (relative_degree - deg) * 60
    min_ = int(minutes)
    sec = round((minutes - min_) * 60)

    return f'{sign_symbol} {deg}° {min_}\' {sec}″'

def find_aspect(lon1, lon2):
    """
    Determines whether there is a major aspect between two longitudes based on predefined angles and orbs.

    Args:
        lon1 (float): Longitude of the first body (in degrees).
        lon2 (float): Longitude of the second body (in degrees).

    Returns:
        int or None: The ID of the matching aspect if found, or None if no aspect is within orb.
    """

    diff = angle_difference(lon1, lon2)

    for aspect_id, aspect in st.session_state.aspects.items():
        target_angle = aspect['angle']
        tolerance = aspect['orb']
        if abs(diff - target_angle) <= tolerance:
            return aspect_id

    return None

def is_dissociative(sign1, sign2, aspect_id):
    """
    Returns True if the aspect between two signs is dissociative (non-standard zodiacal configuration).
    Uses the zodiacal distance between signs and aspect type.

    Args:
        sign1 (int): Index of the first zodiac sign (0-11)
        sign2 (int): Index of the second zodiac sign (0-11)
        aspect_id (int): ID of the aspect based on angle

    Returns:
        bool: True if the aspect is dissociative, False otherwise
    """

    distance = abs(sign1 - sign2) % 12

    aspect_distances = {
        0: [0],        # Conjunction
        1: [6],        # Opposition
        2: [4, 8],     # Trine
        3: [3, 9],     # Square
        4: [2, 10]     # Sextile
    }

    expected = aspect_distances.get(aspect_id, [])
    return distance not in expected


def generate_chart(jd, latitude, longitude, house_system=b'P'):
    """
    Generates the natal chart: houses, planetary positions, and aspects.

    Args:
        jd (float): Julian day
        latitude (float): Birth latitude
        longitude (float): Birth longitude
        house_system (bytes): House calculation system (default: Placidus)

    Returns:
        tuple: (houses, planets, aspects)
    """
    cusps = calculate_houses(jd, latitude, longitude, method=house_system)

    house_list = [{
        'House': i + 1,
        'Cusp': cusps[i],
        'Longitude': sign_string(cusps[i]),
    } for i in range(12)]

    planet_list = []
    for id, planet in st.session_state.planets.items():
        lon, lat, dist, lon_speed, *_ = swe.calc_ut(jd, id)[0]
        planet_list.append({
            'Symbol': planet['symbol'],
            'Name': planet['name'],
            'Direction': "℞" if lon_speed < 0 else "",
            'Lon': lon,
            'Sign': calculate_sign(lon),
            'Longitude': sign_string(lon),
            'House': find_house(jd, id, latitude, longitude)
        })

    aspect_list = []
    for i, planet1 in enumerate(planet_list):
        for j, planet2 in enumerate(planet_list):
            if j <= i:
                continue  # Skip repeated pairs and self-aspects

            aspect_id = find_aspect(planet1['Lon'], planet2['Lon'])
            if aspect_id is not None:
                aspect_list.append({
                    'Planet1': planet1['Symbol'],
                    'Planet2': planet2['Symbol'],
                    'Aspect': st.session_state.aspects[aspect_id]['name'],
                    'Symbol': st.session_state.aspects[aspect_id]['symbol'],
                    'Angle': round(angle_difference(planet1['Lon'], planet2['Lon']), 2),
                    'Dissociate': is_dissociative(planet1['Sign'], planet2['Sign'], aspect_id),
                })

    return house_list, planet_list, aspect_list

def generate_progressed_chart(progressed_jd, latitude, longitude, natal_jd, house_system=b'P'):
    """
    Generates a secondary progressed chart using the day-for-a-year method.

    Args:
        progressed_jd (float): Target Julian Day for the progressed chart (UTC).
        latitude (float): Latitude of the observation location.
        longitude (float): Longitude of the observation location.
        natal_jd (float): Natal Julian Day.
        house_system (bytes): House system (default: b'P' for Placidus).

    Returns:
        tuple: (house_list, planet_list, aspect_list)
            - house_list: List of 12 houses with cusps and positions.
            - planet_list: Planetary positions and directions.
            - aspect_list: List of aspects between planets, including dissociative flag.
    """
    # Convert elapsed time into "days of life" for progression
    years_elapsed = (progressed_jd - natal_jd) / 365.24219893
    progression_jd = natal_jd + years_elapsed  # For houses only

    # Compute house cusps
    cusps = calculate_houses(progression_jd, latitude, longitude, method=house_system)

    house_list = [
        {
            'House': i + 1,
            'Cusp': cusp % 360,
            'Longitude': sign_string(cusp % 360),
        }
        for i, cusp in enumerate(cusps[:12])
    ]

    # Compute progressed planetary positions
    planet_list = []
    for id, planet in st.session_state.planets.items():
        lon, lat, dist, lon_speed, lat_speed, dist_speed = swe.calc_ut(progressed_jd, id)[0]
        planet_list.append({
            'Symbol': planet['symbol'],
            'Name': planet['name'],
            'Direction': "℞" if lon_speed < 0 else "",
            'Lon': lon,
            'Sign': calculate_sign(lon),
            'Longitude': sign_string(lon),
            'House': find_house(progressed_jd, id, latitude, longitude)
        })

    # Calculate aspects between planets
    aspect_list = []
    for i, planet1 in enumerate(planet_list):
        for j, planet2 in enumerate(planet_list):
            if j <= i:
                continue  # Skip duplicates and self-aspects

            aspect_id = find_aspect(planet1['Lon'], planet2['Lon'])
            if aspect_id is not None:
                aspect_list.append({
                    'Planet1': planet1['Symbol'],
                    'Planet2': planet2['Symbol'],
                    'Aspect': st.session_state.aspects[aspect_id]['name'],
                    'Symbol': st.session_state.aspects[aspect_id]['symbol'],
                    'Angle': round(angle_difference(planet1['Lon'], planet2['Lon']), 2),
                    'Dissociate': is_dissociative(planet1['Sign'], planet2['Sign'], aspect_id),
                })

    return house_list, planet_list, aspect_list
