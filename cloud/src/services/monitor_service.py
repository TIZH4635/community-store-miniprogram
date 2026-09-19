"""实时监控服务 — AI自动分析 + 标记"""

from datetime import datetime
from src.models.monitor import MonitorMessage, MonitorMessageCreate
from src.models.mark import MarkCreate
from src.services.ai_service import AIService, KeywordService


class MonitorService:
    def __init__(self, db):
        self.db = db
        self.ai = AIService()
        self.keyword_service = KeywordService(db)

    async def add_message(self, data: MonitorMessageCreate) -> MonitorMessage:
        """添加消息 → AI自动分析 → 自动标记异常"""
        # AI分析
        keywords = await self.keyword_service.list_keywords()
        ai_result = await self.ai.analyze_message(data.message_text, keywords)

        # 创建监控记录
        doc = {
            "group_id": data.group_id,
            "message_text": data.message_text,
            "sender": data.sender,
            "ai_category": ai_result.get("category"),
            "ai_reason": ai_result.get("reason"),
            "ai_confidence": ai_result.get("confidence"),
            "is_abnormal": ai_result.get("is_abnormal", False),
            "status": "pending" if ai_result.get("is_abnormal") else "confirmed",
            "created_at": datetime.utcnow(),
        }
        result = await self.db["monitored_messages"].insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        # 自动标记异常消息
        if ai_result.get("is_abnormal"):
            mark_service = MarkService(self.db)
            await mark_service.create(
                MarkCreate(
                    group_id=data.group_id,
                    message_text=data.message_text,
                    message_time=datetime.utcnow().isoformat(),
                    reason=ai_result.get("reason", "AI判定异常"),
                    suggest_kick=False,
                ),
                marker_id="ai_auto",
            )
            # 新增敏感词
            if ai_result.get("suggested_keywords"):
                await self.keyword_service.add_keywords(ai_result["suggested_keywords"])

        return MonitorMessage(**doc)

    async def list_messages(self, group_id: str, limit: int = 50) -> list[MonitorMessage]:
        """获取监控消息列表"""
        cursor = (
            self.db["monitored_messages"]
            .find({"group_id": group_id})
            .sort("created_at", -1)
            .limit(limit)
        )
        docs = await cursor.to_list(length=limit)
        return [MonitorMessage(**self._normalize(d)) for d in docs]

    async def confirm(self, msg_id: str, marker_openid: str) -> MonitorMessage | None:
        """店员确认异常"""
        await self.db["monitored_messages"].update_one(
            {"_id": msg_id},
            {"$set": {"status": "confirmed", "marker_id": marker_openid, "confirmed_at": datetime.utcnow()}},
        )
        doc = await self.db["monitored_messages"].find_one({"_id": msg_id})
        if doc:
            doc["_id"] = str(doc.get("_id", ""))
            return MonitorMessage(**doc)
        return None

    async def reject(self, msg_id: str, marker_openid: str) -> MonitorMessage | None:
        """店员驳回误判"""
        await self.db["monitored_messages"].update_one(
            {"_id": msg_id},
            {"$set": {"status": "rejected", "marker_id": marker_openid, "confirmed_at": datetime.utcnow()}},
        )
        doc = await self.db["monitored_messages"].find_one({"_id": msg_id})
        if doc:
            doc["_id"] = str(doc.get("_id", ""))
            return MonitorMessage(**doc)
        return None

    @staticmethod
    def _normalize(doc: dict) -> dict:
        doc["_id"] = str(doc.get("_id", ""))
        return doc
