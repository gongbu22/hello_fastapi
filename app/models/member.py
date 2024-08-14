from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, DateTime, func

from app.models.base import Base


class Member(Base):
    __tablename__ = 'member'

    userno = Column(Integer, Sequence('seq_member'), primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime, default=datetime.now)