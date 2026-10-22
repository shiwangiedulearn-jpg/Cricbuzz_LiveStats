import requests

from api.client import HEADERS, BASE_URL


def get_series_venues(series_id):
    """Fetch venue information for a series."""

    url = f"{BASE_URL}/series/v1/{series_id}/venues"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()