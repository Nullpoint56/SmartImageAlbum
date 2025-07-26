import uuid

from sqlalchemy import Column, DateTime, Enum, func, ForeignKey, UUID, Integer, Boolean, String
from sqlalchemy.orm import relationship

from shared.custom_types.enums import JobStatus, JobStepName
from shared.models.base import Base


class ImageProcessingJob(Base):
    __tablename__ = "image_processing_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=False)
    image = relationship("Image", back_populates="jobs")

    steps = relationship("JobStep", back_populates="job", cascade="all, delete-orphan")

    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.CREATED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def current_step(self) -> str | None:
        pending = sorted(
            [s for s in self.steps if not s.done],
            key=lambda s: s.step_index
        )
        return pending[0].step_name if pending else None

    @property
    def is_completed(self) -> bool:
        return all(s.done for s in self.steps)


class JobStep(Base):
    __tablename__ = "job_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("image_processing_jobs.id"), nullable=False)
    job = relationship("ImageProcessingJob", back_populates="steps")

    step_name = Column(Enum(JobStepName), nullable=False)
    step_index = Column(Integer, nullable=False)

    done = Column(Boolean, nullable=False, default=False)
    error = Column(String, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
