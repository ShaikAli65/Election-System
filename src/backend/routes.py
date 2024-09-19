# from main import app
from database import admins


@app.get("/admin{admin_id}")
async def get_admin(admin_id):
    return admins().get(admin_id)
