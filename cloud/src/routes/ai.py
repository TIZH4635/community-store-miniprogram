"""AI 识别与敏感词路由"""

from fastapi import APIRouter, Request
from src.services.ai_service import AIService, KeywordService

router = APIRouter(prefix="/api/ai", tags=["ai"])

ai_service = AIService()


def get_db(request: Request):
    return request.app.state.db


@router.post("/analyze")
async def analyze(request: Request):
    """AI分析群消息"""
    body = await request.json()
    message_text = body.get("message_text", "")
    if not message_text:
        return {"code": 1, "msg": "消息内容为空"}

    db = get_db(request)
    kw_service = KeywordService(db)
    keywords = await kw_service.list_keywords()

    result = await ai_service.analyze_message(message_text, keywords)
    return {"code": 0, "data": result}


@router.get("/keywords")
async def list_keywords(request: Request):
    """获取敏感词库"""
    db = get_db(request)
    service = KeywordService(db)
    words = await service.list_keywords()
    return {"code": 0, "data": words}


@router.post("/keywords")
async def add_keywords(request: Request):
    """批量添加敏感词"""
    body = await request.json()
    words = body.get("words", [])
    db = get_db(request)
    service = KeywordService(db)
    new_words = await service.add_keywords(words)
    return {"code": 0, "data": {"added": new_words}}


@router.delete("/keywords/{word}")
async def delete_keyword(word: str, request: Request):
    """删除敏感词"""
    db = get_db(request)
    service = KeywordService(db)
    ok = await service.remove_keyword(word)
    return {"code": 0 if ok else 1, "data": {"deleted": ok}}
