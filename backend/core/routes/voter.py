import asyncio
from typing import Annotated

import requests
from fastapi import APIRouter, Cookie, Form, Request, status
from fastapi.params import Depends
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.core.operations import db
from backend.core.operations.getuser import VoterContext, get_voter_context
from ..constants import get_config
from ..models.person import PersonId, Voter

router = APIRouter(
    prefix="/voter",
    tags=["voter",],
    responses={404: {"description": "Not found"}},
)

voterContext = Annotated[VoterContext, Depends(get_voter_context)]


@router.get("/signin")
async def signup_voter() -> HTMLResponse:
    with open("C:\\Users\\7862s\\Desktop\\Election-System\\frontend\\static\\google.html") as f:
        return HTMLResponse(f.read())
    # return FileResponse()


@router.get('')
async def voter(req:Request, voter_context: voterContext):
    print(list(req.items()))
    print(voter_context.voter_id)
    return {'whoami':voter_context.voter_id}


@router.post("/postsignin")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):

    response = RedirectResponse('/voter', status_code=status.HTTP_303_SEE_OTHER,)
    response.set_cookie(key="session_id", value="your_generated_session_token")
    return response


@router.get("/i/{voter_id}")
async def get_voter(voter_id: PersonId, cookie: Annotated[str, Cookie()]) -> Voter:
    print("&"*60)
    print(cookie)
    return db.voters[voter_id]


@router.put("/i/{voter_id}/joinrequest/{pollid}")
async def join_poll(cookie:Annotated[str, Cookie(...,)]):
    ...


@router.post("/signin")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(email)
    print(password)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get('code')

    if not code:
        return {"error": "Authorization code not provided"}

    # Step 2: Exchange authorization code for access token

    token_data = get_config().google_oauth_creds
    token_response = await asyncio.to_thread(requests.post, token_data['token_uri'], data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return {"error": "Failed to retrieve access token"}

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = await asyncio.to_thread(requests.get,user_info_url, headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()

    response = JSONResponse(content={"user_info": user_info})
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response
