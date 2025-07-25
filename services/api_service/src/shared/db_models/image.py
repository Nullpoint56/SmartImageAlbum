import uuid

from sqlalchemy import Column, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db_models.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    content_hash = Column(String(64), nullable=False)

    jobs = relationship("ImageProcessingJob", back_populates="image", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("content_hash", name="uq_image_content_hash"),)
