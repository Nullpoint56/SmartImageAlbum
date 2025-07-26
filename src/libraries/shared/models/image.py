import uuid
from typing import Optional

from sqlalchemy import Column, String, DateTime, func, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from shared.models.base import Base


class Image(Base):
    """Represents the core image object stored in the object store."""
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # Relationship to metadata and processing jobs
    image_metadata: Mapped["ImageMetadata"] = relationship("ImageMetadata", back_populates="image", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("ImageProcessingJob", back_populates="image", cascade="all, delete-orphan")

    embedding_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ImageMetadata(Base):
    """Descriptive metadata about the image."""
    __tablename__ = "image_metadata"
    __table_args__ = (
        UniqueConstraint("image_id"),  # enforce 1-to-1 relationship
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), unique=True)

    filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    image: Mapped["Image"] = relationship("Image", back_populates="image_metadata")