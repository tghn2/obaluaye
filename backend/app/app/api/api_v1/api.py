from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    group,
    pathway,
    theme,
    node,
    services,
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(group.router, prefix="/group", tags=["group"])
api_router.include_router(pathway.router, prefix="/pathway", tags=["pathway"])
api_router.include_router(theme.router, prefix="/theme", tags=["theme"])
api_router.include_router(node.router, prefix="/node", tags=["node"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
