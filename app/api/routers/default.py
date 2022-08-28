from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"result": True, "message": "Hello."}


@router.get("/health")
def health_check():
    return {"result": True, "message": "Ok."}
