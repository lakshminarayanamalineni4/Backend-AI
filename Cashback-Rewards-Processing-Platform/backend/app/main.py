from fastapi import FastAPI
from app.core.config import settings
# from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.role import router as role_router
from app.api.routes.user import router as user_router

from app.core.exceptions.handlers import register_exception_handlers

import logging

logging.getLogger("app").setLevel(logging.INFO)
if not logging.getLogger("app").handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter("%(levelname)s:     %(name)s - %(message)s")
    )
    logging.getLogger("app").addHandler(_handler)

app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
)

register_exception_handlers(app)

# app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(
    health_router,
)

app.include_router(
    role_router,
    prefix="/api/v1/roles",
    tags=["Roles"],
)

app.include_router(
    user_router,
    prefix="/api/v1/users",
    tags=["Users"],
)

@app.get("/")
def health_check():
    return {
        "message": "Cashback Rewards Platform Running",
        "environment": settings.ENVIRONMENT,
    }
    
# uv run uvicorn app.main:app --reload