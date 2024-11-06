from fastapi import APIRouter

router = APIRouter(
    prefix="/poll",
    tags=["poll",],
    responses={404: {"description": "Not found"}},
)

