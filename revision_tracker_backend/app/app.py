from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app import models  
from app.auth import router as auth_router
from app.dependencies import get_current_user
from app.topics import router as topic_router
from app.revisions import router as revisions_router
from app.revision_queue import router as revision_queue_router
from app.syllabus import router as syllabus_router
from app.subjects import router as subjects_router
from app.units import router as units_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.include_router(auth_router)
app.include_router(topic_router)
app.include_router(revisions_router)
app.include_router(revision_queue_router)
app.include_router(syllabus_router)
app.include_router(subjects_router)
app.include_router(units_router)


@app.get("/")
async def health():
    return {"status": "ok"}

@app.get("/me")
async def read_me(user: models.User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
    }





