"""推送时间设置模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SettingsCreate(BaseModel):
    key: str
    value: list[str]


class SettingRecord(BaseModel):
    _id: Optional[str] = None
    key: str
    value: list[str]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
