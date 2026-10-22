from sqlalchemy import text

from database.database import engine


def get_database_counts():
    """Return basic database record counts."""
    queries = {
        "matches": "SELECT COUNT(*) FROM matches",
        "batting": "SELECT COUNT(*) FROM batting",
        "bowling": "SELECT COUNT(*) FROM bowling",
        "partnerships": "SELECT COUNT(*) FROM partnerships",
        "venues": "SELECT COUNT(*) FROM venues",
    }

    counts = {}

    with engine.connect() as connection:
        for name, query in queries.items():
            counts[name] = connection.execute(text(query)).scalar()

    return counts
