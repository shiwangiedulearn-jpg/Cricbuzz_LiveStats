def parse_venue_details(data, venue_id):
    """Extract useful venue information."""

    capacity = data.get("capacity")

    if capacity:
        capacity = int(capacity.replace(",", ""))

    return {
        "venue_id": venue_id,
        "ground": data.get("ground"),
        "city": data.get("city"),
        "country": data.get("country"),
        "capacity": capacity,
        "home_team": data.get("homeTeam")
    }