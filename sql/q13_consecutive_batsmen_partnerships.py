from sqlalchemy import text
from database.database import engine


query = """
SELECT
    p.batsman1_name,
    p.batsman2_name,
    p.total_runs AS combined_runs,
    p.match_id,
    p.innings_id

FROM partnerships p

WHERE p.total_runs >= 100

ORDER BY p.total_runs DESC;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nConsecutive Batsmen with Combined Partnership >= 100")
    print("-" * 100)

    for row in result:
        print(row)