import asyncio
from typing import Annotated, Any

import requests
from fastapi import APIRouter, Cookie, Request, Form
from starlette.datastructures import FormData
from starlette.responses import HTMLResponse, JSONResponse

from backend.core import constants
from backend.core.models import PersonId, Voter
from backend.core.operations import db
from backend.temp import poll_id

router = APIRouter(
    prefix="/voter",
    tags=["voter",],
    responses={404: {"description": "Not found"}},
)


@router.get("/signin/")
async def signup_voter() -> HTMLResponse:
    with open("C:\\Users\\7862s\\Desktop\\Election-System\\frontend\\static\\signin.html") as f:
        return HTMLResponse(f.read())
    # return FileResponse()


@router.get("/i/{voter_id}")
async def get_voter(voter_id: PersonId, cookie: Annotated[str, Cookie()]) -> Voter:
    print("&"*60)
    print(cookie)
    return db.voters[voter_id]


@router.put("/i/{voter_id}/joinrequest/{pollid}")
async def join_poll(cookie:Annotated[str, Cookie(...,)]):
    db.get_poll(poll_id)


@router.post("/signin/")
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(email)
    print(password)


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
    token_data = constants.google_oauth_creds
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
