from sqlalchemy import text
from database.database import engine

query = """
WITH quarterly_player AS (
    SELECT b.player_id, b.player_name,
           CAST(strftime('%Y', datetime(CAST(m.start_date AS INTEGER)/1000, 'unixepoch')) AS INTEGER) AS year,
           CAST(((CAST(strftime('%m', datetime(CAST(m.start_date AS INTEGER)/1000, 'unixepoch')) AS INTEGER)-1)/3)+1 AS INTEGER) AS quarter,
           COUNT(DISTINCT b.match_id) AS matches,
           SUM(b.runs) AS total_runs,
           SUM(b.balls) AS total_balls
    FROM batting b
    JOIN matches m ON b.match_id = m.match_id
    WHERE CAST(m.start_date AS INTEGER) > 0
    GROUP BY b.player_id, b.player_name, year, quarter
)
SELECT player_name, year, quarter, matches,
       ROUND(CAST(total_runs AS FLOAT)/NULLIF(matches,0),2) AS avg_runs_per_match,
       ROUND(CAST(total_runs AS FLOAT)/NULLIF(total_balls,0)*100,2) AS strike_rate
FROM quarterly_player
ORDER BY player_name, year, quarter;
"""
with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()
print("\nQ25 - Quarterly Player Performance Evolution")
print("-" * 100)
if not rows:
    print("No quarterly player performance data found.")
else:
    for row in rows:
        print(row)
print("\nNote: QoQ and career-phase thresholds are not specified.")
