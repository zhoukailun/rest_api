from fastapi import APIRouter

from tests.import_test_data import import_mock_data

router = APIRouter()

@router.post("/import", name="Import test data")
async def import_test_data(start: int = 1, end: int = 100):
    return import_mock_data(start, end)

