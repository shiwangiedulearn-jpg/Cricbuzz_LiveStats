from sqlalchemy import text
from database.database import engine

query = """
SELECT
    b.player_name,
    m.format,
    COUNT(DISTINCT b.match_id) AS matches,
    ROUND(
        CAST(SUM(b.runs) AS FLOAT) /
        NULLIF(SUM(b.balls), 0) * 6,
        2
    ) AS average_economy,
    ROUND(CAST(SUM(b.balls) AS FLOAT) / COUNT(DISTINCT b.match_id) / 6, 2)
        AS average_overs_per_match
FROM bowling b
JOIN matches m ON b.match_id = m.match_id
WHERE m.format IN ('ODI', 'T20')
GROUP BY b.player_id, b.player_name, m.format
HAVING COUNT(DISTINCT b.match_id) >= 10
   AND CAST(SUM(b.balls) AS FLOAT) / COUNT(DISTINCT b.match_id) >= 12
ORDER BY average_economy ASC;
"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    print("\nEconomical Limited-Overs Bowlers")
    print("-" * 90)
    for row in result:
        print(row)
