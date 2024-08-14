from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import config

engine = create_engine(config.sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db_startup():
    pass
