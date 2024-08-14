from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from app.models.member import Member
from app.schema.member import MemberModel, NewMemberModel

member_router = APIRouter()

# @member_router.get('/')
# def index():
#     return 'Hello,member_router!!'

@member_router.get('/', response_model=List[MemberModel])
def list(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 회원 추가
@member_router.post('/', response_model=NewMemberModel)
def memadd(mem: NewMemberModel, db: Session = Depends(get_db)):
    mem = Member(**dict(mem))
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem

@member_router.get('/{userno}', response_model=Optional[MemberModel])
def readone_mem(userno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.userno == userno).first()
    return member

@member_router.delete('/{userno}', response_model=Optional[MemberModel])
def delete_mem(userno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.userno == userno).first()
    if member:
        db.delete(member)
        db.commit()
    return member

# 회원 수정
@member_router.put('/{userno}', response_model=Optional[MemberModel])
def update_mem(mem: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.userno == mem.userno).first()
    if member:
        for key, val in mem.dict().items():
            setattr(member, key, val)
        db.commit()
        db.refresh(member)
    return member