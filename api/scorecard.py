import requests

from api.client import HEADERS, BASE_URL


def get_scorecard(match_id):
    """Fetch scorecard for a specific match."""

    url = f"{BASE_URL}/mcenter/v1/{match_id}/scard"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()