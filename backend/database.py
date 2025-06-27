from sqlalchemy import create_engine, Column, String, DateTime, Integer, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transcription_logs = relationship("TranscriptionLog", back_populates="user")
    memorization_stats = relationship("MemorizationStat", back_populates="user")

class TranscriptionLog(Base):
    __tablename__ = "transcription_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    transcription_text = Column(Text, nullable=False)
    matched_ayah = Column(String)  # Format: "surah:ayah" e.g., "2:255"
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transcription_logs")

class MemorizationStat(Base):
    __tablename__ = "memorization_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    surah = Column(Integer, nullable=False)
    ayah = Column(Integer, nullable=False)
    times_attempted = Column(Integer, default=1)
    last_attempted = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="memorization_stats")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dhikra_user:dhikra_password@localhost:5432/dhikra_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(db: Session, firebase_uid: str) -> User:
    """Get existing user or create new one"""
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        user = User(firebase_uid=firebase_uid)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user 