from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from requests import Session
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# sqlalchemy
# 파이썬용 ORM 라이브러리
# sqlalchemy.org

# 데이터베이스 설정
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()

class Sungjuk(Base):
    __tablename__ = 'sungjuk'

    sjno = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    kor = Column(Integer)
    eng = Column(Integer)
    mat = Column(Integer)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal() # 데이터베이스 세션 객체  split3 cursor, close~ 부분
    try:
        yield db    # yield : 파이썬 제너레이터 객체 ex) db 라는 변수를 함수 내 뿐만 아니라 다른 곳에서도 사용하고 반환함
                    # 함수가 호출될 때 비로소 객체를 반환(넘김)
    finally:
        db.close()  # 데이터베이스 세션 닫음 (디비 연결 해제, 리소스 반환)

# pydantic 모델
class SungjukModel(BaseModel):
    sjno: int
    name: str
    kor: int
    eng: int
    mat: int

# FastAPI 메인
app = FastAPI()

@app.get('/')
def index():
    return 'Hello, SQLAchemey!!'

# 성적 조회
# Depends: 의존성 주입 - 디비 세션 제공**
# => 코드 재사용성 향상, 관리 용이성 향상
@app.get('/sj', response_model=List[SungjukModel])
def read_sj(db: Session = Depends(get_db)):
    sungjuks = db.query(Sungjuk).all()
    return sungjuks

# 성적 추가
@app.post('/sj', response_model=SungjukModel)
def sjadd(sj: SungjukModel, db: Session = Depends(get_db)):
    sj = Sungjuk(**dict(sj))    # 클라이언트가 전송한 성적데이터가
                                # pydantic으로 유효성 검사후
                                # 데이터베이스에 저장할 수 있도록
                                # sqlalchemy 객체로 변환하기 위해 **dict(sj) 사용
    # pydantic 방식 : Sungjuk(name='통통', kor=99, eng=88, mat=77)
    # sqlalchemy 방식 : Sungjuk(sj['name'], sj['kor'], sj['eng'], sj['mat'])

    db.add(sj)
    db.commit()
    db.refresh(sj)      # 시스템에 반영
    return sj


# __name__: 실행중인 모듈 이름을 의미하는 매직키워드
# 만일, 파일을 직접 실행하면 __name__의 이름은 __main__으로 자동지정
if __name__ == "__main__":   # 파일을 직접 실행하면 아래 코드를 불러와라
    import uvicorn
    uvicorn.run('sqlalchemy01:app', reload=True)