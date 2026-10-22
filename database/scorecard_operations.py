from database.database import (
    SessionLocal,
    Batting,
    Bowling,
    Partnership,
    FallOfWicket
)


def save_scorecard(scorecard_data, match_id):
    session = SessionLocal()

    try:
        # Remove old scorecard data for this match
        session.query(Batting).filter(
            Batting.match_id == match_id
        ).delete()

        session.query(Bowling).filter(
            Bowling.match_id == match_id
        ).delete()

        session.query(Partnership).filter(
            Partnership.match_id == match_id
        ).delete()

        session.query(FallOfWicket).filter(
            FallOfWicket.match_id == match_id
        ).delete()

        # Insert batting records
        for data in scorecard_data["batting"]:
            session.add(Batting(**data))

        # Insert bowling records
        for data in scorecard_data["bowling"]:
            session.add(Bowling(**data))

        # Insert partnership records
        for data in scorecard_data["partnerships"]:
            session.add(Partnership(**data))

        # Insert fall-of-wicket records
        for data in scorecard_data["fall_of_wickets"]:
            session.add(FallOfWicket(**data))

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

def scorecard_exists(match_id):
    session = SessionLocal()

    try:
        record = (
            session.query(Batting)
            .filter(Batting.match_id == match_id)
            .first()
        )

        return record is not None

    finally:
        session.close()