from fastapi import FastAPI

from app.api import tasks
from app.configs.db_config import config
from app.configs.logging_config import setup_logging
from app.db.schema import Base, engine

setup_logging()



Base.metadata.create_all(bind=engine)


app = FastAPI(title=config.app_name)

# Register routes
app.include_router(tasks.router, prefix="/api")
