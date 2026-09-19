"""推送时间设置路由"""

from fastapi import APIRouter, Request
from src.models.setting import SettingsCreate
from src.services.setting_service import SettingService

router = APIRouter(prefix="/api/settings", tags=["settings"])


def get_db(request: Request):
    return request.app.state.db


@router.get("/{key}")
async def get_setting(key: str, request: Request):
    """获取设置"""
    db = get_db(request)
    service = SettingService(db)
    setting = await service.get(key)
    if setting:
        return {"code": 0, "data": setting.dict()}
    return {"code": 0, "data": None}


@router.put("/{key}")
async def set_setting(key: str, request: Request):
    """更新设置"""
    body = await request.json()
    db = get_db(request)
    service = SettingService(db)
    setting = await service.set(key, body.get("value", []))
    return {"code": 0, "data": setting.dict()}
