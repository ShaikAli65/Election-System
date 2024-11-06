import re
import uuid
from collections import defaultdict
from typing import Annotated

from fastapi import Form, HTTPException, Request
from fastapi.exceptions import ValidationException
from starlette import status

from election.core.models.poll import CandidateInPoll, Poll
from election.utils.files import generate_portfolio_path, save_porfolio
from election.core.models.poll import PollMetaData
from election.core.models.user import CandidateParsed


async def parse_poll(
        poll_meta_data: Annotated[PollMetaData, Form()],
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
    :param poll_meta_data:
    :param request:
    :return:
    """

    form_data = await request.form()

    candidates = defaultdict(lambda: CandidateParsed(election_id=str(poll_meta_data.election_id)))
    syntax_regex = r"candidates\{(?P<candidate_id>[a-f0-9-]+)\}\{(?P<item_name>\w+)\}"
    # "can_{candidate_id}{item_name}"

    for key in form_data:

        match = re.match(syntax_regex, key)
        if not match:
            continue

        candidate_id = uuid.UUID(match.group("candidate_id"))
        item_name = match.group("item_name")

        print(f"{candidate_id=} {item_name=}, {form_data.get(key)}")
        if item_name == 'portfolio':
            file_data = form_data[key]
            file_location = generate_portfolio_path(poll_meta_data.election_id, candidate_id)
            await save_porfolio(file_location, file_data.file)
            setattr(candidates[candidate_id], 'manifesto_file_path', str(file_location))
            continue

        setattr(candidates[candidate_id], item_name, form_data.get(key))

    try:
        if not any(candidates):
            raise ValidationException

        poll = Poll(
            **poll_meta_data.model_dump(),
            candidates=[CandidateInPoll(**x.model_dump()) for x in candidates.values()]
        )
        return poll
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


