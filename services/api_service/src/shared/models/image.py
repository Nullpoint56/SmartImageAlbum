import uuid

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.models.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)

    filename = Column(String, nullable=False)
    object_key = Column(String, nullable=False, unique=True)
    content_type = Column(String, nullable=False)
    embedding_id = Column(UUID(as_uuid=True), nullable=True, default=None)

    jobs = relationship(
        "ImageProcessingJob",
        back_populates="image",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
