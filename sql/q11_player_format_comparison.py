from sqlalchemy import text
from database.database import engine


query = """
WITH player_format AS (

    SELECT
        b.player_id,
        b.player_name,
        m.format,

        SUM(b.runs) AS total_runs,

        SUM(
            CASE
                WHEN b.dismissal IS NOT NULL
                     AND b.dismissal != ''
                THEN 1
                ELSE 0
            END
        ) AS dismissals

    FROM batting b

    JOIN matches m
        ON b.match_id = m.match_id

    WHERE m.format IN ('TEST', 'ODI', 'T20')

    GROUP BY
        b.player_id,
        b.player_name,
        m.format
),

eligible_players AS (

    SELECT
        player_id

    FROM player_format

    GROUP BY player_id

    HAVING COUNT(DISTINCT format) >= 2
),

player_summary AS (

    SELECT
        pf.player_id,
        pf.player_name,

        SUM(pf.total_runs) AS overall_runs,

        SUM(pf.dismissals) AS overall_dismissals,

        MAX(
            CASE
                WHEN pf.format = 'TEST'
                THEN pf.total_runs
            END
        ) AS test_runs,

        MAX(
            CASE
                WHEN pf.format = 'ODI'
                THEN pf.total_runs
            END
        ) AS odi_runs,

        MAX(
            CASE
                WHEN pf.format = 'T20'
                THEN pf.total_runs
            END
        ) AS t20_runs

    FROM player_format pf

    JOIN eligible_players ep
        ON pf.player_id = ep.player_id

    GROUP BY
        pf.player_id,
        pf.player_name
)

SELECT
    player_name,

    test_runs,
    odi_runs,
    t20_runs,

    ROUND(
        CAST(overall_runs AS FLOAT) /
        NULLIF(overall_dismissals, 0),
        2
    ) AS overall_batting_average

FROM player_summary

ORDER BY overall_batting_average DESC;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nPlayer Comparison Across Formats")
    print("-" * 100)

    for row in result:
        print(row)