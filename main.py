from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import models, schemas, database
from database import get_db, engine

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_password_hash, verify_password, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

app = FastAPI(title="MyProfile API", description="MyProfile API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Routes
@app.post("/api/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Category Routes
@app.get("/api/categories", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.post("/api/categories", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product Routes
@app.get("/api/products", response_model=List[schemas.Product])
def get_products(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.all()

@app.post("/api/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Order Routes
@app.post("/api/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/api/orders", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Order).order_by(models.Order.created_at.desc()).all()

# Page Routes
@app.get("/api/pages", response_model=List[schemas.Page])
def get_pages(db: Session = Depends(get_db)):
    return db.query(models.Page).all()

@app.get("/api/pages/{slug}", response_model=schemas.Page)
def get_page(slug: str, db: Session = Depends(get_db)):
    page = db.query(models.Page).filter(models.Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@app.put("/api/pages/{page_id}", response_model=schemas.Page)
def update_page(page_id: int, page_update: schemas.PageCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_page = db.query(models.Page).filter(models.Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    for key, value in page_update.dict().items():
        setattr(db_page, key, value)
    db.commit()
    db.refresh(db_page)
    return db_page

# Dashboard Summary
@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    product_count = db.query(models.Product).count()
    order_count = db.query(models.Order).count()
    category_count = db.query(models.Category).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0
    return {
        "products": product_count,
        "orders": order_count,
        "categories": category_count,
        "revenue": total_revenue
    }

# Existing About Us Endpoints
@app.get("/api/about", response_model=schemas.AboutUs)
def get_about(db: Session = Depends(get_db)):
    about = db.query(models.AboutUs).first()
    if not about:
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
def update_about(about_update: schemas.AboutUsCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()

@app.post("/api/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Contact Endpoints
@app.post("/api/contact", response_model=schemas.ContactSubmission)
def submit_contact(submission: schemas.ContactSubmissionCreate, db: Session = Depends(get_db)):
    db_submission = models.ContactSubmission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@app.get("/api/contact", response_model=List[schemas.ContactSubmission])
def get_contacts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.ContactSubmission).order_by(models.ContactSubmission.created_at.desc()).all()
