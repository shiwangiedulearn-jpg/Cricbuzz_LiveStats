# Cricbuzz LiveStats — Answerable SQL Dashboard

This version intentionally shows only SQL questions that are supported by the
Cricbuzz API data currently collected and stored in the local SQLite database.

Included:
Q2, Q3, Q4, Q5, Q7, Q9, Q10, Q11, Q13, Q14, Q15, Q16, Q18, Q19, Q20, Q23, Q24.

Questions requiring unavailable player-profile, toss, fielding, team-country,
or other missing API fields are not shown as runnable dashboard analyses.

Run:
```powershell
streamlit run app.py
```

Keep the existing api/, database/, sql/, .env and requirements.txt from the
project alongside this app.py.
