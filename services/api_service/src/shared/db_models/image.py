import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    embedding = Column(Text, nullable=True)  # Could be JSON or vector field
