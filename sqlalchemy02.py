from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Date, DateTime, Integer, String, Sequence, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from sqlalchemy01 import SessionLocal

# 회원정보를 이용한 SQL CRUD
# mno, userid, passwd, name, email, regdate

# 데이터베이스 설정
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    userno = Column(Integer, Sequence('seq_member'), primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime(timezone=True), server_default=func.now())

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# pydantic 모델
class MemberModel(BaseModel):
    userno: int
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

# FastAPI 메인
app = FastAPI()

@app.get('/')
def index():
    return 'Hello, Members!!'

# 회원 조회
@app.get('/member', response_model=List[MemberModel])
def read_mem(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 회원 추가
@app.post('/member', response_model=MemberModel)
def memadd(mem: MemberModel, db: Session = Depends(get_db)):
    mem = Member(**dict(mem))
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem

# 회원 상세조회
@app.get('/member/{userno}', response_model=Optional[MemberModel])
def readone_mem(userno: int, db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.userno == userno).first()
    return members

# 회원 삭제
@app.delete('/member/{userno}', response_model=Optional[MemberModel])
def delete_mem(userno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.userno == userno).first()
    if member:
        db.delete(member)
        db.commit()
    return member

# 회원 수정
@app.put('/member/{userno}', response_model=Optional[MemberModel])
def update_mem(Mem: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.userno == Mem.userno).first()
    if member:
        for key, val in Mem.dict().items():
            setattr(member, key, val)
        db.commit()
        db.refresh(member)
    return member


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)