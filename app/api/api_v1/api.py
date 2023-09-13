from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
<<<<<<< Updated upstream

=======
api_router.include_router(items.router, prefix="/items", tags=["items"])
>>>>>>> Stashed changes
