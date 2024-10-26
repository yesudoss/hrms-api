from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    description: str

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class Job(JobBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Updated from 'orm_mode' to 'from_attributes'
