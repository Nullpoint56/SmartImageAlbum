from pydantic import BaseModel, Field
from custom_types.enums import DistanceMetric

class VectorDBSettings(BaseModel):
    host: str
    port: int
    collection: str
    top_k: int = Field(default=5, ge=1, le=100, description="Default number of similar results to return")
    vector_size: int = 512
    distance_metric: DistanceMetric = DistanceMetric.COSINE