import enum
import uuid

from pydantic import HttpUrl
from sqlalchemy import Column, String, Enum, Text, UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import Base


class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    error = "error"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_url = Column(String, nullable=False)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.pending)
    detail = Column(Text, nullable=True)

    @classmethod
    async def create(cls, db: AsyncSession, image_url: str) -> "Job":
        job = cls(image_url=image_url, status=JobStatus.pending)
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job

    @classmethod
    async def get(cls, db: AsyncSession, job_id: UUID) -> "Job | None":
        result = await db.execute(select(cls).where(cls.id == job_id))
        return result.scalar_one_or_none()

    async def update_status(self, db: AsyncSession, status: JobStatus, detail: str = None) -> None:
        self.status = status
        self.detail = detail
        await db.commit()
        await db.refresh(self)
