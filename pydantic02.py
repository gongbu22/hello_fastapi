from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel


# 회원정보를 이용한 CRUD
# userid, passwd, name, email, regdate

# 회원 모델 정의
class User(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

# 회원 데이터 저장용 변수
user_db: List[User] = []

app = FastAPI()

@app.get('/')
def sayhello():
    return 'Hello, Users!!'

# 회원 데이터 조회
@app.get('/user', response_model=List[User])
def user_readall():
    return user_db

# 회원 데이터 추가 - post
@app.post('/useradd', response_model=List[User])
def user_create(user: User):
    user_db.append(user)
    return user

# 회원 데이터 추가 - get
@app.get('/useradd', response_model=User)
def user_create():
    user = User(userid='haha', passwd='haha123', name='하하', email='haha@naver.com', regdate='2024-05-01 12:50:30')
    user_db.append(user)
    user = User(userid='kiki', passwd='kiki123', name='키키', email='kiki@naver.com', regdate='2024-01-12 07:40:23')
    user_db.append(user)
    user = User(userid='hey', passwd='hey', name='헤이', email='hey@naver.com', regdate='2022-12-25 09:12:54')
    user_db.append(user)

    return user

# 회원 데이터 상세 조회 - userid로 조회
@app.get('/user/{userid}', response_model=User)
def userone(userid: str):
    findone = User(userid='none', passwd='none', name='none', email='none', regdate='1970-01-01T00:00:00.000Z')
    for user in user_db:
        if user.userid == userid:
            findone = user
    return findone

# 회원 데이터 삭제 - userid로 삭제
@app.delete('/user/{userid}', response_model=User)
def userrmv(userid: str):
    rmvone = User(userid='none', passwd='none', name='none', email='none', regdate='1970-01-01T00:00:00.000Z')
    for idx, user in enumerate(user_db):
        if user.userid == userid:
            rmvone = user_db.pop(idx)
    return rmvone

# 회원 데이터 수정
@app.put('/user', response_model=User)
def mbput(one: User):
    putone = User(userid='none', passwd='none', name='none', email='none', regdate='1970-01-01T00:00:00.000Z')
    for idx, user in enumerate(user_db):
        if user.userid == one.userid:
            user_db[idx] = one
            putone = one
    return putone

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('pydantic02:app', reload=True)