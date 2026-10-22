from sqlalchemy import text
from database.database import engine

# Q2 - Show matches played in the last 30 days.
#
# Required:
# - match description
# - both team names
# - venue with city
# - match date
# - most recent first
#
# start_date is stored as Unix milliseconds in the current database.

query = """
SELECT
    match_description,
    team1,
    team2,
    venue,
    city,
    datetime(
        CAST(start_date AS INTEGER) / 1000,
        'unixepoch'
    ) AS match_date
FROM matches
WHERE CAST(start_date AS INTEGER) >=
      (strftime('%s', 'now', '-30 days') * 1000)
ORDER BY CAST(start_date AS INTEGER) DESC;
"""

with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()

print("\nQ2 - Matches Played in the Last 30 Days")
print("-" * 100)

if not rows:
    print("No matches found in the last 30 days.")
else:
    for row in rows:
        print(row)
