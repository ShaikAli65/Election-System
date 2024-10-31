import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import backend.utils.makeconfig
from core import constants
from core.routes import admin, candidate, poll, portfolio, voter


@asynccontextmanager
async def life_span(_: FastAPI):
    with open(constants.CONFIG_FILE_PATH) as f:
        backend.utils.makeconfig.make_default_config(f)

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
