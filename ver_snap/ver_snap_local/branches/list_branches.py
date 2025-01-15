from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import Branch

def list_branches():
    # Load environment variables if needed
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..','..','config', '.env'))
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

    # Create a Session
    session = Session()

    try:
        # Query all branches
        branches = session.query(Branch).all()

        # List all branches
        for branch in branches:
            if branch.is_main:
                print(f"{branch.name} (main)")
            else:
                print(branch.name)
    finally:
        # Close the session
        session.close()

# Example usage
if __name__ == "__main__":
    list_branches()