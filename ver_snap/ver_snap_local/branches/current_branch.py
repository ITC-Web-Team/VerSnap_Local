from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import ActiveBranch, Branch  # Assuming models are in a file named models.py

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..','..','config', '.env'))
load_dotenv()

# Database URL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_current_active_branch_name():
    active_branch = session.query(ActiveBranch).first()
    if active_branch:
        return active_branch.branch.name
    return None

# Example usage
if __name__ == "__main__":
    current_branch_name = get_current_active_branch_name()
    if current_branch_name:
        print(f"The current active branch is: {current_branch_name}")
    else:
        print("No active branch found.")