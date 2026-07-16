from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
def dashboard():

    return {
        "products": 1248,
        "score": 91,
        "commission": 14.8,
        "ai_products": 327,
    }