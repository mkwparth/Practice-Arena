from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

from app.routers import auth_router, preference_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(preference_router.router)

@app.get("/")
def home():
    return {"status": "API Running"}