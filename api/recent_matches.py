import requests

from api.client import HEADERS, BASE_URL


def get_recent_matches():
    """Fetch recently completed/recent matches."""

    url = f"{BASE_URL}/matches/v1/recent"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()