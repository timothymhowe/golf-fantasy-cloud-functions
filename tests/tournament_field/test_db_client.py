"""
Tests for database client functionality
"""

import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.tournament_field.db_client import get_upcoming_tournament, update_tournament_entries
from src.models import Tournament, TournamentGolfer, Golfer, Base

# Test data
MOCK_FIELD_DATA = {
    "results": {
        "tournament": {
            "id": 659,
            "type": "Stroke Play",
            "name": "Charles Schwab Challenge",
        },
        "entry_list": [
            {
                "player_id": 100240,
                "first_name": "Tyson",
                "last_name": "Alexander",
                "country": "USA"
            },
            {
                "player_id": 103138,
                "first_name": "Erik",
                "last_name": "Barnes",
                "country": "USA"
            }
        ]
    }
}

@pytest.fixture
def db_session():
    """Create test database and session"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    session = Session(engine)
    
    # Add test data
    tournament = Tournament(
        id=1,
        tournament_name="Charles Schwab Challenge",
        start_date=datetime.now().date(),
        sportcontent_api_id=659
    )
    
    golfers = [
        Golfer(
            id="G100240",
            first_name="Tyson",
            last_name="Alexander",
            full_name="Tyson Alexander",
            sportcontent_api_id=100240
        ),
        Golfer(
            id="G103138",
            first_name="Erik",
            last_name="Barnes",
            full_name="Erik Barnes",
            sportcontent_api_id=103138
        )
    ]
    
    session.add(tournament)
    session.add_all(golfers)
    session.commit()
    
    yield session
    
    Base.metadata.drop_all(engine)

def test_get_upcoming_tournament_success(db_session):
    """Test successful retrieval of upcoming tournament"""
    # Use tomorrow's date to ensure it's upcoming
    tomorrow = datetime.now().date() + timedelta(days=1)
    
    tournament = db_session.query(Tournament).first()
    tournament.start_date = tomorrow
    db_session.commit()
    
    result = get_upcoming_tournament(db_session)
    
    assert result is not None
    assert result["id"] == 1
    assert result["sportcontent_api_id"] == 659
    assert result["tournament_name"] == "Charles Schwab Challenge"

def test_get_upcoming_tournament_none(db_session):
    """Test when no upcoming tournament exists"""
    # Update tournament to be in the past
    tournament = db_session.query(Tournament).first()
    tournament.start_date = datetime(2020, 1, 1).date()
    db_session.commit()
    
    result = get_upcoming_tournament(db_session)
    assert result is None

def test_update_tournament_entries_success(db_session):
    """Test successful update of tournament entries"""
    result = update_tournament_entries(db_session, 1, MOCK_FIELD_DATA)
    
    assert result is True
    
    # Verify entries were created
    entries = db_session.query(TournamentGolfer).all()
    assert len(entries) == 2
    
    # Verify entry details
    entry = entries[0]
    assert entry.tournament_id == 1
    assert entry.is_most_recent is True
    assert entry.is_active is True
    assert str(datetime.now().year) == str(entry.year)

def test_update_tournament_entries_existing_entries(db_session):
    """Test updating entries when previous entries exist"""
    # Create an existing entry
    old_entry = TournamentGolfer(
        tournament_id=1,
        golfer_id=1,
        year=str(datetime.now().year),
        is_most_recent=True,
        is_active=True
    )
    db_session.add(old_entry)
    db_session.commit()
    
    result = update_tournament_entries(db_session, 1, MOCK_FIELD_DATA)
    
    assert result is True
    
    # Verify old entry was updated
    old_entry = db_session.query(TournamentGolfer).filter_by(
        tournament_id=1,
        golfer_id=1,
        year=str(datetime.now().year)
    ).first()
    assert old_entry.is_most_recent is False

def test_update_tournament_entries_unknown_golfer(db_session):
    """Test handling of unknown golfer IDs"""
    bad_data = {
        "results": {
            "entry_list": [
                {
                    "player_id": "999999",
                    "first_name": "Unknown",
                    "last_name": "Player"
                }
            ]
        }
    }
    
    result = update_tournament_entries(db_session, 1, bad_data)
    
    assert result is True
    entries = db_session.query(TournamentGolfer).all()
    assert len(entries) == 0

def test_update_tournament_entries_error(db_session):
    """Test error handling during update"""
    # Mock session to raise an error
    db_session.commit = Mock(side_effect=Exception("Database error"))
    
    result = update_tournament_entries(db_session, 1, MOCK_FIELD_DATA)
    
    assert result is None