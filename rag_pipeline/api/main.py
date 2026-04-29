from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as rag_router
from api.auth import auth_router
from config.db import engine, Base

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(rag_router)