from typing import Annotated

from fastapi import APIRouter, Cookie, Form, Request, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse, RedirectResponse

from core.contexts.auth import AuthContext, get_auth_context, sign_in_user
from core.contexts.voter import VoterContext, get_voter_context
from core.models.person import PersonId, UserLoggedInCookie, Voter
from db import fakedata as db

router = APIRouter(
    prefix="/voter",
    tags=["voter", ],
    responses={404: {"description": "Not found"}},
)

voterContext = Annotated[VoterContext, Depends(get_voter_context)]
Authenticator = Annotated[AuthContext, Depends(get_auth_context)]


@router.post("/signin")
async def signin_voter(reply_cookie:Annotated[UserLoggedInCookie, Depends(sign_in_user)]) -> JSONResponse:
    reply = await sign_in_user(voter_info)
    print(voter_info)
    resp = JSONResponse(voter_info, status.HTTP_202_ACCEPTED)
    if reply:
        for k,v in reply:
            resp.set_cookie(k,v)

    return resp


@router.get('')
async def voter(req: Request, voter_context: voterContext):
    print(list(req.items()))
    print(voter_context.voter_id)
    return {'whoami': voter_context.voter_id}


@router.get("/i/{voter_id}")
async def get_voter(voter_id: PersonId, cookie: Annotated[str, Cookie()]) -> Voter:
    print("&" * 60)
    print(cookie)
    return db.voters[voter_id]


@router.put("/i/{voter_id}/joinrequest/{pollid}")
async def join_poll(cookie: Annotated[str, Cookie(..., )]):
    ...


@router.post("/signin")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(email)
    print(password)

