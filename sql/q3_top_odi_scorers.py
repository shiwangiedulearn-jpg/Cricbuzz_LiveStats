from sqlalchemy import text
from database.database import engine


query = """
SELECT
    b.player_name,
    SUM(b.runs) AS total_runs,

    ROUND(
        CAST(SUM(b.runs) AS FLOAT) /
        NULLIF(
            SUM(
                CASE
                    WHEN b.dismissal IS NOT NULL
                         AND b.dismissal != ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS batting_average,

    SUM(
        CASE
            WHEN b.runs >= 100 THEN 1
            ELSE 0
        END
    ) AS centuries

FROM batting b

JOIN matches m
    ON b.match_id = m.match_id

WHERE m.format = 'ODI'

GROUP BY b.player_id, b.player_name

ORDER BY total_runs DESC

LIMIT 10;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nTop 10 ODI Run Scorers")
    print("-" * 70)

    for row in result:
        print(row)