from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewMemberModel(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str

class MemberModel(NewMemberModel):
    userno: int
    regdate: Optional[datetime]