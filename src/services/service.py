"""
This module provides services
"""

from src.services.inference import InferenceEngine
from src.services.model_loader import ModelLoader

class Service:
    """
    A class that provides inference and model loading services.
    """
    def __init__(self):
        self.inference = InferenceEngine()
        self.model = ModelLoader()

    async def get_inference(self):
        """
        Returns the InferenceEngine instance for performing inference operations.

        Returns:
            InferenceEngine: The instance of the InferenceEngine class.
        """
        return self.inference
    