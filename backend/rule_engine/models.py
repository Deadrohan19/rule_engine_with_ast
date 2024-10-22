"""
Database setup
"""
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Database URL from environment variables
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

Base = declarative_base()

class Rule(Base):
    """
    To store rules
    """
    __tablename__ = "rules"

    rule_name = Column(String, index=True, primary_key=True)
    rule_str = Column(String)
    rule_json = Column(Text, nullable=False)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

