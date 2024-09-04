from fastapi import FastAPI
from .api.main import api_router
from .config.database import engine
from .migrations import database_migrations

database_migrations.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)