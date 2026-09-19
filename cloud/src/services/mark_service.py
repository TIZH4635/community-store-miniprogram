"""发言标记业务逻辑"""

from datetime import datetime
from src.models.mark import MarkRecord


class MarkService:
    def __init__(self, db):
        self.db = db

    async def create(self, data: MarkCreate, marker_openid: str) -> MarkRecord:
        doc = {
            "group_id": data.group_id,
            "message_text": data.message_text,
            "message_time": data.message_time,
            "marker_id": marker_openid,
            "reason": data.reason,
            "suggest_kick": data.suggest_kick,
            "status": 'pending',
            "created_at": datetime.utcnow(),
        }
        result = await self.db["marked_messages"].insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return MarkRecord(**doc)

    async def list_pending(self, limit: int = 50) -> list[MarkRecord]:
        cursor = self.db["marked_messages"].find({"status": "pending"}).sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [MarkRecord(**self._normalize(d)) for d in docs]

    async def list_all(self, limit: int = 100) -> list[MarkRecord]:
        cursor = self.db["marked_messages"].find().sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [MarkRecord(**self._normalize(d)) for d in docs]

    async def resolve(self, mark_id: str) -> MarkRecord | None:
        await self.db["marked_messages"].update_one(
            {"_id": mark_id},
            {"$set": {"status": "resolved"}},
        )
        doc = await self.db["marked_messages"].find_one({"_id": mark_id})
        if doc:
            doc["_id"] = str(doc.get("_id", ""))
            return MarkRecord(**doc)
        return None

    @staticmethod
    def _normalize(doc: dict) -> dict:
        doc["_id"] = str(doc.get("_id", ""))
        return doc
