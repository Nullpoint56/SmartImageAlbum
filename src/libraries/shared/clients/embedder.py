from pydantic import BaseModel, HttpUrl, AnyUrl
import httpx
import logging
from custom_types.schemas import EmbeddingRequest, EmbeddingResponse

class EmbedderClient:
    """
    Client for communicating with the Embedding Service over HTTP.
    """

    def __init__(self, base_url: str):
        """
        Initialize the client with the base URL of the embedding service.

        Args:
            base_url (str): Base URL of the embedding service.
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """
        Send an image embedding request to the embedding service.

        Args:
            request (EmbeddingRequest): A request containing image data and parameters.

        Returns:
            EmbeddingResponse: Parsed embedding result from the service.

        Raises:
            httpx.HTTPError: If the HTTP request fails.
            ValueError: If response parsing fails.
        """
        url = f"{self.base_url}/encode"

        with httpx.Client() as client:
            try:
                response = client.post(url, json=request.model_dump(mode="json"))
                response.raise_for_status()
                return EmbeddingResponse(**response.json())
            except httpx.HTTPError as e:
                self.logger.exception(f"HTTP error while calling embedding service: {e}")
                raise
            except Exception as e:
                self.logger.exception(f"Unexpected error during embedding: {e}")
                raise ValueError("Failed to parse embedding response") from e
