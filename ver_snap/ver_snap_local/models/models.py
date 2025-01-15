from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

Base = declarative_base()

class Branch(Base):
    __tablename__ = 'branches'

    MAIN_BRANCH_NAME = 'main'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-increment for primary key  
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_main = Column(Boolean, default=False)

    def save(self, session):
        if self.is_main:
            session.query(Branch).filter_by(is_main=True).update({Branch.is_main: False})
        session.add(self)
        session.commit()

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_main': self.is_main
        }
    
class ActiveBranch(Base):
    __tablename__ = 'active_branches'

    id = Column(String, primary_key=True, unique=True, nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    branch = relationship('Branch', backref='active_branches')

    def __str__(self):
        return f"Active Branch: {self.branch.name}"
    

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
Base.metadata.create_all(engine)