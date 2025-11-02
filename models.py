# models.py
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Password hashed from the key
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    files = relationship("File", back_populates="owner", foreign_keys="File.owner_id")
    received_files = relationship("File", back_populates="recipient", foreign_keys="File.recipient_id")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)          # Original filename (e.g., "report.pdf")
    saved_filename = Column(String, unique=True) # Secure name on disk (e.g., "uuid.pdf")
    owner_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)  # UTC timestamp

    owner = relationship("User", back_populates="files", foreign_keys=[owner_id])
    recipient = relationship("User", back_populates="received_files", foreign_keys=[recipient_id])
