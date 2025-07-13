from app.database.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, Enum, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


class FileType(enum.Enum):
    pptx = "pptx"
    docx = "docx"
    xlsx = "xlsx"

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), nullable=False)
    file_name = Column(String, nullable=False)      
    file_path = Column(String, nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    file_size = Column(Integer, nullable=True) 
    created_on = Column(TIMESTAMP(timezone=True), server_default=text("now()"))