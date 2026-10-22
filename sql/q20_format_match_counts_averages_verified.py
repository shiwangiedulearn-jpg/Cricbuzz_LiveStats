from sqlalchemy import text
from database.database import engine

query = """
WITH player_matches AS (
    SELECT
        b.player_id,
        b.player_name,
        m.format,
        COUNT(DISTINCT b.match_id) AS batting_matches,
        SUM(b.runs) AS total_runs,
        SUM(
            CASE
                WHEN b.dismissal IS NOT NULL
                     AND b.dismissal != ''
                THEN 1 ELSE 0
            END
        ) AS dismissals
    FROM batting b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, b.player_name, m.format
),
eligible AS (
    SELECT
        player_id
    FROM player_matches
    GROUP BY player_id
    HAVING SUM(batting_matches) >= 20
)
SELECT
    pm.player_name,
    pm.format,
    pm.batting_matches,
    ROUND(
        CAST(pm.total_runs AS FLOAT) /
        NULLIF(pm.dismissals, 0),
        2
    ) AS batting_average
FROM player_matches pm
JOIN eligible e
    ON pm.player_id = e.player_id
ORDER BY pm.player_name, pm.format;
"""

with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()

print("\nQ20 - Players with at least 20 total batting appearances")
print("-" * 90)

if not rows:
    print("No qualifying players found in the current dataset.")
else:
    for row in rows:
        print(row)
