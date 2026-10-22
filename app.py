import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import text

from database.database import engine
from api.client import get_live_matches
from api.parser import parse_live_matches

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- CSS --------------------
st.markdown("""
<style>
/* Hide Streamlit's default sidebar completely.
   IMPORTANT: also rename/delete the project's old pages/ folder because
   Streamlit automatically creates sidebar navigation from it. */
section[data-testid="stSidebar"] {display:none !important;}
[data-testid="stSidebarCollapsedControl"] {display:none !important;}
header[data-testid="stHeader"] {background:#07111f;}
footer {display:none;}

.stApp {
    background:#07111f;
    color:#f3f7fb;
}
.block-container {
    max-width:1700px;
    padding:7rem 2.6rem 3rem 2.6rem;
}

/* Header */
.header {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:8px 0 18px 0;
    border-bottom:1px solid #1b2a3c;
}
.logo {
    font-size:28px;
    line-height:1.2;
    font-weight:850;
    letter-spacing:-1px;
}
.logo .accent {color:#19c6bb;}
.tagline {margin-top:8px;color:#71839b;font-size:13px;}
.header-right {text-align:right;}
.header-chip {
    display:inline-block;
    border:1px solid #24425e;
    background:#10243a;
    color:#d8e7f5;
    border-radius:20px;
    padding:7px 12px;
    margin-left:6px;
    font-size:12px;
}

/* App navigation */
.nav-wrap {
    padding:15px 0 10px 0;
    border-bottom:1px solid #17263a;
}
div[role="radiogroup"] {
    gap:7px !important;
}
div[role="radiogroup"] > label {
    background:#0d1b2c;
    border:1px solid #223852;
    border-radius:9px;
    padding:8px 14px !important;
    color:#a9b9cc !important;
    font-weight:650;
}
div[role="radiogroup"] > label:hover {
    border-color:#19c6bb;
}
div[role="radiogroup"] > label:has(input:checked) {
    background:#0f6e6a;
    border-color:#19c6bb;
    color:#ffffff !important;
}

/* Controls */
.control-label {
    color:#71839b;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.2px;
    margin-bottom:5px;
}

/* KPI cards */
.kpi {
    background:#101e30;
    border:1px solid #20354c;
    border-radius:14px;
    padding:18px 20px;
    min-height:108px;
}
.kpi-label {
    color:#71839b;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.3px;
}
.kpi-value {
    margin-top:8px;
    font-size:31px;
    font-weight:850;
    color:#f4f8fc;
}
.kpi-note {
    color:#19c6bb;
    font-size:11px;
    margin-top:3px;
}

/* Cards */
.card {
    background:#101e30;
    border:1px solid #20354c;
    border-radius:14px;
    padding:18px;
    margin-top:18px;
}
.card-title {font-size:17px;font-weight:800;}
.card-subtitle {font-size:12px;color:#71839b;margin-top:4px;}

/* Match cards */
.match {
    background:#101e30;
    border:1px solid #20354c;
    border-radius:13px;
    padding:15px 17px;
    margin-bottom:10px;
}
.match-format {
    color:#19c6bb;
    font-size:10px;
    font-weight:850;
    letter-spacing:1px;
}
.match-teams {font-size:17px;font-weight:780;margin-top:6px;}
.match-meta {font-size:11px;color:#71839b;margin-top:6px;}
.match-status {font-size:12px;color:#dce7f3;margin-top:8px;}

/* Streamlit buttons */
.stButton > button {
    background:#10243a;
    border:1px solid #29445f;
    color:#f1f6fb;
    border-radius:9px;
    font-weight:700;
}
.stButton > button:hover {
    border-color:#19c6bb;
    color:#19c6bb;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border:1px solid #20354c;
    border-radius:12px;
    overflow:hidden;
}

/* Selectboxes */
div[data-baseweb="select"] > div {
    background:#101e30;
    border-color:#29445f;
}

/* Tabs */
button[data-baseweb="tab"] {
    color:#8495aa;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color:#19c6bb;
}

/* Make plot area blend into cards */
.js-plotly-plot .plotly {
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- Helpers --------------------
@st.cache_data(ttl=60)
def summary(fmt):
    params = {}
    where = ""
    if fmt != "All":
        where = "WHERE m.format = :format"
        params["format"] = fmt

    with engine.connect() as con:
        matches = con.execute(
            text(f"SELECT COUNT(*) FROM matches m {where}"), params
        ).scalar() or 0

        runs = con.execute(
            text(f"""
                SELECT COALESCE(SUM(b.runs),0)
                FROM batting b
                JOIN matches m ON b.match_id=m.match_id
                {where}
            """), params
        ).scalar() or 0

        wickets = con.execute(
            text(f"""
                SELECT COALESCE(SUM(b.wickets),0)
                FROM bowling b
                JOIN matches m ON b.match_id=m.match_id
                {where}
            """), params
        ).scalar() or 0

        players = con.execute(
            text(f"""
                SELECT COUNT(DISTINCT b.player_id)
                FROM batting b
                JOIN matches m ON b.match_id=m.match_id
                {where}
            """), params
        ).scalar() or 0

    return matches, runs, wickets, players


@st.cache_data(ttl=60)
def top_scorers(fmt):
    params = {}
    where = ""
    if fmt != "All":
        where = "WHERE m.format=:format"
        params["format"] = fmt

    with engine.connect() as con:
        return pd.read_sql(
            text(f"""
                SELECT b.player_name AS player, SUM(b.runs) AS runs
                FROM batting b
                JOIN matches m ON b.match_id=m.match_id
                {where}
                GROUP BY b.player_id,b.player_name
                ORDER BY runs DESC
                LIMIT 10
            """),
            con,
            params=params,
        )


@st.cache_data(ttl=60)
def format_counts():
    with engine.connect() as con:
        return pd.read_sql(
            text("""
                SELECT format, COUNT(*) AS matches
                FROM matches
                GROUP BY format
                ORDER BY matches DESC
            """),
            con,
        )


@st.cache_data(ttl=60)
def recent_matches():
    with engine.connect() as con:
        return pd.read_sql(
            text("""
                SELECT
                    match_description AS match,
                    team1,
                    team2,
                    format,
                    status,
                    venue
                FROM matches
                WHERE state='Complete'
                ORDER BY CAST(start_date AS INTEGER) DESC
                LIMIT 12
            """),
            con,
        )


@st.cache_data(ttl=60)
def player_leaderboard(fmt):
    params = {}
    where = ""
    if fmt != "All":
        where = "WHERE m.format=:format"
        params["format"] = fmt

    with engine.connect() as con:
        return pd.read_sql(
            text(f"""
                SELECT
                    b.player_name AS player,
                    SUM(b.runs) AS runs,
                    MAX(b.runs) AS best_score,
                    COUNT(DISTINCT b.match_id) AS appearances
                FROM batting b
                JOIN matches m ON b.match_id=m.match_id
                {where}
                GROUP BY b.player_id,b.player_name
                ORDER BY runs DESC
                LIMIT 25
            """),
            con,
            params=params,
        )


def kpi(label, value, note=""):
    return f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value:,}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """


def chart_layout(fig, height=410):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=12, b=8),
        paper_bgcolor="#101e30",
        plot_bgcolor="#101e30",
        font=dict(color="#cbd7e5"),
        xaxis=dict(
            gridcolor="#1c3046",
            zerolinecolor="#1c3046",
        ),
        yaxis=dict(
            gridcolor="#1c3046",
            zerolinecolor="#1c3046",
        ),
    )
    return fig


# -------------------- Header --------------------
st.markdown("""
<div class="header">
    <div>
        <div class="logo">Cricbuzz <span class="accent">LiveStats</span></div>
        <div class="tagline">Real-Time Cricket Insights · SQL-Based Analytics</div>
    </div>
    <div class="header-right">
        <span class="header-chip">🏏 Sports Analytics</span>
        <span class="header-chip">● Live Data</span>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.radio(
    "Application Navigation",
    ["Dashboard", "Live Matches", "Player Analytics", "SQL Analytics", "CRUD"],
    horizontal=True,
    label_visibility="collapsed",
)

# -------------------- Dashboard --------------------
if page == "Dashboard":
    st.markdown('<div class="nav-wrap"></div>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([1, 1, 1, .55])

    with f1:
        st.markdown('<div class="control-label">FORMAT</div>', unsafe_allow_html=True)
        fmt = st.selectbox(
            "format",
            ["All", "TEST", "ODI", "T20"],
            label_visibility="collapsed",
        )

    with f2:
        st.markdown('<div class="control-label">DATASET</div>', unsafe_allow_html=True)
        st.selectbox(
            "dataset",
            ["Collected API Data"],
            label_visibility="collapsed",
        )

    with f3:
        st.markdown('<div class="control-label">VIEW</div>', unsafe_allow_html=True)
        st.selectbox(
            "view",
            ["Overview"],
            label_visibility="collapsed",
        )

    with f4:
        st.markdown('<div class="control-label">&nbsp;</div>', unsafe_allow_html=True)
        if st.button("↻ Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    matches, runs, wickets, players = summary(fmt)

    st.write("")
    a, b, c, d = st.columns(4)

    with a:
        st.markdown(kpi("MATCHES", matches, "Collected matches"), unsafe_allow_html=True)
    with b:
        st.markdown(kpi("TOTAL RUNS", runs, "Batting records"), unsafe_allow_html=True)
    with c:
        st.markdown(kpi("WICKETS", wickets, "Bowling records"), unsafe_allow_html=True)
    with d:
        st.markdown(kpi("UNIQUE PLAYERS", players, "Players in dataset"), unsafe_allow_html=True)

    left, right = st.columns([1.45, 1])

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Top run scorers</div>
            <div class="card-subtitle">Highest run totals in the selected dataset</div>
        </div>
        """, unsafe_allow_html=True)

        df = top_scorers(fmt)
        if not df.empty:
            fig = go.Figure(
                go.Bar(
                    x=df["runs"],
                    y=df["player"],
                    orientation="h",
                    marker=dict(color="#19b7ad"),
                    text=df["runs"],
                    textposition="outside",
                    cliponaxis=False,
                )
            )
            fig.update_yaxes(autorange="reversed")
            chart_layout(fig, 450)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Matches by format</div>
            <div class="card-subtitle">Distribution of collected matches</div>
        </div>
        """, unsafe_allow_html=True)

        df = format_counts()
        if not df.empty:
            fig = go.Figure(
                go.Pie(
                    labels=df["format"],
                    values=df["matches"],
                    hole=.62,
                    marker=dict(
                        colors=["#19b7ad", "#1687a7", "#c88a35", "#6f7bf7"]
                    ),
                    textinfo="percent",
                )
            )
            chart_layout(fig, 450)
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div class="card">
        <div class="card-title">Recent completed matches</div>
        <div class="card-subtitle">Latest completed matches stored from Cricbuzz</div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        recent_matches(),
        use_container_width=True,
        hide_index=True,
    )


# -------------------- Live Matches --------------------
elif page == "Live Matches":
    st.title("Live Matches")
    st.caption("Current matches from the configured Cricbuzz RapidAPI endpoint.")

    if st.button("🔄 Fetch Live Matches"):
        try:
            data = parse_live_matches(get_live_matches())

            if not data:
                st.info("No live matches are currently available.")
            else:
                for match in data:
                    st.markdown(
                        f"""
                        <div class="match">
                            <div class="match-format">{match.get("format", "MATCH")}</div>
                            <div class="match-teams">
                                {match.get("team1")} &nbsp; vs &nbsp; {match.get("team2")}
                            </div>
                            <div class="match-meta">
                                {match.get("venue")} · {match.get("city")}
                            </div>
                            <div class="match-status">
                                {match.get("status") or match.get("state")}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except Exception as e:
            st.error(f"Unable to fetch live matches: {e}")


# -------------------- Player Analytics --------------------
elif page == "Player Analytics":
    st.title("Player Analytics")

    fmt = st.selectbox(
        "Format",
        ["All", "TEST", "ODI", "T20"],
        key="player_format",
    )

    df = player_leaderboard(fmt)

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown(
            '<div class="card"><div class="card-title">Player leaderboard</div>'
            '<div class="card-subtitle">Runs, best score and batting appearances</div></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

    with right:
        if not df.empty:
            fig = go.Figure(
                go.Bar(
                    x=df.head(10)["runs"],
                    y=df.head(10)["player"],
                    orientation="h",
                    marker=dict(color="#19b7ad"),
                )
            )
            fig.update_yaxes(autorange="reversed")
            chart_layout(fig, 520)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# -------------------- SQL Analytics --------------------
elif page == "SQL Analytics":
    st.title("SQL Analytics")
    st.caption("Analytics supported by the Cricbuzz API data currently collected.")

    st.info(
        "Only SQL questions that can be answered from the data currently stored "
        "from the Cricbuzz API are shown here. Unsupported questions are not "
        "included so the dashboard does not present fabricated results."
    )

    sql_questions = {
        "Q2 — Matches Played in the Last 30 Days": "sql.q2_matches_last_30_days",
        "Q3 — Top 10 ODI Run Scorers": "sql.q3_top_odi_scorers",
        "Q4 — Venues Above 50,000 Capacity": "sql.q4_venues_capacity",
        "Q5 — Total Wins by Team": "sql.q5_team_wins",
        "Q7 — Highest Score by Format": "sql.q7_highest_score_by_format",
        "Q9 — All-Rounders Above 1000 Runs and 50 Wickets": "sql.q9_all_rounders",
        "Q10 — Recent Completed Matches": "sql.q10_recent_matches",
        "Q11 — Player Format Comparison": "sql.q11_player_format_comparison",
        "Q13 — Partnerships Above 100": "sql.q13_consecutive_batsmen_partnerships",
        "Q14 — Bowler Venue Performance": "sql.q14_bowlers_venue_performance",
        "Q15 — Close Matches": "sql.q15_close_matches",
        "Q16 — Yearly Player Performance Since 2020": "sql.q16_yearly_player_performance",
        "Q18 — Economical Limited-Overs Bowlers": "sql.q18_economical_limited_overs_bowlers",
        "Q19 — Batsman Consistency": "sql.q19_batsman_consistency",
        "Q20 — Format Match Counts & Averages": "sql.q20_format_match_counts_averages",
        "Q23 — Recent Player Form": "sql.q23_recent_player_form",
        "Q24 — Partnership Rankings": "sql.q24_partnership_rankings",
    }

    selected = st.selectbox(
        "Analysis",
        list(sql_questions.keys()),
        key="sql_question_selector",
    )

    st.caption("Run the selected SQL analysis against the local SQLite database.")

    if st.button("▶ Run Analysis", key="run_sql_analysis"):
        import subprocess
        import sys

        module = sql_questions[selected]

        result = subprocess.run(
            [sys.executable, "-m", module],
            capture_output=True,
            text=True,
        )

        output = result.stdout.strip()
        errors = result.stderr.strip()

        if result.returncode == 0:
            if output:
                st.code(output, language="text")
            else:
                st.info("No output was returned.")
        else:
            st.error("This SQL script could not be executed.")
            if errors:
                st.code(errors, language="text")

# -------------------- CRUD --------------------


else:
    st.title("CRUD Operations")
    st.caption("Manage match records stored in the local SQLite database.")

    create_tab, read_tab, delete_tab = st.tabs(
        ["Create / Update", "Read", "Delete"]
    )

    with create_tab:
        mid = st.number_input("Match ID", min_value=1, step=1)
        c1, c2 = st.columns(2)

        with c1:
            team1 = st.text_input("Team 1")
            fmt = st.selectbox("Format", ["TEST", "ODI", "T20"])
            venue = st.text_input("Venue")

        with c2:
            team2 = st.text_input("Team 2")
            status = st.text_input("Status")
            city = st.text_input("City")

        description = st.text_input("Match Description")

        if st.button("Save Match"):
            if not team1 or not team2:
                st.warning("Team 1 and Team 2 are required.")
            else:
                try:
                    with engine.begin() as con:
                        con.execute(
                            text("""
                                INSERT INTO matches
                                (match_id,match_description,format,status,
                                 team1,team2,venue,city)
                                VALUES
                                (:id,:d,:f,:s,:t1,:t2,:v,:c)
                                ON CONFLICT(match_id) DO UPDATE SET
                                    match_description=excluded.match_description,
                                    format=excluded.format,
                                    status=excluded.status,
                                    team1=excluded.team1,
                                    team2=excluded.team2,
                                    venue=excluded.venue,
                                    city=excluded.city
                            """),
                            {
                                "id": mid,
                                "d": description,
                                "f": fmt,
                                "s": status,
                                "t1": team1,
                                "t2": team2,
                                "v": venue,
                                "c": city,
                            },
                        )
                    st.success("Match saved successfully.")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Unable to save match: {e}")

    with read_tab:
        if st.button("Load latest matches"):
            with engine.connect() as con:
                df = pd.read_sql(
                    text("""
                        SELECT match_id,match_description,format,
                               team1,team2,status,venue,city
                        FROM matches
                        ORDER BY CAST(start_date AS INTEGER) DESC
                        LIMIT 50
                    """),
                    con,
                )
            st.dataframe(df, use_container_width=True, hide_index=True)

    with delete_tab:
        did = st.number_input(
            "Match ID to delete",
            min_value=1,
            step=1,
            key="delete_match",
        )

        if st.button("Delete Match"):
            with engine.begin() as con:
                result = con.execute(
                    text("DELETE FROM matches WHERE match_id=:id"),
                    {"id": did},
                )

            if result.rowcount:
                st.success("Match deleted successfully.")
                st.cache_data.clear()
            else:
                st.warning("No match found with that ID.")

st.markdown("---")
st.caption(
    "Cricbuzz LiveStats  ·  Python  ·  Streamlit  ·  SQLAlchemy  ·  SQLite  ·  Cricbuzz RapidAPI"
)