import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from core import constants
from core.routes import admin, candidate, poll, portfolio, voter


@asynccontextmanager
async def life_span(_: FastAPI):
    with open(constants.GOOGLE_OAUTH_SECRETS_PATH) as f:
        google_oauth_creds = json.load(fp=f)
        constants.google_oauth_creds = google_oauth_creds
    yield


app = FastAPI(
    title="ElectionSystem",
    lifespan=life_span,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # allow_origin_regex="*",
)


app.include_router(poll.router)
app.include_router(voter.router)
app.include_router(portfolio.router)
app.include_router(candidate.router)
app.include_router(admin.router)


@app.get("/")
async def main():
    return RedirectResponse("/voter/signin")
