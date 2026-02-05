from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    slug: str
    description: str
    price: int
    stock: int
    category_id: int
    images: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: int

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_name: str
    customer_email: str
    total_amount: int
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True

# Page Schemas
class PageBase(BaseModel):
    title: str
    slug: str
    content: str
    is_active: bool = True

class PageCreate(PageBase):
    pass

class Page(PageBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

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
