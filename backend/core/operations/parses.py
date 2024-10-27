import fastapi
import pydantic
from fastapi import Form, HTTPException, Request
from fastapi.exceptions import ValidationException

from backend.core.files import generate_portfolio_path, save_porfolio
from backend.core.models import CandidateInPoll, Poll, PortFolio
from backend.core.utils.useables import get_unique_id


async def parse_poll(
        request: Request,
):
    """
    {
        title:
        type:
        startDate:
        endDate:
        candidateId : File()
        .
        .
        .
    }
    :param request:
    :return:
    """
    poll_id = get_unique_id(str)
    form_data = await request.form()
    title = form_data.get("title")
    poll_type = form_data.get("type")
    start_date = form_data.get("startDate")
    end_date = form_data.get("endDate")
    candidates_portfolios = {}
    saved_files = []
    for key in form_data:
        if key.startswith("can_"):
            candidate_id = key[4:]
            file = form_data[key]
            file_location = generate_portfolio_path(poll_id, candidate_id)
            await save_porfolio(file_location, file)
            saved_files.append(file_location)
            candidates_portfolios[candidate_id] = file_location
    try:
        poll = Poll(
            poll_id=poll_id,
            title=title,
            type=poll_type,
            start_date=start_date,
            end_date=end_date,
            candidates=[
                CandidateInPoll(
                    candidate_id=c_id,
                    portfolio=PortFolio(
                        portfolio_path=portfolio_path,
                        poll_id=poll_id,
                        candidate_id=c_id,
                    )
                )
                for c_id, portfolio_path in candidates_portfolios.items()
            ]
        )
    except pydantic.ValidationError as ve:
        raise HTTPException(fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,f"parsing failed :{ve}")
    return poll
