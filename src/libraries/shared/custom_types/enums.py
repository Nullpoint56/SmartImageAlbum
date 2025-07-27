import enum


class JobStatus(str, enum.Enum):
    CREATED = "created"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"

class JobStepName(str, enum.Enum):
    EMBEDDING = "embedding"
    INDEXING = "indexing"
    COMPLETED = "completed"

class DistanceMetric(str, enum.Enum):
    COSINE = "cosine"
    EUCLID = "euclid"
    DOT = "dot"