import swisseph as swe

def calculate_houses(jd, lat, lon, method='Placidus'):
    """
    Calculates the house cusps for a given Julian Day and geographic location.

    Args:
        jd (float): Julian Day.
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        method (str): House system code (e.g., 'Placidus', 'Koch', etc).

    Returns:
        list: List of 12 house cusp longitudes in degrees.
    """
    cusps = swe.houses(jd, lat, lon, method)[0]
    return cusps


def calculate_planet(jd, planet_id):
    """
    Calculates the position and motion of a planet for a given Julian Day.

    Args:
        jd (float): Julian Day.
        planet_id (int): Swiss Ephemeris planet constant (e.g., swe.SUN = 0).

    Returns:
        tuple: (longitude, latitude, distance, longitude_speed, latitude_speed, distance_speed)
    """
    return swe.calc_ut(jd, planet_id)[0]


def find_house(jd, planet_id, lat, lon, hsys=b'P'):
    """
    Determines the astrological house position of a planet.

    Args:
        jd (float): Julian Day.
        planet_id (int): Swiss Ephemeris planet constant (e.g., swe.MOON = 1).
        lat (float): Latitude of location (in degrees).
        lon (float): Longitude of location (in degrees).
        hsys (bytes): House system (default: b'P' = Placidus).

    Returns:
        int: House number (1–12) where the planet is located.
    """
    armc = swe.sidtime(jd) * 15 + lon
    eps = swe.calc_ut(jd, swe.ECL_NUT)[0][0]  # Obliquity of the ecliptic
    planet_pos = swe.calc_ut(jd, planet_id)[0]
    ecl_lon = planet_pos[0]
    ecl_lat = planet_pos[1]

    xpin = (ecl_lon, ecl_lat)
    serr = bytes(256)

    house_number = int(swe.house_pos(armc, lat, eps, xpin, hsys))
    return house_number


def angle_difference(angle1, angle2):
    """
    Computes the absolute angular distance between two celestial longitudes.

    Args:
        angle1 (float): First angle in degrees.
        angle2 (float): Second angle in degrees.

    Returns:
        float: Angular difference in degrees (0 to 180).
    """
    return abs(swe.difdeg2n(angle1, angle2))
