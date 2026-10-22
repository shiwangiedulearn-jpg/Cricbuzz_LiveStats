from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///database/cricbuzz.db"

engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True)
    series_name = Column(String)
    series_id = Column(Integer)
    start_date = Column(String)
    match_description = Column(String)
    format = Column(String)
    state = Column(String)
    status = Column(String)

    team1 = Column(String)
    team2 = Column(String)

    venue = Column(String)
    city = Column(String)

    team1_score = Column(Integer, nullable=True)
    team1_wickets = Column(Integer, nullable=True)
    team1_overs = Column(Float, nullable=True)

    team2_score = Column(Integer, nullable=True)
    team2_wickets = Column(Integer, nullable=True)
    team2_overs = Column(Float, nullable=True)

class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True)
    ground = Column(String)
    city = Column(String)
    country = Column(String)
    capacity = Column(Integer)
    home_team = Column(String)
    
class Batting(Base):
    __tablename__ = "batting"

    id = Column(Integer, primary_key=True, autoincrement=True)

    match_id = Column(Integer)
    innings_id = Column(Integer)

    team = Column(String)

    player_id = Column(Integer)
    player_name = Column(String)

    runs = Column(Integer)
    balls = Column(Integer)
    fours = Column(Integer)
    sixes = Column(Integer)
    strike_rate = Column(Float)

    dismissal = Column(String)


class Bowling(Base):
    __tablename__ = "bowling"

    id = Column(Integer, primary_key=True, autoincrement=True)

    match_id = Column(Integer)
    innings_id = Column(Integer)

    player_id = Column(Integer)
    player_name = Column(String)

    overs = Column(String)
    maidens = Column(Integer)
    runs = Column(Integer)
    wickets = Column(Integer)
    economy = Column(Float)
    balls = Column(Integer)


class Partnership(Base):
    __tablename__ = "partnerships"

    id = Column(Integer, primary_key=True, autoincrement=True)

    match_id = Column(Integer)
    innings_id = Column(Integer)

    batsman1_id = Column(Integer)
    batsman1_name = Column(String)
    batsman1_runs = Column(Integer)
    batsman1_balls = Column(Integer)

    batsman2_id = Column(Integer)
    batsman2_name = Column(String)
    batsman2_runs = Column(Integer)
    batsman2_balls = Column(Integer)

    total_runs = Column(Integer)
    total_balls = Column(Integer)


class FallOfWicket(Base):
    __tablename__ = "fall_of_wickets"

    id = Column(Integer, primary_key=True, autoincrement=True)

    match_id = Column(Integer)
    innings_id = Column(Integer)

    player_id = Column(Integer)
    player_name = Column(String)

    over = Column(Float)
    team_runs = Column(Integer)
    ball = Column(Integer)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)