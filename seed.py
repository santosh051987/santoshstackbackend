from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models
from datetime import datetime

def seed_data():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Seed About Us
        if not db.query(models.AboutUs).first():
            about = models.AboutUs(
                title="Building Future with Innovation",
                description="We are a forward-thinking development studio specializing in modern web solutions and AI integration. With a focus on performance and user experience, we bridge the gap between complex technology and intuitive design.",
                mission="To empower businesses by creating scalable, high-quality digital products that define the next generation of the web.",
                vision="To be the global benchmark for creative engineering and technological excellence.",
                team_members="Antigravity Team",
                images="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=2070"
            )
            db.add(about)
            print("Added About Us data")

        # 2. Seed Projects
        if db.query(models.Project).count() == 0:
            projects = [
                models.Project(
                    title="Vanguard E-Commerce",
                    description="A high-performance e-commerce engine built with Next.js 15 and FastAPI. Features include real-time inventory tracking, AI-powered product recommendations, and a global edge-cached storefront.",
                    technologies="Next.js, FastAPI, PostgreSQL, Redis, Stripe",
                    featured=True,
                    images="https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&q=80&w=2089",
                    project_url="https://vanguard-demo.vercel.app",
                    github_url="https://github.com/example/vanguard"
                ),
                models.Project(
                    title="Nexus Analytics Dashboard",
                    description="Enterprise-grade analytics platform providing real-time data visualization and predictive insights. Designed for high volume data processing with a focus on accessibility and speed.",
                    technologies="React, Python, D3.js, AWS Lambda",
                    featured=True,
                    images="https://images.unsplash.com/photo-1551288049-bbbda536339a?auto=format&fit=crop&q=80&w=2070",
                    project_url="https://nexus-dashboard.vercel.app"
                ),
                models.Project(
                    title="Aura UI System",
                    description="A design system and component library focused on glassmorphism and modern aesthetics. Built with performance and developer experience in mind.",
                    technologies="TypeScript, Tailwind CSS, Framer Motion",
                    featured=False,
                    images="https://images.unsplash.com/photo-1613909209432-7b48865c5b52?auto=format&fit=crop&q=80&w=2070",
                    github_url="https://github.com/example/aura-ui"
                )
            ]
            db.add_all(projects)
            print(f"Added {len(projects)} projects")

        db.commit()
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
