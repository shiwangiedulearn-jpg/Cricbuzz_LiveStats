from sqlalchemy import text
from database.database import engine


query = """
SELECT
    b.player_name,
    SUM(b.runs) AS total_runs,
    SUM(bl.wickets) AS total_wickets

FROM batting b

JOIN bowling bl
    ON b.player_id = bl.player_id

GROUP BY
    b.player_id,
    b.player_name

HAVING
    SUM(b.runs) > 1000
    AND SUM(bl.wickets) > 50

ORDER BY
    total_runs DESC;
"""


with engine.connect() as connection:
    result = connection.execute(text(query))

    print("\nAll-rounders with >1000 Runs and >50 Wickets")
    print("-" * 70)

    rows = result.fetchall()

    if not rows:
        print("No players found.")
    else:
        for row in rows:
            print(row)