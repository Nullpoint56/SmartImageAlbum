import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io

from image_embedding_service.main import app

client = TestClient(app)

@pytest.fixture
def test_image_bytes() -> bytes:
    """
    Create an in-memory RGB image and return JPEG bytes.
    """
    img = Image.new("RGB", (64, 64), color=(0, 255, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_encode_valid_image(test_image_bytes):
    """
    Test that uploading a valid image returns a proper embedding.
    """
    files = {"file": ("test.jpg", test_image_bytes, "image/jpeg")}
    response = client.post("/encode", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "embedding" in data
    assert isinstance(data["embedding"], list)
    assert all(isinstance(x, float) for x in data["embedding"])
    assert 128 <= len(data["embedding"]) <= 1024  # CLIP embeddings are usually 512 or 768


def test_encode_invalid_format():
    """
    Test uploading a non-image file.
    """
    files = {"file": ("test.txt", b"not an image", "text/plain")}
    response = client.post("/encode", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid image format"


def test_encode_missing_file_field():
    """
    Test missing file upload completely.
    """
    response = client.post("/encode", files={})
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json()["detail"][0]["loc"][-1] == "file"


def test_encode_empty_file():
    """
    Test uploading an empty file.
    """
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/encode", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid image format"


def test_health_check():
    """
    Health check endpoint should return 200 OK.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
