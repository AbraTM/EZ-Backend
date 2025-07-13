from app.database.database import Base
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

class UserType(enum.Enum):
    ops = "ops"
    client = "client"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
