from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('station.station_id'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    max_temp = Column(Integer, nullable=True)
    min_temp = Column(Integer, nullable=True)
    precipitation = Column(Integer, nullable=True)

    station = relationship('Station', foreign_keys=[station_id])


class Station(Base):
    __tablename__ = 'station'

    station_id = Column(Integer, primary_key=True)
    station_name = Column(String, unique=True, nullable=False)
