# 🏏 Cricbuzz LiveStats

### Real-Time Cricket Insights & SQL-Based Analytics

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cricbuzzlivestats-proj.streamlit.app/)

**Cricbuzz LiveStats** is an interactive cricket analytics dashboard built with **Python, Streamlit, SQLite, SQLAlchemy, Pandas, Plotly, and the Cricbuzz RapidAPI**.

The application collects cricket match and scorecard data through an API, stores structured data in a relational SQLite database, and provides interactive dashboards, player statistics, match information, and SQL-based analytical insights.

🔗 **Live Application:** https://cricbuzzlivestats-proj.streamlit.app/

---

## 📌 Project Overview

Cricbuzz LiveStats combines **API integration + database management + SQL analytics + interactive visualization** into a single Streamlit application.

The application is designed to answer questions such as:

- Which players are currently performing well?
- Who are the top run scorers?
- Which teams have the most wins?
- Which venues have the largest capacities?
- What are the highest individual scores by format?
- How do players perform across different formats?
- Which bowlers have performed economically?
- What are the recent batting performances?
- What insights can be extracted using SQL?

Instead of displaying raw cricket data, the application transforms it into **structured, queryable and visual cricket insights**.

---

## 🚀 Live Demo

### 👉 [Open Cricbuzz LiveStats](https://cricbuzzlivestats-proj.streamlit.app/)

The deployed application is hosted using **Streamlit Community Cloud**.

---

## ✨ Key Features

### 🏠 Interactive Dashboard

A centralized dashboard providing an overview of the available cricket data and analytics.

### 🏏 Live & Recent Matches

Fetches cricket match information through the Cricbuzz API and presents:

- Match description
- Teams
- Match format
- Venue
- City
- Match status
- Scores
- Overs
- Wickets

### 📊 Player Analytics

Analyze batting and bowling performances using structured scorecard data.

Metrics include:

- Runs
- Balls faced
- Strike rate
- Fours
- Sixes
- Wickets
- Economy
- Overs

### 📈 SQL Analytics

The project contains a collection of SQL analytical queries covering different levels of complexity.

Examples include:

- Top ODI run scorers
- Largest cricket venues
- Team wins
- Player role analysis
- Highest individual scores
- All-rounder performance
- Recent match analysis
- Player format comparison
- Partnership analysis
- Bowling performance
- Recent player form
- Player consistency
- Format-wise statistics

### 🗄️ Relational Database

Cricket data is stored in a **SQLite relational database** using SQLAlchemy.

Main database entities include:

- Matches
- Batting
- Bowling
- Partnerships
- Fall of Wickets
- Venues

### 🛠️ CRUD Operations

The application includes database operations for managing stored cricket information.

### 📊 Interactive Visualizations

Plotly is used to create interactive charts and analytical visualizations.

---

# 🏗️ System Architecture

```text
                  ┌──────────────────────┐
                  │   Cricbuzz RapidAPI  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    API Client        │
                  │      requests        │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Data Parsers       │
                  │ Match / Scorecard    │
                  │ Venue Information    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   SQLite Database    │
                  │      SQLAlchemy      │
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │   SQL    │   │ Pandas   │   │ CRUD     │
        │ Analytics│   │ Analysis │   │Operations│
        └────┬─────┘   └────┬─────┘   └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                  ┌──────────────────────┐
                  │  Streamlit Dashboard │
                  │  + Plotly Charts     │
                  └──────────────────────┘
```

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Streamlit** | Interactive web application |
| **Pandas** | Data manipulation and analysis |
| **Requests** | API communication |
| **SQLAlchemy** | Database ORM and SQL interaction |
| **SQLite** | Relational database |
| **Plotly** | Interactive visualizations |
| **python-dotenv** | Environment variable management |
| **Cricbuzz RapidAPI** | Cricket data source |

---

# 📂 Project Structure

```text
Cricbuzz_LiveStats/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── .streamlit/
│   └── config.toml
│
├── api/
│   ├── client.py
│   ├── parser.py
│   ├── scorecard.py
│   ├── scorecard_parser.py
│   ├── recent_matches.py
│   ├── recent_matches_parser.py
│   ├── upcoming_matches.py
│   ├── upcoming_matches_parser.py
│   ├── venues.py
│   └── venue_details.py
│
├── database/
│   ├── database.py
│   ├── operations.py
│   ├── recent_match_operations.py
│   ├── scorecard_operations.py
│   ├── venue_operations.py
│   ├── schema.sql
│   └── cricbuzz.db
│
├── pages/
│   ├── Live Matches
│   ├── Top Player Stats
│   ├── SQL Analytics
│   └── CRUD Operations
│
├── services/
│   └── dashboard_service.py
│
├── sql/
│   ├── q1_players_india.py
│   ├── q2_matches_last_30_days.py
│   ├── q3_top_odi_scorers.py
│   ├── q4_large_venues.py
│   ├── q5_team_wins.py
│   ├── q7_highest_score.py
│   ├── q9_all_rounders.py
│   ├── q10_recent_matches.py
│   ├── q11_player_format_comparison.py
│   ├── q12_home_away_performance.py
│   ├── q13_consecutive_batsmen_partnerships.py
│   ├── q14_bowlers_venue_performance.py
│   ├── q15_close_matches.py
│   ├── q16_yearly_player_performance.py
│   ├── q17_toss_advantage.py
│   ├── q18_economical_limited_overs_bowlers.py
│   ├── q19_batsman_consistency.py
│   ├── q20_format_match_counts_averages.py
│   ├── q21_weighted_player_ranking.py
│   ├── q22_head_to_head_team_performance.py
│   ├── q23_recent_player_form.py
│   ├── q24_partnership_rankings.py
│   └── q25_quarterly_player_evolution.py
│
└── documentation/
    ├── PROJECT_DOCUMENTATION.md
    └── API_SETUP.md
```

---

# 🔄 Data Flow

The application follows this general workflow:

```text
Cricbuzz API
     ↓
API Client
     ↓
JSON Response
     ↓
Parser
     ↓
Structured Cricket Data
     ↓
SQLite Database
     ↓
SQL Queries / Pandas
     ↓
Analytics
     ↓
Streamlit Dashboard
```

---

# 🗃️ Database Schema

The main database tables are:

### `matches`

Stores match-level information.

```text
match_id
series_id
series_name
match_description
format
start_date
state
status
team1
team2
venue
city
team1_score
team1_wickets
team1_overs
team2_score
team2_wickets
team2_overs
```

### `batting`

Stores individual batting performances.

```text
match_id
innings_id
player_id
player_name
runs
balls
fours
sixes
strike_rate
dismissal
```

### `bowling`

Stores bowling performances.

```text
match_id
innings_id
player_id
player_name
overs
maidens
runs
wickets
economy
balls
```

### `partnerships`

Stores batting partnership information.

### `fall_of_wickets`

Stores wicket-fall information.

### `venues`

Stores venue information including:

- Ground
- City
- Country
- Capacity
- Home team

---

# 📊 SQL Analytics

The project implements a series of cricket analytics queries.

Some examples:

| Query | Analysis |
|---|---|
| Q2 | Matches played in the last 30 days |
| Q3 | Top 10 ODI run scorers |
| Q4 | Venues with capacity greater than 50,000 |
| Q5 | Team wins |
| Q7 | Highest individual score by format |
| Q9 | All-rounders with significant runs and wickets |
| Q10 | Recent completed matches |
| Q11 | Player performance across formats |
| Q13 | Consecutive batsmen partnerships |
| Q14 | Bowler performance by venue |
| Q15 | Close-match player performance |
| Q16 | Yearly player performance |
| Q18 | Economical limited-overs bowlers |
| Q19 | Batsman consistency |
| Q20 | Match counts and batting averages |
| Q21 | Weighted player ranking |
| Q22 | Head-to-head team performance |
| Q23 | Recent player form |
| Q24 | Partnership rankings |
| Q25 | Quarterly player performance evolution |

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Cricbuzz_LiveStats.git
cd Cricbuzz_LiveStats
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the API key

Create a `.env` file in the project root:

```env
RAPIDAPI_KEY=your_api_key_here
```

The API key should **never be committed to GitHub**.

## 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🔐 Environment Variables

The application requires a RapidAPI key.

```env
RAPIDAPI_KEY=your_api_key_here
```

For Streamlit Community Cloud, configure the API key through the application's **Secrets** settings instead of committing `.env` to the repository.

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

### Live Application

👉 **https://cricbuzzlivestats-proj.streamlit.app/**

The deployment is connected to the GitHub repository, allowing changes pushed to the repository to be reflected in the deployed application. Streamlit Community Cloud supports deployment directly from GitHub repositories.

---

# ⚠️ API & Data Considerations

The application depends on the availability and limits of the Cricbuzz API.

If the API reaches its request quota or becomes temporarily unavailable, API-dependent functionality may not return fresh data.

The application also uses a local SQLite database for structured storage.

Because Streamlit Community Cloud runs applications in a managed environment, persistent database storage should not be treated as equivalent to a production database server. For a production-scale system, a hosted relational database such as PostgreSQL would be a better choice.

---

# 🔒 Security

Sensitive credentials are intentionally excluded from the repository.

The project uses:

```text
.env
```

for local development and Streamlit Secrets for cloud deployment.

The `.gitignore` file prevents the local environment file from being committed.

**Never expose or commit your RapidAPI key.**

---

# 🎯 Learning Objectives

This project demonstrates practical experience with:

- Python application development
- REST API integration
- JSON parsing
- Database design
- SQLite
- SQLAlchemy ORM
- SQL querying
- Pandas data analysis
- Data visualization
- Streamlit application development
- CRUD operations
- API authentication
- Cloud deployment
- Git/GitHub workflow

---

# 🔮 Future Improvements

Possible improvements include:

- PostgreSQL/MySQL production database
- Automated scheduled data collection
- More historical cricket data
- Advanced player comparison
- Team performance dashboards
- Head-to-head visualizations
- Advanced filters
- Automated data refresh
- Player profile integration
- Predictive analytics and machine-learning models

---

# 👩‍💻 Author

**Shiwangi Rana**

B.Tech Computer Science & Engineering

Interested in:

- Artificial Intelligence & Machine Learning
- Data Science
- Python Development
- Data Analytics
- Full-Stack Development

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

### 🏏 Cricbuzz LiveStats

**Real cricket data → structured database → SQL analytics → interactive insights.**