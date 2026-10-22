from sqlalchemy import text
from database.database import engine

query = """
SELECT
    winner AS team_name,
    SUM(CASE WHEN home_away = 'Home' THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN home_away = 'Away' THEN 1 ELSE 0 END) AS away_wins
FROM (
    SELECT
        CASE
            WHEN status LIKE '% won by %'
            THEN substr(status, 1, instr(status, ' won by') - 1)
        END AS winner,
        CASE
            WHEN instr(status, team1) = 1 THEN
                CASE WHEN venue IS NOT NULL THEN 'Home' ELSE 'Away' END
        END AS home_away
    FROM matches
    WHERE state = 'Complete'
      AND status LIKE '% won by %'
) x
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY (home_wins + away_wins) DESC;
"""

print("\nQ12 note: The current matches table does not reliably contain the team's country and venue country.")
print("A fully correct home-vs-away analysis therefore requires country metadata.")
print("The query below is only a placeholder and should NOT be used as the final Q12 result.")

with engine.connect() as connection:
    result = connection.execute(text(query))
    for row in result:
        print(row)
