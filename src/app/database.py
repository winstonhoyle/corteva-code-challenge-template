from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

## From my other project: https://github.com/winstonhoyle/TimeKeeper-QGIS-Plugin/blob/main/app/database.py

SQLALCHEMY_DATABASE_URL = 'sqlite:///./weather.db'

# For sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
