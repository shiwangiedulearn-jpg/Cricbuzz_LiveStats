from sqlalchemy import text
from database.database import engine


query = """
SELECT
    substr(status, 1, instr(status, ' won') - 1) AS team_name,
    COUNT(*) AS total_wins
FROM matches
WHERE status LIKE '% won by %'
GROUP BY team_name
ORDER BY total_wins DESC;
"""


with engine.connect() as connection:
    result = connection.execute(text(query))

    print("\nTotal Wins by Team")
    print("-" * 50)

    for row in result:
        print(row)