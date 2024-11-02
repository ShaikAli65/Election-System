from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends
from starlette.responses import JSONResponse

from core.contexts.auth import AuthContext, Authenticator, sign_in_user
from core.contexts.user import userContext

router = APIRouter(
    prefix="/voter",
    tags=["voter", ],
    responses={404: {"description": "Not found"}},
)


@router.post("/signin")
async def signin_user(auth_context: Annotated[AuthContext, Depends(sign_in_user)]) -> JSONResponse:
    reply_cookie = await auth_context.generate_cookie()
    resp = JSONResponse(reply_cookie.model_dump(), status.HTTP_202_ACCEPTED)

    if reply_cookie:
        print(reply_cookie.model_dump())
        for k,v in reply_cookie:
            resp.set_cookie(k,v)

    return resp


@router.get("/i")
async def get_voter(voter_context: userContext):
    print(voter_context)


@router.put("/i/{voter_id}/joinrequest/{pollid}")
async def join_poll(authenticator: Authenticator):
    ...

