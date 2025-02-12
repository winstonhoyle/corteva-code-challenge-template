import collections
from datetime import datetime
import logging
import os
from typing import Optional

from fastapi import Depends, FastAPI, UploadFile
from fastapi_pagination import add_pagination, paginate
import pandas as pd
from sqlalchemy.orm import Session

from . import schemas, models, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
add_pagination(app)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s : %(message)s',
    datefmt='%m/%d/%y %I:%M:%S %p',
    handlers=[logging.StreamHandler(), logging.FileHandler('log.log', 'a'),],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event('startup')
def bulk_upload():

    logger.info('Initializing Database')
    with SessionLocal() as db:

        # Get all text files
        txt_files = os.listdir('wx_data')
        dfs = []
        station_normalization = {}
        for i, txt_file in enumerate(txt_files):
            txt_file_path = os.path.join('wx_data', txt_file)
            df = pd.read_csv(
                txt_file_path,
                sep='\t',
                names=['date', 'max_temp', 'min_temp', 'precipitation'],
            )
            df['station_id'] = txt_file.split('.')[0]
            station_normalization[txt_file.split('.')[0]] = i
            dfs.append(df)

        # Add stations table
        station_models = [
            models.Station(station_id=station_id, station_name=station_name)
            for station_name, station_id in station_normalization.items()
        ]
        db.add_all(station_models)
        db.commit()

        logger.debug('Created Station table')

        # Concat
        df = pd.concat(dfs, ignore_index=True)

        # Format
        df['station_id'].str.split('USC').str[1].astype(int)
        df['max_temp'] = df['max_temp'].astype(int)
        df['min_temp'] = df['min_temp'].astype(int)
        df['precipitation'] = df['precipitation'].astype(int)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df = df.replace(-9999, None)

        # Check Duplications
        duplicates = df[df.duplicated()]

        if len(duplicates) == 0:
            df = df[~df.duplicated()]

        logger.debug(f'Found {len(duplicates)} duplicates')

        chunks = range(0, len(df), 1000)
        for chunk in chunks:
            if chunk == chunks[-1]:
                chunk_range = range(chunk, len(df))
            else:
                chunk_range = range(chunk, chunk + 1000)
            db.add_all([models.Weather(**df.iloc[i].to_dict()) for i in chunk_range])
            db.flush()

        db.commit()

        logger.info(f'Database initialized, {len(df)} Records inputted into database')


@app.get('/weather', description='Get Weather data')
async def get_weather_records(
    station_id: str = None, year: int = None, db: Session = Depends(get_db),
):
    if station_id:
        weather_records = crud.get_all_weather_by_id(db=db, station_id=station_id)

    if year:
        weather_records = crud.get_all_weather_by_year(db=db, year=year)

    ## TODO
    if weather_records:
        return paginate(weather_records)
    else:
        return {'result': 'no result'}


@app.get('/weather/stats', description='Get Stats')
async def get_stats(
    calculation: Optional[schemas.Calculations] = None,
    attribute: Optional[schemas.QueryableAttributes] = None,
    station_id: str = None,
    year: int = None,
    db: Session = Depends(get_db),
):

    if station_id:
        stat_result = crud.calculate_attribute_weather_by_id(
            db=db, calculation=calculation, attribute=attribute, station_id=station_id
        )

    if year:
        stat_result = crud.calculate_attribute_weather_by_year(
            db=db, calculation=calculation, attribute=attribute, year=year,
        )

    if year and station_id:
        stat_result = crud.calculate_attribute_weather_by_year_and_id(
            db=db,
            calculation=calculation,
            attribute=attribute,
            year=year,
            station_id=station_id,
        )

    if stat_result:
        return {'func': attribute.lower(), 'calculation': calculation, 'result': stat_result}
    else:
        return {'func': attribute.lower(), 'calculation': calculation, 'result': 'no result'}


@app.post('/upload')
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):

    # Get Station ID
    station = file.filename.split('.')[0]

    records_to_insert = []

    for line in file.file:

        # Get line and split via tab
        input_record = line.decode('utf-8').split('\t')

        # Create weather record
        attributes_int = [int(attribute.strip()) for attribute in input_record[1:]]
        weather_record = schemas.WeatherRecord(
            station_id=station,
            date=datetime.strptime(input_record[0], '%Y%m%d'),
            max_temp=attributes_int[0],
            min_temp=attributes_int[1],
            precipitation=attributes_int[2],
        )
        records_to_insert.append(models.Weather(**weather_record.dict()))

    # Check Duplicates
    duplicates = [
        item for item, count in collections.Counter(records_to_insert).items() if count > 1
    ]
    if duplicates:
        print(duplicates)
    db.add_all(records_to_insert)
    db.commit()

    return {'resp': 'records loaded'}
