import streamlit as st
import pandas as pd
from sqlalchemy import text

from database.database import engine

st.title("📈 SQL Analytics")

queries = {
    "Q3 - Top 10 ODI Run Scorers": """
        SELECT
            b.player_name,
            SUM(b.runs) AS total_runs,
            ROUND(
                CAST(SUM(b.runs) AS FLOAT) /
                NULLIF(
                    SUM(CASE
                        WHEN b.dismissal IS NOT NULL
                             AND b.dismissal != ''
                        THEN 1 ELSE 0
                    END), 0
                ), 2
            ) AS batting_average,
            SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS centuries
        FROM batting b
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.format = 'ODI'
        GROUP BY b.player_id, b.player_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    "Q4 - Venues Above 50,000 Capacity": """
        SELECT ground, city, country, capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
    """,

    "Q5 - Total Wins by Team": """
        SELECT
            substr(status, 1, instr(status, ' won') - 1) AS team_name,
            COUNT(*) AS total_wins
        FROM matches
        WHERE status LIKE '% won by %'
        GROUP BY team_name
        ORDER BY total_wins DESC;
    """,

    "Q7 - Highest Score by Format": """
        SELECT
            m.format,
            b.player_name,
            b.runs AS highest_score
        FROM batting b
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.format IN ('TEST', 'ODI', 'T20')
          AND b.runs = (
              SELECT MAX(b2.runs)
              FROM batting b2
              JOIN matches m2 ON b2.match_id = m2.match_id
              WHERE m2.format = m.format
          )
        ORDER BY
            CASE m.format
                WHEN 'TEST' THEN 1
                WHEN 'ODI' THEN 2
                WHEN 'T20' THEN 3
            END;
    """,

    "Q9 - All-Rounders": """
        WITH batting_totals AS (
            SELECT player_id, player_name, SUM(runs) AS total_runs
            FROM batting
            GROUP BY player_id, player_name
        ),
        bowling_totals AS (
            SELECT player_id, player_name, SUM(wickets) AS total_wickets
            FROM bowling
            GROUP BY player_id, player_name
        )
        SELECT
            b.player_name,
            b.total_runs,
            w.total_wickets
        FROM batting_totals b
        JOIN bowling_totals w ON b.player_id = w.player_id
        WHERE b.total_runs > 1000
          AND w.total_wickets > 50
        ORDER BY b.total_runs DESC;
    """,

    "Q13 - Partnerships Above 100 Runs": """
        SELECT
            batsman1_name,
            batsman2_name,
            total_runs AS combined_runs,
            match_id,
            innings_id
        FROM partnerships
        WHERE total_runs >= 100
        ORDER BY total_runs DESC;
    """,
}

selected = st.selectbox("Select SQL Question", list(queries.keys()))

if st.button("▶ Run Query"):
    try:
        with engine.connect() as connection:
            rows = connection.execute(text(queries[selected])).fetchall()

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No qualifying records found in the current dataset.")
    except Exception as e:
        st.error(f"Query failed: {e}")

st.divider()
st.caption(
    "The standalone SQL files in sql/ remain the source of the complete Q3-Q25 analysis. "
    "This page exposes the most useful working queries in the dashboard."
)
