import enum


class JobStatus(str, enum.Enum):
    CREATED = "created"
    PENDING = "pending"
    DONE = "done"
    ERROR = "error"

class JobState(str, enum.Enum):
    NONE = "none"
    EMBEDDING = "embedding"
    INDEXING = "indexing"
    COMPLETED = "completed"