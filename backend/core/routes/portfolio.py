from typing import Annotated

from fastapi import APIRouter, Query
from starlette.responses import FileResponse

from backend.utils.files import get_porfolio_path
from ..models.poll import PollId

router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio",],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_portfolio(
        poll_id: Annotated[PollId, Query(alias='pollId')],
        candidate_id: Annotated[PollId, Query(alias='candidateId')]
):
    print("get PortFolioId", poll_id, candidate_id)
    file_path = get_porfolio_path(poll_id, candidate_id)
    return FileResponse(file_path, media_type='application/pdf', filename=f"{candidate_id}.pdf")
