from sqlalchemy import text
from database.database import engine


query = """
SELECT
    ground AS venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""


with engine.connect() as connection:
    result = connection.execute(text(query))

    print("\nVenues with capacity > 50,000")
    print("-" * 70)

    rows = result.fetchall()

    if not rows:
        print("No venues found.")

    else:
        for row in rows:
            print(row)