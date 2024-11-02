from typing import Annotated

from fastapi import APIRouter, Query

from core.contexts.admin import get_admin_context

router = APIRouter(
    prefix="/candidate",
    tags=["candidate",],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_candidates(page: Annotated[int, Query()] = 0, page_size: Annotated[int, Query()] = 10):
    admin_context = get_admin_context()
    await admin_context.get_candidates()
