from fastapi import APIRouter

from app.api import health, auth, build_log

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(build_log.router)
