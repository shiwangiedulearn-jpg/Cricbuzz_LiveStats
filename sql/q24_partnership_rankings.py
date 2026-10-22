from sqlalchemy import text
from database.database import engine

query = """
WITH partnership_stats AS (
    SELECT
        CASE WHEN batsman1_id < batsman2_id THEN batsman1_id ELSE batsman2_id END AS player1_id,
        CASE WHEN batsman1_id < batsman2_id THEN batsman2_id ELSE batsman1_id END AS player2_id,
        CASE WHEN batsman1_id < batsman2_id THEN batsman1_name ELSE batsman2_name END AS player1_name,
        CASE WHEN batsman1_id < batsman2_id THEN batsman2_name ELSE batsman1_name END AS player2_name,
        total_runs
    FROM partnerships
)
SELECT player1_name, player2_name, COUNT(*) AS partnerships,
       ROUND(AVG(total_runs), 2) AS average_partnership_runs,
       SUM(CASE WHEN total_runs > 50 THEN 1 ELSE 0 END) AS partnerships_over_50,
       MAX(total_runs) AS highest_partnership,
       ROUND(CAST(SUM(CASE WHEN total_runs >= 50 THEN 1 ELSE 0 END) AS FLOAT)
             / COUNT(*) * 100, 2) AS success_rate
FROM partnership_stats
GROUP BY player1_id, player2_id, player1_name, player2_name
HAVING COUNT(*) >= 5
ORDER BY average_partnership_runs DESC;
"""
with engine.connect() as connection:
    rows = connection.execute(text(query)).fetchall()
print("\nQ24 - Partnership Rankings")
print("-" * 90)
if not rows:
    print("No batting pairs have at least 5 partnerships in the current dataset.")
else:
    for rank, row in enumerate(rows, start=1):
        print(rank, row)
