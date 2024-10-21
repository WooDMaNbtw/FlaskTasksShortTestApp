import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

environ.Env.read_env(BASE_DIR / '.env.local')

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://admin:admin@torg-zap-db/torg_zap_database')

# create Engine instance with connected database
engine = create_engine(DATABASE_URL)

# sessions for managing database
Session = sessionmaker(bind=engine)
session = Session()

BaseModel = declarative_base()

class Task(BaseModel):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    description = Column(Text(), nullable=True)
    completed = Column(Boolean, default=False)

    def to_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

BaseModel.metadata.create_all(engine)
