from sqlalchemy import Column, DateTime, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, time

Base = declarative_base()
class Tournament(Base):
    """
    A class that represents a golf tournament in the system.

    Attributes:
        id (int): The unique identifier for the tournament (primary key).
        sportcontent_api_id (int): The unique identifier for the tournament in the SportContent API.
        sportcontent_api_tour_id (int): The unique identifier for the tour in the SportContent API.
        datagolf_id (int): The unique identifier for the tournament in the DataGolf API.
        year (int): The year of the tournament.
        tournament_name (str): The name of the tournament.
        tournament_format (str): The format of the tournament (stroke, match, etc.).
        start_date (date): The start date of the tournament.
        start_time (time): The start time of the tournament.
        time_zone (str): The time zone of the tournament.
        location_raw (str): The raw location information of the tournament.
        end_date (date): The end date of the tournament.
        course_name (str): The name of the course where the tournament is played.
        city (str): The city where the tournament is played.
        state (str): The state where the tournament is played.
        latitude (str): The latitude of the tournament.
        longitude (str): The longitude of the tournament.
        is_major (bool): Whether the tournament is a major.
    """

    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    sportcontent_api_id = Column(Integer, unique=True)
    sportcontent_api_tour_id = Column(Integer, unique=False, default=2)
    datagolf_id = Column(Integer, unique=True)
    year = Column(Integer, nullable=False)
    tournament_name = Column(String(100), nullable=False)
    tournament_format = Column(String(100), nullable=False, default="stroke")
    start_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False, default=time(7, 00))
    time_zone = Column(String(50), nullable=False, default="America/New_York")
    location_raw = Column(String(100), nullable=True)
    end_date = Column(Date, nullable=False)
    course_name = Column(String(100))
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    latitude = Column(String(10), nullable=True)
    longitude = Column(String(10), nullable=True)
    is_major = Column(Boolean, nullable=False, default=False)
    
class Golfer(Base):
    """
    Represents a golfer in the system.

    Attributes:
        id (int): The unique identifier for the golfer. (Primary Key)
        sportcontent_api_id (int): The unique identifier for the golfer in the SportContent API.
        first_name (str): The first name of the golfer.
        last_name (str): The last name of the golfer.
        photo_url (str): The URL of the photo of the golfer.
    """

    __tablename__ = 'golfer'

    id = Column(String(9), primary_key=True)
    sportcontent_api_id = Column(Integer, unique=True)
    datagolf_id = Column(Integer, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    photo_url = Column(String(512))
    

class TournamentGolfer(Base):
    """
    Represents a golfer's appearance in a tournament.

    Attributes:
        id (int): The unique identifier for the tournament golfer. Primary Key.
        tournament_id (int): The unique identifier for the tournament.
        golfer_id (int): The unique identifier for the golfer.
        year (int): The year of the tournament.
        is_active (bool): Whether the golfer is active in the tournament.
        is_alternate (bool): Whether the golfer is an alternate in the tournament.
        is_injured (bool): Whether the golfer is injured in the tournament.
        timestamp (datetime): The timestamp when this record was most recently updated.
        is_most_recent (bool): Whether this record is the most recent record for the golfer in the entry list.
    """

    __tablename__ = 'tournament_golfer'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(
        Integer, ForeignKey("tournament.id"), nullable=False
    )
    golfer_id = Column(String(9), ForeignKey("golfer.id"), nullable=False)
    year = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_alternate = Column(Boolean, nullable=False, default=False)
    is_injured = Column(Boolean, nullable=False, default=False)
    timestamp_utc = Column(DateTime, default=datetime.utcnow)
    is_most_recent = Column(Boolean, default=True, nullable=False)

    # def to_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}