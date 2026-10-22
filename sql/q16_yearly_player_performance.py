from sqlalchemy import text
from database.database import engine


query = """
WITH yearly_player AS (

    SELECT
        b.player_id,
        b.player_name,

        CAST(
            strftime(
                '%Y',
                datetime(
                    CAST(m.start_date AS INTEGER) / 1000,
                    'unixepoch'
                )
            ) AS INTEGER
        ) AS year,

        COUNT(DISTINCT b.match_id) AS matches,

        SUM(b.runs) AS total_runs,

        SUM(b.balls) AS total_balls

    FROM batting b

    JOIN matches m
        ON b.match_id = m.match_id

    WHERE CAST(m.start_date AS INTEGER) > 0

    GROUP BY
        b.player_id,
        b.player_name,
        year

    HAVING
        year >= 2020
        AND COUNT(DISTINCT b.match_id) >= 5
)

SELECT
    player_name,
    year,
    matches,

    ROUND(
        CAST(total_runs AS FLOAT)
        / matches,
        2
    ) AS avg_runs_per_match,

    ROUND(
        CAST(total_runs AS FLOAT)
        / NULLIF(total_balls, 0)
        * 100,
        2
    ) AS avg_strike_rate

FROM yearly_player

ORDER BY
    year,
    avg_runs_per_match DESC;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nYearly Player Performance Since 2020")
    print("-" * 90)

    for row in result:
        print(row)