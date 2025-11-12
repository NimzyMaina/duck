# Create SQLite database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base

engine = create_engine("sqlite:///sales.db", echo=False)
Session = sessionmaker(bind=engine)