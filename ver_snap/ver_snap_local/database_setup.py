from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Create the database connection string
DATABASE_URL = os.getenv("DATABASE_URL") 

# Create the engine
engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected")
except Exception as e:
    print(f"Connection failed: {e}")

# Create a base class for models to inherit from
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Get a new database session.

    This function is a generator that provides a new database session
    using SQLAlchemy's SessionLocal. It ensures that the session is
    properly closed after use.

    Yields:
        Session: A new SQLAlchemy database session.

    Raises:
        SQLAlchemyError: If there is an issue creating the session.
    """
    """Get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
