from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    parent_id = Column(Integer, nullable=True) # self-referencing for multi-level

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text)
    price = Column(Integer) # In cents
    stock = Column(Integer, default=0)
    category_id = Column(Integer)
    images = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    total_amount = Column(Integer)
    status = Column(String, default="pending") # pending, processing, shipped, delivered, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AboutUs(Base):
    __tablename__ = "about_us"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    mission = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    team_members = Column(Text, nullable=True)
    images = Column(Text, nullable=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    technologies = Column(String, nullable=True)
    images = Column(Text, nullable=True)
    project_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
