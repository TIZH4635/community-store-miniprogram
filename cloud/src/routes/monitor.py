"""实时监控路由"""

from fastapi import APIRouter, Request
from src.models.monitor import MonitorMessageCreate
from src.services.monitor_service import MonitorService

router = APIRouter(prefix="/api/monitor", tags=["monitor"])


def get_db(request: Request):
    return request.app.state.db


@router.post("")
async def add_message(request: Request):
    """添加消息（AI自动分析 + 自动标记）"""
    body = await request.json()
    data = MonitorMessageCreate(**body)
    db = get_db(request)
    service = MonitorService(db)
    msg = await service.add_message(data)
    return {"code": 0, "data": msg.dict()}


@router.get("/list")
async def list_messages(request: Request, group_id: str = "", limit: int = 50):
    """监控消息列表"""
    db = get_db(request)
    service = MonitorService(db)
    messages = await service.list_messages(group_id, limit)
    return {"code": 0, "data": [m.dict() for m in messages]}


@router.put("/{msg_id}/confirm")
async def confirm_message(msg_id: str, request: Request):
    """确认异常"""
    db = get_db(request)
    service = MonitorService(db)
    msg = await service.confirm(msg_id, request.headers.get("x-openid", "unknown"))
    if msg:
        return {"code": 0, "data": msg.dict()}
    return {"code": 1, "msg": "记录不存在"}


@router.put("/{msg_id}/reject")
async def reject_message(msg_id: str, request: Request):
    """驳回误判"""
    db = get_db(request)
    service = MonitorService(db)
    msg = await service.reject(msg_id, request.headers.get("x-openid", "unknown"))
    if msg:
        return {"code": 0, "data": msg.dict()}
    return {"code": 1, "msg": "记录不存在"}
