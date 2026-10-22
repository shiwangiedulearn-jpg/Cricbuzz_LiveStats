from sqlalchemy import text
from database.database import engine

query = """
WITH recent_matches AS (
    SELECT match_id, team1, team2, status,
           CASE WHEN status LIKE '% won by %'
                THEN substr(status, 1, instr(status, ' won by') - 1)
                ELSE NULL END AS winner
    FROM matches
    WHERE state = 'Complete'
      AND CAST(start_date AS INTEGER) >=
          (strftime('%s', 'now', '-3 years') * 1000)
),
team_pairs AS (
    SELECT CASE WHEN team1 < team2 THEN team1 ELSE team2 END AS team_a,
           CASE WHEN team1 < team2 THEN team2 ELSE team1 END AS team_b,
           winner
    FROM recent_matches
)
SELECT team_a, team_b, COUNT(*) AS matches,
       SUM(CASE WHEN winner = team_a THEN 1 ELSE 0 END) AS team_a_wins,
       SUM(CASE WHEN winner = team_b THEN 1 ELSE 0 END) AS team_b_wins,
       ROUND(CAST(SUM(CASE WHEN winner = team_a THEN 1 ELSE 0 END) AS FLOAT)
             / COUNT(*) * 100, 2) AS team_a_win_percentage
FROM team_pairs
GROUP BY team_a, team_b
HAVING COUNT(*) >= 5
ORDER BY matches DESC;
"""
with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()
print("\nQ22 - Head-to-Head Team Performance")
print("-" * 90)
if not rows:
    print("No qualifying team pairs found in the current dataset.")
else:
    for row in rows:
        print(row)
