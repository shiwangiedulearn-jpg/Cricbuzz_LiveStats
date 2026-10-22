import requests

from api.client import HEADERS, BASE_URL


def get_venue_details(venue_id):
    """Fetch detailed information about a venue."""

    url = f"{BASE_URL}/venues/v1/{venue_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()