import subprocess
import sys
import os
from seed import seed_data

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("🚀 Starting Database Setup...")
    
    # 1. Create migrations if doesn't exist? 
    # For now, let's just make sure we have a versions directory
    versions_dir = os.path.join("alembic", "versions")
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
        print("Created alembic/versions directory")

    # 2. Run initial migration (optional: if they want to use alembic)
    # run_command("alembic revision --autogenerate -m 'Initial migration'")
    # run_command("alembic upgrade head")

    # 3. Seed data
    print("🌱 Seeding data...")
    seed_data()
    
    print("✅ Setup complete!")

if __name__ == "__main__":
    main()
