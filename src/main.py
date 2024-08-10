from fastapi import FastAPI
from .database import Base, engine
from .api import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media App", description="Engine behind Social Media App")

app.include_router(router)
