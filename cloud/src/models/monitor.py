"""监控消息模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MonitorMessageCreate(BaseModel):
    group_id: str
    message_text: str
    sender: Optional[str] = None


class MonitorMessage(BaseModel):
    _id: Optional[str] = None
    group_id: str
    message_text: str
    sender: Optional[str] = None
    ai_category: Optional[str] = None      # AI判定类别
    ai_reason: Optional[str] = None         # AI判定原因
    ai_confidence: Optional[float] = None   # AI置信度
    is_abnormal: bool = False               # 是否异常
    status: str = "pending"                 # pending / confirmed / rejected
    marker_id: Optional[str] = None         # 确认标记的店员
    confirmed_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
