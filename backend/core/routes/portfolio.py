from fastapi import APIRouter, File
from starlette.responses import FileResponse

from backend.core.files import get_porfolio_path
from backend.core.models import PersonId, PollId, PortFolioId

router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio",],
    responses={404: {"description": "Not found"}},
)


@router.get("/{portfolio_id}")
async def get_portfolio(portfolio_id: PortFolioId):
    print("get PortFolioId", portfolio_id)


@router.get("/")
async def get_portfolio(pollid: PollId, candidate_id: PersonId):
    print("getting portfolio of", candidate_id)
    file_path = get_porfolio_path(pollid, candidate_id)
    return FileResponse(file_path, media_type='application/pdf', filename=f"{candidate_id}.pdf")
