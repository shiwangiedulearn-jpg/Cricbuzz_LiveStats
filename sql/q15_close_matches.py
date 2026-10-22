from sqlalchemy import text
from database.database import engine


query = """
WITH close_matches AS (

    SELECT
        match_id,
        team1,
        team2,
        status,

        CASE
            WHEN status LIKE '% won by % runs'
            THEN CAST(
                substr(
                    status,
                    instr(status, ' won by ') + 8,
                    instr(status, ' runs')
                    - (instr(status, ' won by ') + 8)
                ) AS INTEGER
            )

            ELSE NULL
        END AS run_margin,

        CASE
            WHEN status LIKE '% won by % wkts'
            THEN CAST(
                substr(
                    status,
                    instr(status, ' won by ') + 8,
                    instr(status, ' wkts')
                    - (instr(status, ' won by ') + 8)
                ) AS INTEGER
            )

            ELSE NULL
        END AS wicket_margin

    FROM matches

    WHERE state = 'Complete'
      AND status LIKE '% won by %'
),

filtered_close_matches AS (

    SELECT *
    FROM close_matches

    WHERE
        (run_margin IS NOT NULL AND run_margin < 50)
        OR
        (wicket_margin IS NOT NULL AND wicket_margin < 5)
),

player_close_performance AS (

    SELECT
        b.player_id,
        b.player_name,

        COUNT(DISTINCT b.match_id) AS close_matches,

        ROUND(
            AVG(b.runs),
            2
        ) AS average_runs,

        SUM(
            CASE
                WHEN fcm.status LIKE b.team || ' won by %'
                THEN 1
                ELSE 0
            END
        ) AS close_matches_won_when_batted

    FROM batting b

    JOIN filtered_close_matches fcm
        ON b.match_id = fcm.match_id

    GROUP BY
        b.player_id,
        b.player_name
)

SELECT
    player_name,
    average_runs,
    close_matches,
    close_matches_won_when_batted

FROM player_close_performance

ORDER BY
    close_matches DESC,
    average_runs DESC;
"""


with engine.connect() as connection:

    result = connection.execute(text(query))

    print("\nPlayer Performance in Close Matches")
    print("-" * 80)

    for row in result:
        print(row)