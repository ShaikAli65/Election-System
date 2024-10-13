from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from core.routes import admin, candidate, poll, portfolio, voter

app = FastAPI(
    title="ElectionSystem",
)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
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
    content = """
<body>
<form action="/poll/P1/upload/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    r = HTMLResponse(content=content)
    r.set_cookie('a','1',120,180,'/')
    return r
