"""敏感词模型"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeywordCreate(BaseModel):
    word: str


class KeywordRecord(BaseModel):
    _id: Optional[str] = None
    word: str
    created_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
