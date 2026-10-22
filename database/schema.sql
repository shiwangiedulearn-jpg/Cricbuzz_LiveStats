-- Cricbuzz LiveStats
-- SQLite schema matching the current SQLAlchemy database models.

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    series_id INTEGER,
    series_name TEXT,
    match_description TEXT,
    format TEXT,
    start_date TEXT,
    state TEXT,
    status TEXT,
    team1 TEXT,
    team2 TEXT,
    venue TEXT,
    city TEXT,
    team1_score INTEGER,
    team1_wickets INTEGER,
    team1_overs REAL,
    team2_score INTEGER,
    team2_wickets INTEGER,
    team2_overs REAL
);

CREATE TABLE IF NOT EXISTS batting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    innings_id INTEGER,
    team TEXT,
    player_id INTEGER,
    player_name TEXT,
    runs INTEGER,
    balls INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate REAL,
    dismissal TEXT
);

CREATE TABLE IF NOT EXISTS bowling (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    innings_id INTEGER,
    player_id INTEGER,
    player_name TEXT,
    overs TEXT,
    maidens INTEGER,
    runs INTEGER,
    wickets INTEGER,
    economy REAL,
    balls INTEGER
);

CREATE TABLE IF NOT EXISTS partnerships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    innings_id INTEGER,
    batsman1_id INTEGER,
    batsman1_name TEXT,
    batsman1_runs INTEGER,
    batsman1_balls INTEGER,
    batsman2_id INTEGER,
    batsman2_name TEXT,
    batsman2_runs INTEGER,
    batsman2_balls INTEGER,
    total_runs INTEGER,
    total_balls INTEGER
);

CREATE TABLE IF NOT EXISTS fall_of_wickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    innings_id INTEGER,
    player_id INTEGER,
    player_name TEXT,
    over REAL,
    team_runs INTEGER,
    ball INTEGER
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    ground TEXT,
    city TEXT,
    country TEXT,
    capacity INTEGER,
    home_team TEXT
);

CREATE INDEX IF NOT EXISTS idx_batting_match ON batting(match_id);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_match ON bowling(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling(player_id);
CREATE INDEX IF NOT EXISTS idx_partnership_match ON partnerships(match_id);
CREATE INDEX IF NOT EXISTS idx_fow_match ON fall_of_wickets(match_id);
