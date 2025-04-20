from fastapi import FastAPI
from app.routers import auth, notes, categories
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(notes.router, prefix="/notes")
app.include_router(categories.router, prefix="/categories")