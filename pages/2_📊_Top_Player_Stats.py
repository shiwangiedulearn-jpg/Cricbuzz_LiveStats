import streamlit as st
import pandas as pd
from sqlalchemy import text

from database.database import engine

st.title("📊 Top Player Statistics")

format_choice = st.selectbox(
    "Select Format",
    ["All", "TEST", "ODI", "T20"]
)

where_clause = ""
params = {}

if format_choice != "All":
    where_clause = "WHERE m.format = :format"
    params["format"] = format_choice

query = f"""
SELECT
    b.player_name,
    SUM(b.runs) AS total_runs,
    COUNT(DISTINCT b.match_id) AS matches,
    ROUND(
        CAST(SUM(b.runs) AS FLOAT) /
        NULLIF(
            SUM(
                CASE
                    WHEN b.dismissal IS NOT NULL
                         AND b.dismissal != ''
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    ) AS batting_average,
    MAX(b.runs) AS highest_score
FROM batting b
JOIN matches m ON b.match_id = m.match_id
{where_clause}
GROUP BY b.player_id, b.player_name
ORDER BY total_runs DESC
LIMIT 20;
"""

with engine.connect() as connection:
    rows = connection.execute(text(query), params).fetchall()

if rows:
    columns = [
        "Player",
        "Total Runs",
        "Matches",
        "Batting Average",
        "Highest Score",
    ]
    df = pd.DataFrame(rows, columns=columns)

    st.dataframe(df, use_container_width=True)

    st.subheader("Top 10 Run Scorers")
    chart_df = df.head(10).set_index("Player")
    st.bar_chart(chart_df["Total Runs"])
else:
    st.info("No batting data available.")
