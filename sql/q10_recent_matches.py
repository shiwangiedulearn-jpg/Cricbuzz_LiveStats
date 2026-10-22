from sqlalchemy import text
from database.database import engine

query = """
SELECT
    match_description,
    team1,
    team2,
    CASE
        WHEN status LIKE '% won by %'
        THEN substr(status, 1, instr(status, ' won by') - 1)
        ELSE 'No winner'
    END AS winner,
    CASE
        WHEN status LIKE '% won by %'
        THEN substr(status, instr(status, ' won by') + 8)
        ELSE status
    END AS victory_margin,
    venue
FROM matches
WHERE state = 'Complete'
ORDER BY CAST(start_date AS INTEGER) DESC
LIMIT 20;
"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    print("\nLast 20 Completed Matches")
    print("-" * 100)
    for row in result:
        print(row)
