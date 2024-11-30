"""
SQLAlchemy models for tournament field functionality.
Simplified to include only necessary fields for the functions.
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Tournament(Base):
    """Tournament model - simplified for tournament field functionality"""
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    tournament_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    sportcontent_api_id = Column(Integer, unique=True)

class Golfer(Base):
    """Golfer model - simplified for tournament field functionality"""
    __tablename__ = 'golfer'

    id = Column(String(9), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    sportcontent_api_id = Column(Integer, unique=True)

class TournamentGolfer(Base):
    """Tournament-Golfer relationship model - simplified for tournament field functionality"""
    __tablename__ = 'tournament_golfer'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), nullable=False)
    golfer_id = Column(String(9), ForeignKey('golfer.id'), nullable=False)
    year = Column(Integer, nullable=False)
    is_most_recent = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
class TournamentGolferResult(Base):
    __tablename__ = "tournament_golfer_results"
    
    id = Column(Integer, primary_key=True)
    tournament_golfer_id = Column(Integer, ForeignKey("tournament_golfers.id"))
    result = Column(String)  # Can be numeric or text (e.g., "T3")
    status = Column(String)  # active, cut, wd, dq
    score_to_par = Column(Integer)

    tournament_golfer = relationship("TournamentGolfer")