import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Branch , ActiveBranch
from datetime import datetime

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

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def create_branch(name: str, is_main: bool = False):
    # Create session
    session = SessionLocal()

    try:
        # Check if branch already exists
        existing_branch = session.query(Branch).filter_by(name=name).first()
        if existing_branch:
            print(f'{YELLOW}Branch "{name}" already exists!{RESET}')
            return
        
        # If no branches exist, the first one should be the main branch
        branch_count = session.query(Branch).count()
        if branch_count == 0:
            is_main = True
            print(f'{YELLOW}No branches exist. The branch "{name}" will be the main branch by default.{RESET}')

        # Handle the case where we want to set the branch as the main branch
        if is_main:
            main_branch = session.query(Branch).filter_by(is_main=True).first()
            if main_branch:
                # Ask the user if they want to overwrite the main branch
                user_input = input(f"A main branch already exists. Do you want to make '{name}' the main branch? (y/n): ").strip().lower()
                if user_input == 'y':
                    # Deactivate the current main branch and make the new branch the main
                    main_branch.is_main = False
                    session.commit()

                    # Create the new main branch
                    new_branch = Branch(name=name, is_main=True)
                    session.add(new_branch)
                    session.commit()
                    print(f'{GREEN}Successfully created the main branch: {name}{RESET}')
                else:
                    # Create the branch as a regular branch
                    new_branch = Branch(name=name, is_main=False)
                    session.add(new_branch)
                    session.commit()
                    print(f'{GREEN}Successfully created the branch: {name}, but not as the main branch.{RESET}')
            else:
                # If no main branch exists, create the first branch as the main
                new_branch = Branch(name=name, is_main=True)
                session.add(new_branch)
                session.commit()
                print(f'{GREEN}Successfully created the main branch: {name}{RESET}')

        else:
            # Create the branch as a regular branch
            new_branch = Branch(name=name, is_main=False)
            session.add(new_branch)
            session.commit()
            print(f'{GREEN}Successfully created the branch: {name}{RESET}')

    except Exception as e:
        print(f"{RED}Error creating branch: {e}{RESET}")
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    branch_name = input("Enter the name of the branch to create: ")
    is_main_input = input("Should this branch be the main branch? (y/n): ").strip().lower()
    is_main = is_main_input == 'y'
    create_branch(branch_name, is_main)
