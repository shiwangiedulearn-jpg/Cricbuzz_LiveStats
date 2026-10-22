import streamlit as st
from sqlalchemy import text

from database.database import engine

st.title("🛠️ CRUD Operations")

st.subheader("Create / Update Match")

match_id = st.number_input("Match ID", min_value=1, step=1)
team1 = st.text_input("Team 1")
team2 = st.text_input("Team 2")
match_description = st.text_input("Match Description")
match_format = st.selectbox("Format", ["TEST", "ODI", "T20"])
venue = st.text_input("Venue")
city = st.text_input("City")
status = st.text_input("Status")

if st.button("Save Match"):
    if not team1 or not team2:
        st.warning("Team 1 and Team 2 are required.")
    else:
        query = text("""
            INSERT INTO matches
            (
                match_id,
                match_description,
                format,
                status,
                team1,
                team2,
                venue,
                city
            )
            VALUES
            (
                :match_id,
                :match_description,
                :format,
                :status,
                :team1,
                :team2,
                :venue,
                :city
            )
            ON CONFLICT(match_id) DO UPDATE SET
                match_description = excluded.match_description,
                format = excluded.format,
                status = excluded.status,
                team1 = excluded.team1,
                team2 = excluded.team2,
                venue = excluded.venue,
                city = excluded.city
        """)

        try:
            with engine.begin() as connection:
                connection.execute(
                    query,
                    {
                        "match_id": match_id,
                        "match_description": match_description,
                        "format": match_format,
                        "status": status,
                        "team1": team1,
                        "team2": team2,
                        "venue": venue,
                        "city": city,
                    },
                )
            st.success("Match saved successfully.")
        except Exception as e:
            st.error(f"Unable to save match: {e}")

st.divider()
st.subheader("Read Matches")

if st.button("Load Matches"):
    with engine.connect() as connection:
        rows = connection.execute(
            text("""
                SELECT
                    match_id,
                    match_description,
                    format,
                    team1,
                    team2,
                    status,
                    venue,
                    city
                FROM matches
                ORDER BY match_id DESC
                LIMIT 50
            """)
        ).fetchall()

    for row in rows:
        st.write(row)

st.divider()
st.subheader("Delete Match")

delete_id = st.number_input(
    "Match ID to delete",
    min_value=1,
    step=1,
    key="delete_id",
)

if st.button("Delete Match"):
    try:
        with engine.begin() as connection:
            result = connection.execute(
                text("DELETE FROM matches WHERE match_id = :match_id"),
                {"match_id": delete_id},
            )

        if result.rowcount:
            st.success("Match deleted successfully.")
        else:
            st.warning("No match found with that ID.")
    except Exception as e:
        st.error(f"Unable to delete match: {e}")
