import fastapi
import uvicorn
from fastapi import FastAPI, staticfiles
from database import admins


app = FastAPI()


@app.get("/admin/{admin_id}")
async def get_admin(admin_id):
    return admins().get(admin_id)


@app.get("/admin/{admin_id}/createPoll")
async def get_createpoll(admin_id):
    with open("C:\\Users\\7862s\\Desktop\\sem5\\CSE312 SOFTWARE MANGEMENT\\Election-System"
              "\\src\\frontend\\index.html") as f:
        file = f.read()

    return fastapi.Response(file)


@app.get("/index")
async def get_index():
    with open("C:\\Users\\7862s\\Desktop\\sem5\\CSE312 SOFTWARE MANGEMENT\\Election-System"
              "\\src\\frontend\\index.html") as f:
        file = f.read()

    return fastapi.Response(file)


@app.get("/")
async def get_hello():
    return {"hello": "hi"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="debug")
