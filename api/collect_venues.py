from database.database import SessionLocal, Match
from api.venues import get_series_venues
from api.venue_details import get_venue_details
from database.venue_operations import save_venue


def collect_venues():
    """Collect venue details from all series in the database."""

    session = SessionLocal()

    try:
        series_ids = (
            session.query(Match.series_id)
            .filter(Match.series_id.isnot(None))
            .distinct()
            .all()
        )

    finally:
        session.close()

    print("Unique series found:", len(series_ids))

    processed = set()
    saved = 0

    for (series_id,) in series_ids:

        print(f"\nProcessing series: {series_id}")

        try:
            data = get_series_venues(series_id)

            for venue in data.get("seriesVenue", []):

                venue_id = venue.get("id")

                if not venue_id:
                    continue

                # Avoid requesting the same venue multiple times
                if venue_id in processed:
                    continue

                processed.add(venue_id)

                details = get_venue_details(venue_id)

                capacity = details.get("capacity")

                if not capacity:
                    continue

                # Handle values such as:
                # "11,600"
                # "3500 (Increased to 6000 by temporary seating)"

                capacity = int(
                    capacity.replace(",", "")
                    .split("(")[0]
                    .strip()
                )

                venue_data = {
                    "venue_id": venue_id,
                    "ground": details.get("ground"),
                    "city": details.get("city"),
                    "country": details.get("country"),
                    "capacity": capacity,
                    "home_team": details.get("homeTeam")
                }

                save_venue(venue_data)

                saved += 1

                print(
                    f"✓ {venue_data['ground']} - "
                    f"{venue_data['capacity']}"
                )

        except Exception as e:
            print(f"✗ Failed for series {series_id}: {e}")

    print("\n========== SUMMARY ==========")
    print("Unique venues processed:", len(processed))
    print("Venues saved:", saved)


if __name__ == "__main__":
    collect_venues()