from database.database import SessionLocal, Match


def save_matches(matches):
    session = SessionLocal()

    try:
        for match_data in matches:

            existing_match = session.get(
                Match,
                match_data["match_id"]
            )

            if existing_match:
                # Update existing match
                for key, value in match_data.items():
                    setattr(existing_match, key, value)

            else:
                # Insert new match
                new_match = Match(**match_data)
                session.add(new_match)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()