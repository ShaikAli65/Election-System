from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse

from core.constants import get_config, get_dbconfig
from db.database import initialize_database
from utils.makeconfig import load_db_configs, make_default_config
from core import constants
from core.routes import admin, candidate, poll, portfolio, voter


@asynccontextmanager
async def life_span(_: FastAPI):
    with open(constants.CONFIG_FILE_PATH) as f:
        make_default_config(f)
        f.seek(0)
        load_db_configs(f)
    # print(get_dbconfig())
    # print(get_config())
    await initialize_database()
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
    # return RedirectResponse("/voter/signin")
    return JSONResponse({'hello':1})
