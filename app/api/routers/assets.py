from fastapi import APIRouter

from app.models.assets import AssetsInSearch, AssetsInCreate, AssetsInUpdate, AssetPath
from app.db.operators import DBOperator

router = APIRouter()


@router.get("/{asset_type}}/search", name="Search Objects by ID")
async def search_asset_object_by_id(asset_type: AssetPath, asset_id: str = None):
    db_operator = DBOperator()
    return db_operator.search_by_id(asset_type, asset_id)


@router.post("/search", name="Search Objects by Query Body")
async def search_asset_objects(payload_search: AssetsInSearch):
    db_operator = DBOperator()
    return db_operator.search(payload_search)


@router.post("/update", name="Create Objects")
async def create_asset_objects(payload_create: AssetsInCreate):
    db_operator = DBOperator()
    return db_operator.create(payload_create.data)


@router.put("/update", name="Update Objects")
async def update_asset_objects(payload_update: AssetsInUpdate):
    db_operator = DBOperator()
    return db_operator.update(payload_update.data)

