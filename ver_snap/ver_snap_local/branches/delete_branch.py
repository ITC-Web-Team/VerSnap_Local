from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import Branch
from make_main import change_main_branch
from list_branches import list_branches

# Load environment variables if needed
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.env'))
load_dotenv()

# Database URL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Define the engine (replace 'DATABASE_URL' with your actual database URL)
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def delete_branch(branch_name):
    session = Session()
    try:
        # Find the branch by name
        branch = session.query(Branch).filter_by(name=branch_name).one()
        
        # Check if the branch is the main branch
        if branch.is_main:
            print(f"{RED}This is the main branch and you can't delete it unless you make another branch the main branch.{RESET}")
            change_main = input(f"{YELLOW}Do you want to change the main branch? (y/n): {RESET}")
            if change_main.lower() == 'y':
                print(f"{YELLOW}List of branches:{RESET}")
                list_branches()
                new_main_branch_name = input(f"{YELLOW}Enter the name of the new main branch: {RESET}")
                try:
                    change_main_branch(new_main_branch_name)
                    
                    # Re-fetch the branch to check if it is still the main branch
                    branch = session.query(Branch).filter_by(name=branch_name).one()
                    if branch.is_main:
                        print(f"{RED}The branch '{branch_name}' is still the main branch. Cannot delete it.{RESET}")
                        return
                    
                    # Confirm deletion
                    confirm_delete = input(f"{YELLOW}Are you sure you want to delete the branch '{branch_name}'? (y/n): {RESET}")
                    if confirm_delete.lower() == 'y':
                        # Delete the branch after changing the main branch
                        session.delete(branch)
                        session.commit()
                        print(f"{GREEN}Branch '{branch_name}' deleted successfully.{RESET}")
                    else:
                        print(f"{YELLOW}Branch deletion cancelled.{RESET}")
                except NoResultFound:
                    print(f"{YELLOW}Branch '{new_main_branch_name}' not found.{RESET}")
                except Exception as e:
                    session.rollback()
                    print(f"{RED}An error occurred: {e}{RESET}")
            return
        
        # Confirm deletion
        confirm_delete = input(f"{YELLOW}Are you sure you want to delete the branch '{branch_name}'? (y/n): {RESET}")
        if confirm_delete.lower() == 'y':
            # Delete the branch
            session.delete(branch)
            session.commit()
            print(f"{GREEN}Branch '{branch_name}' deleted successfully.{RESET}")
        else:
            print(f"{YELLOW}Branch deletion cancelled.{RESET}")
    except NoResultFound:
        print(f"{YELLOW}Branch '{branch_name}' not found.{RESET}")
    except Exception as e:
        session.rollback()
        print(f"{RED}An error occurred: {e}{RESET}")
    finally:
        session.close()

if __name__ == "__main__":
    branch_name = input(f"{YELLOW}Enter the name of the branch to delete: {RESET}")
    delete_branch(branch_name)
