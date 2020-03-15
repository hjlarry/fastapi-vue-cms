from fastapi import Depends, FastAPI, HTTPException
from starlette.requests import Request

from . import crud, models, schemas, api, config, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title=config.PROJECT_NAME)


app.include_router(api.api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = database.SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
