from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from election.core import constants
from election.core.contexts.admin import admin_init
from election.core.routes import admin, candidate, poll, portfolio, voter
from election.db import database
from election.db.statemanager import activate_db_timed_triggers, finalize
from election.utils.makeconfig import load_db_configs, make_default_config


@asynccontextmanager
async def life_span(_: FastAPI):
    with open(constants.CONFIG_FILE_PATH) as f:
        make_default_config(f)
        f.seek(0)
        load_db_configs(f)
    await database.initialize_database()
    admin_init()
    await activate_db_timed_triggers()
    yield
    await finalize()

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
    return RedirectResponse("/docs")
