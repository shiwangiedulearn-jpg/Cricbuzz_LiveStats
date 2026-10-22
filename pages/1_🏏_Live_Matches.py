import streamlit as st
import pandas as pd

from api.client import get_live_matches
from api.parser import parse_live_matches
from database.database import SessionLocal, Match

st.title("🏏 Live Matches")

if st.button("🔄 Refresh Live Matches"):
    try:
        data = get_live_matches()
        matches = parse_live_matches(data)

        if matches:
            df = pd.DataFrame(matches)
            st.success(f"{len(matches)} live matches found.")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No live matches are currently available.")
    except Exception as e:
        st.error(f"Unable to fetch live matches: {e}")

st.divider()
st.subheader("Recently Stored Matches")

session = SessionLocal()
try:
    rows = (
        session.query(Match)
        .filter(Match.state == "Complete")
        .order_by(Match.match_id.desc())
        .limit(20)
        .all()
    )

    data = [
        {
            "Match": row.match_description,
            "Team 1": row.team1,
            "Team 2": row.team2,
            "Format": row.format,
            "Status": row.status,
            "Venue": row.venue,
        }
        for row in rows
    ]

    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("No completed matches found in the database.")
finally:
    session.close()
