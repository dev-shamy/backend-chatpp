"""Database models"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.base import Base


class Message(Base):
    """Message model for storing chat messages"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    room = Column(String, default="general", nullable=False, index=True)
    
    def __repr__(self):
        return f"<Message(id={self.id}, username='{self.username}', room='{self.room}')>"

