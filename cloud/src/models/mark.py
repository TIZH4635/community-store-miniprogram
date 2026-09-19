"""发言标记模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MarkCreate(BaseModel):
    group_id: str
    message_text: str
    message_time: str
    reason: str
    suggest_kick: bool = False


class MarkRecord(BaseModel):
    _id: Optional[str] = None
    group_id: str
    message_text: str
    message_time: str
    marker_id: str          # 店员 openid
    reason: str             # 无关信息/不当言论/言语冲突/其他
    suggest_kick: bool
    status: str = 'pending' # pending / resolved
    created_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
