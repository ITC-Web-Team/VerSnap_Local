from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import Branch, ActiveBranch
# Load environment variables if needed
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..','..','config', '.env'))
load_dotenv()

# Database URL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
# Define the engine
engine = create_engine(DATABASE_URL)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

def change_main_branch(new_main_branch_name):
    # Find the branch with the given name
    new_main_branch = session.query(Branch).filter_by(name=new_main_branch_name).first()
    
    if not new_main_branch:
        print(f"{RED}Branch with name '{new_main_branch_name}' does not exist.{RESET}")
        return
    
    # Check if the new main branch is already the main branch
    if new_main_branch.is_main:
        print(f"{YELLOW}'{new_main_branch_name}' is already the main branch.{RESET}")
        return
    
    # Set the current main branch to not be main
    current_main_branch = session.query(Branch).filter_by(is_main=True).first()
    if current_main_branch:
        current_main_branch.is_main = False
        session.add(current_main_branch)
    
    # Set the new main branch
    new_main_branch.is_main = True
    session.add(new_main_branch)
    
    # Print success message
    print(f"{GREEN}Successfully changed the main branch to '{new_main_branch_name}'.{RESET}")
    
    # Commit the changes to the database
    session.commit()
