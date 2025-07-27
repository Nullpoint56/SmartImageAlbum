from ai.model_management import CLIPEmbeddingService


class AppSingletons:
    def __init__(self, model_service: CLIPEmbeddingService):
        self.model_service = model_service