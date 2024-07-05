"""
This module provides services
"""

from src.services.inference import InferenceEngine
from src.services.model_loader import ModelLoader
from src.repositories.result import ResultRepository

class Service:
    """
    A class that provides inference and model loading services.
    """
    def __init__(self):
        self.inference = InferenceEngine()
        self.model = ModelLoader()
        self.result_collection = ResultRepository()

    async def get_inference(self):
        """
        Returns the InferenceEngine instance for performing inference operations.

        Returns:
            InferenceEngine: The instance of the InferenceEngine class.
        """
        return self.inference

    async def get_result_collection(self):
        """
        Return the result collection instance.

        Returns:
            ResultRepository: The instance of the ResultRepository class.
        """
        return self.result_collection
