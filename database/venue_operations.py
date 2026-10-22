from database.database import SessionLocal, Venue


def save_venue(venue_data):
    """Save or update venue information."""

    session = SessionLocal()

    try:
        existing = session.get(
            Venue,
            venue_data["venue_id"]
        )

        if existing:
            for key, value in venue_data.items():
                setattr(existing, key, value)
        else:
            session.add(Venue(**venue_data))

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()