# Cricbuzz LiveStats — Final Documentation

## 1. Project Overview

Cricbuzz LiveStats is a Streamlit-based cricket analytics application that
collects cricket information through the Cricbuzz RapidAPI service, parses
the JSON responses, stores structured records in SQLite, and presents the
data through an interactive dashboard.

## 2. Main Modules

- Dashboard
- Live Matches
- Top Player Stats
- SQL Analytics
- CRUD Operations

The project uses `app.py` as the Streamlit application entry point.

## 3. Technology Stack

- Python
- Streamlit
- SQLite
- SQLAlchemy
- Requests
- Pandas
- Plotly
- python-dotenv
- Cricbuzz RapidAPI

## 4. Data Flow

Cricbuzz RapidAPI
→ Python API client
→ JSON parser
→ SQLAlchemy/database operations
→ SQLite database
→ SQL analytics/services
→ Streamlit pages

## 5. API Endpoints Used

The project uses the verified Cricbuzz RapidAPI endpoints developed during
implementation:

- `/matches/v1/live`
- `/matches/v1/recent`
- `/matches/v1/upcoming`
- `/mcenter/v1/{matchId}/scard`
- `/series/v1/{seriesId}/venues`
- `/venues/v1/{venueId}`

The API key is loaded from `.env` and is not hard-coded into the application.

## 6. Database

The project database is:

`database/cricbuzz.db`

Current tables:

- `matches`
- `batting`
- `bowling`
- `partnerships`
- `fall_of_wickets`
- `venues`

The SQL table definition is provided in `database/schema.sql`.

## 7. SQL Analytics

The original project specification contains 25 analytical questions.

The dashboard intentionally exposes only analyses that are supported by the
fields actually collected from the Cricbuzz API/database. This avoids
fabricating information that is not present in the source data.

Runnable/usable SQL scripts currently include:

Q2, Q3, Q4, Q5, Q7, Q9, Q10, Q11, Q13, Q14, Q15, Q16, Q18, Q19, Q20, Q23, Q24.

Some questions require fields that are not stored in the current dataset,
including player-profile roles, toss information, fielding statistics, and
reliable team-country mappings. Those questions are therefore not presented
as runnable dashboard analytics.

## 8. Security

Create a `.env` file in the project root:

RAPIDAPI_KEY=your_rapidapi_key_here

Never commit `.env` to GitHub.

## 9. Installation

From the project root:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## 10. Error Handling

API calls use request timeouts and HTTP error checking. Database operations
use transaction rollback and cleanup when errors occur.

## 11. Dataset Limitation

The dashboard represents the data collected from the Cricbuzz API during
development. It should be interpreted as analytics over the collected
dataset, not as a complete historical cricket database.

## 12. Final Demo Flow

For the recording:

1. Open Dashboard.
2. Show collected-data KPIs.
3. Open Live Matches.
4. Open Top Player Stats.
5. Open SQL Analytics and run 2–3 representative queries.
6. Open CRUD Operations.
7. Demonstrate one read/update/delete operation.
8. Return to Dashboard and conclude.
