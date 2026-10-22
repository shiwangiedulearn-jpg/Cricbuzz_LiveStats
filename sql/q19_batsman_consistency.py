from sqlalchemy import text
from database.database import engine

query = """
SELECT
    b.player_name,
    COUNT(*) AS innings,
    ROUND(AVG(b.runs), 2) AS average_runs,
    ROUND(
        sqrt(
            AVG(b.runs * b.runs) - AVG(b.runs) * AVG(b.runs)
        ),
        2
    ) AS stddev_runs
FROM batting b
JOIN matches m ON b.match_id = m.match_id
WHERE CAST(m.start_date AS INTEGER) >= 1640995200000
  AND b.balls >= 10
GROUP BY b.player_id, b.player_name
HAVING COUNT(*) >= 10
ORDER BY stddev_runs ASC;
"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    print("\nBatsman Consistency Since 2022")
    print("-" * 90)
    for row in result:
        print(row)
