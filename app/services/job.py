from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate

def create_job(job: JobCreate, user_id: int, db: Session):
    db_job = Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(job_id: int, db: Session):
    return db.query(Job).filter(Job.id == job_id).first()

def get_jobs(user_id: int, db: Session):
    return db.query(Job).filter(Job.owner_id == user_id).all()

def update_job(job_id: int, job: JobUpdate, db: Session):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job:
        for key, value in job.dict().items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(job_id: int, db: Session):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
    return db_job
