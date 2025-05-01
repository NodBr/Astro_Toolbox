import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_location_data(city_name):
    """
    Retrieves latitude, longitude, and timezone name for a given city using the OpenCage Geocoding API.

    Parameters:
        city_name (str): City and country name (e.g., "Paris, France").

    Returns:
        tuple: (latitude, longitude, timezone) or (None, None, None) if not found.
    """
    api_key = os.getenv('GEO_API_KEY')  # Get API key from environment variable

    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        result = data['results'][0]
        latitude = result['geometry']['lat']
        longitude = result['geometry']['lng']
        timezone = result['annotations']['timezone']['name']
        return latitude, longitude, timezone
    else:
        return None, None, None
