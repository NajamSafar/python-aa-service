import uvicorn
from fastapi import FastAPI

from config.database import get_database, sqlalchemy_engine
import routers.items
from models import api_logs, items, settings

app = FastAPI(
    title="Item",
    debug=True,
    description='Sample base project',
    version="0.0.1",
    terms_of_service="http://dvara.com/terms/",
    contact={
        "name": "Dvara",
        "url": "http://dvara.com",
        "email": "contact@dvara.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.include_router(routers.items.router)

@app.on_event("startup")
async def startup():
    await get_database().connect()
    api_logs.metadata.create_all(sqlalchemy_engine)
    items.metadata.create_all(sqlalchemy_engine)
    settings.metadata.create_all(sqlalchemy_engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


