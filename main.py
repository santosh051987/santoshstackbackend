from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import models, schemas, database
from database import get_db, engine

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyProfile API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# About Us Endpoints
@app.get("/api/about", response_model=schemas.AboutUs)
def get_about(db: Session = Depends(get_db)):
    about = db.query(models.AboutUs).first()
    if not about:
        # Create default entry if none exists
        about = models.AboutUs(
            title="About Us",
            description="Welcome to our profile. We specialize in building amazing digital experiences.",
            mission="To innovate and deliver quality software.",
            vision="To be a global leader in technology."
        )
        db.add(about)
        db.commit()
        db.refresh(about)
    return about

@app.put("/api/about", response_model=schemas.AboutUs)
def update_about(about_update: schemas.AboutUsCreate, db: Session = Depends(database.get_db)):
    db_about = db.query(models.AboutUs).first()
    if not db_about:
        db_about = models.AboutUs(**about_update.dict())
        db.add(db_about)
    else:
        for key, value in about_update.dict().items():
            setattr(db_about, key, value)
    db.commit()
    db.refresh(db_about)
    return db_about

# Project Endpoints
@app.get("/api/projects", response_model=List[schemas.Project])
def get_projects(db: Session = Depends(database.get_db)):
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(database.get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/api/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.put("/api/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project_update: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project_update.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}

# Contact Endpoints
@app.post("/api/contact", response_model=schemas.ContactSubmission)
def submit_contact(submission: schemas.ContactSubmissionCreate, db: Session = Depends(database.get_db)):
    db_submission = models.ContactSubmission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@app.get("/api/contact", response_model=List[schemas.ContactSubmission])
def get_contacts(db: Session = Depends(database.get_db)):
    return db.query(models.ContactSubmission).order_by(models.ContactSubmission.created_at.desc()).all()
