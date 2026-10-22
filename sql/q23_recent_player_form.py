from sqlalchemy import text
from database.database import engine

query = """
WITH recent_batting AS (
    SELECT b.player_id, b.player_name, b.match_id, m.start_date,
           b.runs, b.balls, b.strike_rate,
           ROW_NUMBER() OVER (
               PARTITION BY b.player_id
               ORDER BY CAST(m.start_date AS INTEGER) DESC
           ) AS innings_rank
    FROM batting b
    JOIN matches m ON b.match_id = m.match_id
)
SELECT player_name,
       ROUND(AVG(CASE WHEN innings_rank <= 5 THEN runs END), 2) AS avg_runs_last_5,
       ROUND(AVG(runs), 2) AS avg_runs_last_10,
       ROUND(AVG(CASE WHEN innings_rank <= 5 THEN strike_rate END), 2) AS avg_strike_rate_last_5,
       SUM(CASE WHEN innings_rank <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS scores_50_plus,
       ROUND(sqrt(AVG(CASE WHEN innings_rank <= 10 THEN runs*runs END)
             - AVG(CASE WHEN innings_rank <= 10 THEN runs END)
             * AVG(CASE WHEN innings_rank <= 10 THEN runs END)), 2) AS stddev_runs
FROM recent_batting
WHERE innings_rank <= 10
GROUP BY player_id, player_name
HAVING COUNT(*) >= 10
ORDER BY avg_runs_last_10 DESC;
"""
with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()
print("\nQ23 - Recent Player Form")
print("-" * 90)
if not rows:
    print("No players have 10 batting performances in the current dataset.")
else:
    for row in rows:
        print(row)
print("\nNote: Excellent/Good/Average/Poor thresholds are not specified.")
