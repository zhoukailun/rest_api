from fastapi import APIRouter

from app.api.routers import default, assets

router = APIRouter()


router.include_router(default.router, tags=["Default"])
router.include_router(assets.router,  prefix="/aoi/v1/assets", tags=["Data Center Assets API"])
