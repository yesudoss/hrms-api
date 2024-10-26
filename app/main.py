from fastapi import FastAPI
from app.routers import auth, job
from app.database import Base, engine

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include authentication routes
app.include_router(auth.router)
app.include_router(job.router)

# uvicorn app.main:app --reload
