"""AI 识别服务 — 通义千问"""

from datetime import datetime
import os
import json
import httpx
from typing import Optional
from src.models.mark import MarkCreate


class AIService:
    def __init__(self):
        self.api_key = os.environ.get("DASHSCOPE_API_KEY", "")
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = "qwen-plus"

    async def analyze_message(
        self, message_text: str, keywords: list[str]
    ) -> dict:
        """分析群消息，返回判定结果"""
        prompt = self._build_prompt(message_text, keywords)
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是社区商店微信群监管助手。分析群消息是否属于无关信息、不当言论、言语冲突或广告。返回JSON格式。",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                    },
                )
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as err:
            print(f"AI analyze error: {err}")
            return {"is_abnormal": False, "reason": "分析失败", "category": "其他", "suggested_keywords": []}

    def _build_prompt(self, message_text: str, keywords: list[str]) -> str:
        kw_str = "、".join(keywords) if keywords else "无"
        return f"""分析以下群消息：
消息内容："{message_text}"
当前敏感词库：{kw_str}

请判断：
1. 是否异常（无关信息/不当言论/言语冲突/广告）
2. 异常原因
3. 异常类别（无关信息/不当言论/言语冲突/广告）
4. 建议新增的敏感词（若无则返回空列表）

返回JSON格式：{{"is_abnormal": true/false, "reason": "原因", "category": "类别", "suggested_keywords": ["词1", "词2"]}}"""


class KeywordService:
    def __init__(self, db):
        self.db = db

    async def list_keywords(self) -> list[str]:
        docs = await self.db["keywords"].find({}).sort("created_at", -1).to_list(length=100)
        return [d["word"] for d in docs]

    async def add_keywords(self, words: list[str]) -> list[str]:
        existing = await self.list_keywords()
        new_words = [w for w in words if w not in existing]
        if new_words:
            docs = [{"word": w, "created_at": datetime.utcnow()} for w in new_words]
            await self.db["keywords"].insert_many(docs)
        return new_words

    async def remove_keyword(self, word: str) -> bool:
        result = await self.db["keywords"].delete_one({"word": word})
        return result.deleted_count > 0
