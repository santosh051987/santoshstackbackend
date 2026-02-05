from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# About Us Schemas
class AboutUsBase(BaseModel):
    title: str
    description: str
    mission: Optional[str] = None
    vision: Optional[str] = None
    team_members: Optional[str] = None
    images: Optional[str] = None

class AboutUsCreate(AboutUsBase):
    pass

class AboutUs(AboutUsBase):
    id: int

    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: str
    technologies: Optional[str] = None
    images: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: bool = False

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Contact Submission Schemas
class ContactSubmissionBase(BaseModel):
    name: str
    email: str
    message: str

class ContactSubmissionCreate(ContactSubmissionBase):
    pass

class ContactSubmission(ContactSubmissionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
