from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.job import Job, JobCreate, JobUpdate
from app.services.job import create_job, get_job, get_jobs, update_job, delete_job
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.post("/", response_model=Job)
def create_new_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return create_job(job, current_user.id, db)

@router.get("/", response_model=List[Job])
def read_jobs(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_jobs(current_user.id, db)

@router.get("/{job_id}", response_model=Job)
def read_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    db_job = get_job(job_id, db)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job

@router.put("/{job_id}", response_model=Job)
def update_existing_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    db_job = get_job(job_id, db)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return update_job(job_id, job, db)

@router.delete("/{job_id}")
def delete_existing_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    db_job = get_job(job_id, db)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    delete_job(job_id, db)
    return {"detail": "Job deleted"}
