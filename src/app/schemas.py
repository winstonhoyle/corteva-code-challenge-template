from enum import Enum
from datetime import datetime
from typing import Optional, Union
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
    SUM = 'sum'


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
    station_id: int
    date: datetime
    max_temp: Optional[Annotated[int, AfterValidator(missing_value)]] = None
    min_temp: Optional[Annotated[int, AfterValidator(missing_value)]] = None
    precipitation: Optional[Annotated[int, AfterValidator(missing_value)]] = None


class WeatherRecordOutput(WeatherRecord, Station):
    pass


class WeatherStat(BaseModel):
    avg: Union[float, None]
    min: Union[int, None]
    max: Union[int, None]
    sum: Union[int, None]


class WeatherStationYearOutputStat(BaseModel):
    weather_stat: WeatherStat
    year: Union[int, None]


class WeatherStationOutputStat(WeatherStationYearOutputStat, Station):
    pass
