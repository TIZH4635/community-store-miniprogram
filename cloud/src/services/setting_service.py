"""推送时间设置业务逻辑"""

from datetime import datetime
from src.models.setting import SettingRecord


class SettingService:
    def __init__(self, db):
        self.db = db

    async def get(self, key: str) -> SettingRecord | None:
        doc = await self.db["settings"].find_one({"key": key})
        if doc:
            doc["_id"] = str(doc.get("_id", ""))
            return SettingRecord(**doc)
        return None

    async def set(self, key: str, value: list[str]) -> SettingRecord:
        existing = await self.db["settings"].find_one({"key": key})
        now = datetime.utcnow()
        if existing:
            await self.db["settings"].update_one(
                {"key": key},
                {"$set": {"value": value, "updated_at": now}},
            )
            doc = await self.db["settings"].find_one({"key": key})
            doc["_id"] = str(doc.get("_id", ""))
            return SettingRecord(**doc)
        else:
            doc = {"key": key, "value": value, "created_at": now, "updated_at": now}
            result = await self.db["settings"].insert_one(doc)
            doc["_id"] = str(result.inserted_id)
            return SettingRecord(**doc)
