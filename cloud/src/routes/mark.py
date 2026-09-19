"""发言标记路由"""

from fastapi import APIRouter, Request
from src.models.mark import MarkCreate
from src.services.mark_service import MarkService

router = APIRouter(prefix="/api/marks", tags=["marks"])


def get_db(request: Request):
    return request.app.state.db


@router.post("")
async def create_mark(request: Request):
    """标记异常消息"""
    body = await request.json()
    data = MarkCreate(**body)
    marker_openid = request.headers.get("x-openid", "anonymous")
    db = get_db(request)
    service = MarkService(db)
    record = await service.create(data, marker_openid)
    return {"code": 0, "data": record.dict()}


@router.get("/pending")
async def list_pending(request: Request, limit: int = 50):
    """待处理标记（店员）"""
    db = get_db(request)
    service = MarkService(db)
    records = await service.list_pending(limit)
    return {"code": 0, "data": [r.dict() for r in records]}


@router.get("/all")
async def list_all(request: Request, limit: int = 100):
    """全部标记（管理员）"""
    db = get_db(request)
    service = MarkService(db)
    records = await service.list_all(limit)
    return {"code": 0, "data": [r.dict() for r in records]}


@router.put("/{mark_id}/resolve")
async def resolve_mark(mark_id: str, request: Request):
    """标记已处理"""
    db = get_db(request)
    service = MarkService(db)
    record = await service.resolve(mark_id)
    if record:
        return {"code": 0, "data": record.dict()}
    return {"code": 1, "msg": "记录不存在"}
