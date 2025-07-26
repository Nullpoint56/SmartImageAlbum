import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime, Enum, ForeignKey, func, Boolean, String, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)

from shared.custom_types.enums import JobStatus, JobStepName
from shared.models.base import Base
from shared.models.image import Image


class ImageProcessingJob(Base):
    """Tracks the full lifecycle of image processing."""
    __tablename__ = "image_processing_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)

    image: Mapped["Image"] = relationship("Image", back_populates="jobs")
    steps: Mapped[list["JobStep"]] = relationship("JobStep", back_populates="job", cascade="all, delete-orphan")

    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False, default=JobStatus.CREATED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    @property
    def current_step(self) -> Optional[str]:
        pending = sorted(
            [s for s in self.steps if not s.done],
            key=lambda s: s.step_index
        )
        return pending[0].step_name if pending else None

    @property
    def is_completed(self) -> bool:
        return all(s.done for s in self.steps)


class JobStep(Base):
    """Represents a step in the image processing pipeline."""
    __tablename__ = "job_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("image_processing_jobs.id", ondelete="CASCADE"), nullable=False)

    job: Mapped["ImageProcessingJob"] = relationship("ImageProcessingJob", back_populates="steps")

    step_name: Mapped[JobStepName] = mapped_column(Enum(JobStepName), nullable=False)
    step_index: Mapped[int] = mapped_column(Integer, nullable=False)

    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    error: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
