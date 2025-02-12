from enum import Enum
from datetime import datetime
from typing import Optional, List
from typing_extensions import Annotated

from pydantic import AfterValidator, BaseModel


def missing_value(value: int):
    if value == -9999:
        return None
    else:
        return value


class QueryableAttributes(str, Enum):
    max_temp = 'max_temp'
    min_temp = 'min_temp'
    precipitation = 'precipitation'


class Calculations(str, Enum):
    ALL = 'all'
    AVG = 'avg'
    MAX = 'max'
    MIN = 'min'


class StationStats(BaseModel):
    query_id: str
    max_temp: Optional[int] = None
    min_temp: Optional[int] = None
    total_precipitation: Optional[int] = None


class Station(BaseModel):
    station_id: int
    station_name: str


class WeatherBase(BaseModel):
    pass

    class Config:
        from_attributes = True


class WeatherRecord(WeatherBase):
    station_id: str
    date: datetime
    max_temp: Optional[Annotated[int, AfterValidator(missing_value)]] = None
    min_temp: Optional[Annotated[int, AfterValidator(missing_value)]] = None
    precipitation: Optional[Annotated[int, AfterValidator(missing_value)]] = None
