from typing import Tuple

import torch
from functools import lru_cache

from transformers import CLIPModel, CLIPProcessor


@lru_cache()
def get_model_and_processor() -> Tuple[CLIPModel, CLIPProcessor, torch.device]:
    """
    Loads and caches the CLIP model and processor for image embeddings.

    Returns:
        Tuple of (CLIPModel, CLIPProcessor, device)
    """
    model_id = "openai/clip-vit-base-patch32"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = CLIPModel.from_pretrained(model_id).to(device).eval()
    processor = CLIPProcessor.from_pretrained(model_id)

    return model, processor, device
