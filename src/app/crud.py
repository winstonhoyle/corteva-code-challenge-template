from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas


def get_station(db: Session, station_id: int):
    station = db.query(models.Station).filter(models.Station.station_id == station_id).first()
    if station:
        return station
    else:
        return None


def get_station_id(db: Session, station_name: str) -> int:
    station = (
        db.query(models.Station).filter(models.Station.station_name == station_name).first()
    )
    if station:
        return station.station_id
    else:
        return None


def determine_attribute(attribute: schemas.QueryableAttributes):
    if attribute == schemas.QueryableAttributes.max_temp:
        col = models.Weather.max_temp
    if attribute == schemas.QueryableAttributes.min_temp:
        col = models.Weather.min_temp
    if attribute == schemas.QueryableAttributes.precipitation:
        col = models.Weather.precipitation
    return col


def determine_func(calculation: schemas.Calculations):
    if calculation == schemas.Calculations.AVG:
        sql_func = func.avg
    if calculation == schemas.Calculations.MAX:
        sql_func = func.max
    if calculation == schemas.Calculations.MIN:
        sql_func = func.min
    return sql_func


def get_all_weather_by_id(db: Session, station_id: str) -> list:
    weather_records = (
        db.query(models.Weather).filter(models.Weather.station_id == station_id).all()
    )
    weather_record_list = [
        schemas.WeatherRecordOutput(
            station_id=weather.station.station_id,
            station_name=weather.station.station_name,
            date=weather.date,
            max_temp=weather.max_temp,
            min_temp=weather.min_temp,
            precipitation=weather.precipitation,
        )
        for weather in weather_records
    ]
    if weather_record_list != []:
        return weather_record_list
    else:
        return None


def get_all_weather_by_year(db: Session, year: int) -> list:
    dt_start = datetime(year, 1, 1)
    dt_end = dt_start.replace(year=dt_start.year + 1)
    datetime_query = and_(models.Weather.date >= dt_start, models.Weather.date < dt_end)
    weather_records = db.query(models.Weather).filter(datetime_query).all()
    weather_record_list = [
        schemas.WeatherRecordOutput(
            station_id=weather.station.station_id,
            station_name=weather.station.station_name,
            date=weather.date,
            max_temp=weather.max_temp,
            min_temp=weather.min_temp,
            precipitation=weather.precipitation,
        )
        for weather in weather_records
    ]
    if weather_record_list != []:
        return weather_record_list
    else:
        return None


def get_all_weather_by_year_and_id(db: Session, station_id: int, year: int) -> list:
    dt_start = datetime(year, 1, 1)
    dt_end = dt_start.replace(year=dt_start.year + 1)
    datetime_query = and_(models.Weather.date >= dt_start, models.Weather.date < dt_end)
    weather_records = db.query(models.Weather).filter(
        and_(datetime_query, models.Weather.station_id == station_id)
    )
    weather_record_list = [
        schemas.WeatherRecordOutput(
            station_id=weather.station.station_id,
            station_name=weather.station.station_name,
            date=weather.date,
            max_temp=weather.max_temp,
            min_temp=weather.min_temp,
            precipitation=weather.precipitation,
        )
        for weather in weather_records
    ]
    if weather_record_list != []:
        return weather_record_list
    else:
        return None


def calculate_attribute_weather_by_year(
    db: Session,
    calculation: schemas.Calculations,
    attribute: schemas.QueryableAttributes,
    year: int,
):
    col = determine_attribute(attribute=attribute)
    sql_func = determine_func(calculation=calculation)

    dt_start = datetime(year, 1, 1)
    dt_end = dt_start.replace(year=dt_start.year + 1)
    datetime_query = and_(models.Weather.date >= dt_start, models.Weather.date < dt_end)
    result = db.query(sql_func(col).filter(datetime_query)).first()
    if result[0] != None:
        return round(result[0], 2)
    else:
        return None


def calculate_attribute_weather_by_year_and_id(
    db: Session,
    calculation: schemas.Calculations,
    attribute: schemas.QueryableAttributes,
    year: int,
    station_id: str,
):
    col = determine_attribute(attribute=attribute)
    sql_func = determine_func(calculation=calculation)

    dt_start = datetime(year, 1, 1)
    dt_end = dt_start.replace(year=dt_start.year + 1)
    datetime_query = and_(models.Weather.date >= dt_start, models.Weather.date < dt_end)
    result = db.query(
        sql_func(col).filter(and_(datetime_query, models.Weather.station_id == station_id))
    ).first()
    if result[0] != None:
        return round(result[0], 2)
    else:
        return None


def calculate_attribute_weather_by_id(
    db: Session,
    calculation: schemas.Calculations,
    attribute: schemas.QueryableAttributes,
    station_id: str,
) -> int:

    col = determine_attribute(attribute=attribute)
    sql_func = determine_func(calculation=calculation)

    result = db.query(sql_func(col).filter(models.Weather.station_id == station_id)).first()
    if result[0] != None:
        return round(result[0], 2)
    else:
        return None


def calculate_all_attributes_by_year(
    db: Session, attribute: schemas.QueryableAttributes, year: int
):
    stat_max = calculate_attribute_weather_by_year(
        db=db, calculation=schemas.Calculations.MAX, attribute=attribute, year=year
    )
    stat_min = calculate_attribute_weather_by_year(
        db=db, calculation=schemas.Calculations.MIN, attribute=attribute, year=year
    )
    stat_avg = calculate_attribute_weather_by_year(
        db=db, calculation=schemas.Calculations.AVG, attribute=attribute, year=year
    )
    return schemas.WeatherStat(avg=stat_avg, min=stat_min, max=stat_max)


def calculate_all_attributes_by_year_and_id(
    db: Session, attribute: schemas.QueryableAttributes, station_id: str, year: int
):
    stat_max = calculate_attribute_weather_by_year_and_id(
        db=db,
        calculation=schemas.Calculations.MAX,
        attribute=attribute,
        station_id=station_id,
        year=year,
    )
    stat_min = calculate_attribute_weather_by_year_and_id(
        db=db,
        calculation=schemas.Calculations.MIN,
        attribute=attribute,
        station_id=station_id,
        year=year,
    )
    stat_avg = calculate_attribute_weather_by_year_and_id(
        db=db,
        calculation=schemas.Calculations.AVG,
        attribute=attribute,
        station_id=station_id,
        year=year,
    )
    return schemas.WeatherStat(avg=stat_avg, min=stat_min, max=stat_max)


def calculate_all_attributes_id(
    db: Session, attribute: schemas.QueryableAttributes, station_id: str
) -> schemas.WeatherStat:
    stat_max = calculate_attribute_weather_by_id(
        db=db, calculation=schemas.Calculations.MAX, attribute=attribute, station_id=station_id
    )
    stat_min = calculate_attribute_weather_by_id(
        db=db, calculation=schemas.Calculations.MIN, attribute=attribute, station_id=station_id
    )
    stat_avg = calculate_attribute_weather_by_id(
        db=db, calculation=schemas.Calculations.AVG, attribute=attribute, station_id=station_id
    )
    return schemas.WeatherStat(avg=stat_avg, min=stat_min, max=stat_max)
