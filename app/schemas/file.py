from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from uuid import UUID

class FileType(str, Enum):
    pptx = "pptx"
    docx = "docx"
    xlsx = "xlsx"

class FileCreated(BaseModel):
    file_name: str
    file_type: FileType
    file_size: Optional[int] = None

class FileOut(BaseModel):
    id: UUID
    file_name: str
    file_type: FileType
    uploaded_by: UUID
    file_size: Optional[int] = None
    created_on: datetime

    class Config:
        from_attributes = True