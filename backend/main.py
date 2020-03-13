from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, api, config, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title=config.PROJECT_NAME)


# Dependency
def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


app.include_router(api.api_router)
