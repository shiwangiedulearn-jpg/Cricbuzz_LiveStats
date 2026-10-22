from sqlalchemy import text
from database.database import engine


query = """
WITH bowler_match AS (

    SELECT
        b.player_id,
        b.player_name,
        b.match_id,
        m.venue,

        SUM(b.balls) AS match_balls,
        SUM(b.runs) AS match_runs,
        SUM(b.wickets) AS match_wickets

    FROM bowling b

    JOIN matches m
        ON b.match_id = m.match_id

    GROUP BY
        b.player_id,
        b.player_name,
        b.match_id,
        m.venue

),

qualified_bowlers AS (

    SELECT
        player_id,
        player_name,
        venue

    FROM bowler_match

    GROUP BY
        player_id,
        player_name,
        venue

    HAVING
        COUNT(*) >= 3
        AND MIN(match_balls) >= 24

)

SELECT
    bm.player_name,
    bm.venue,

    COUNT(*) AS match_count,

    SUM(bm.match_wickets) AS total_wickets,

    ROUND(
        CAST(SUM(bm.match_runs) AS FLOAT)
        / NULLIF(SUM(bm.match_balls), 0) * 6,
        2
    ) AS average_economy

FROM bowler_match bm

JOIN qualified_bowlers qb
    ON bm.player_id = qb.player_id
    AND bm.venue = qb.venue

GROUP BY
    bm.player_id,
    bm.player_name,
    bm.venue

ORDER BY
    average_economy ASC;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nBowlers with at least 3 matches at a venue")
    print("and at least 4 overs in every match")
    print("-" * 90)

    for row in result:
        print(row)