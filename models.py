from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender = Column(String(64))  # e.g., IP or username
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Set up the database
engine = create_engine('sqlite:///messages.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
