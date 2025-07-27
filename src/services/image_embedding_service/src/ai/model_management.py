import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class CLIPEmbeddingService:
    """Encapsulates CLIP model and processor for image embeddings."""

    def __init__(self, model_id: str = "openai/clip-vit-base-patch32"):
        self.model_id = model_id
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model: CLIPModel | None = None
        self.processor: CLIPProcessor | None = None

    async def load_model(self):
        self.model = CLIPModel.from_pretrained(self.model_id).to(self.device).eval()
        self.processor = CLIPProcessor.from_pretrained(self.model_id)

    def encode(self, image: Image.Image) -> list[float]:
        np_image = np.asarray(image)
        with torch.inference_mode():
            inputs = self.processor(images=np_image, return_tensors="pt").to(self.device)
            outputs = self.model.get_image_features(**inputs)
            embedding = outputs[0].cpu().numpy()
            return embedding.tolist()