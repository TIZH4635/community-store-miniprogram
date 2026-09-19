"""社区商店微信群运营小程序 - 后端主入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="community-store-api", version="1.0.0")

# 允许微信小程序端跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 路由注册 ----------
from src.routes import publish, setting, mark, ai, monitor
app.include_router(publish.router)
app.include_router(setting.router)
app.include_router(mark.router)
app.include_router(ai.router)
app.include_router(monitor.router)


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}
