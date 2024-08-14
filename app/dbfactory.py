from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import sungjuk, member
from app.settings import config

engine = create_engine(config.sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def db_startup():
    sungjuk.Base.metadata.create_all(engine)
    member.Base.metadata.create_all(engine)

async def db_shutdown():
    pass
