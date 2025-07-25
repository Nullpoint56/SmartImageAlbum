import uuid

from sqlalchemy import Column, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from custom_types.enums import JobStatus, JobState
from db_models.base import Base


class ImageProcessingJob(Base):
    __tablename__ = "image_processing_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=False)
    image = relationship("Image", back_populates="jobs")

    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.CREATED)
    state = Column(Enum(JobState), nullable=True, default=JobState.NONE)
    detail = Column(Text, nullable=True)

