import requests

from api.client import HEADERS, BASE_URL


def get_upcoming_matches():
    """Fetch upcoming cricket matches."""

    url = f"{BASE_URL}/matches/v1/upcoming"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()