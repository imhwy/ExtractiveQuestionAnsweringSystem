"""
This module is used for loading model
"""
from typing import Any
from transformers import (AutoTokenizer,
                          AutoModelForQuestionAnswering)
import torch

class ModelLoader:
    """
    A class to handle loading of question answering models.
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Loading model")

    async def path_config(self, path: str = None) -> str:
        """
        Configure the model path based on input.

        Args:
            path (str): The path to the model.

        Returns:
            str: The modified model path.
        """
        return "src/models/"+path

    async def load_tokenizer(self, path: str = None) -> AutoTokenizer:
        """
        Load a tokenizer from a specified path.

        Args:
            path (str): The path to the tokenizer model.

        Returns:
            AutoTokenizer: The loaded tokenizer object.
        """
        tokenizer = AutoTokenizer.from_pretrained(path)
        try:
            tokenizer.model_input_names.remove("token_type_ids")
        except ValueError:
            print("already removed!!!")
        return tokenizer

    async def load_model(self, path: str = None) -> AutoModelForQuestionAnswering:
        """
        Load a model from a specified path.

        Args:
            path (str): The path to the model.

        Returns:
            AutoModelForQuestionAnswering: The loaded model object.
        """
        model = AutoModelForQuestionAnswering.from_pretrained(path)
        model.to(self.device)
        return model

    async def loading_question_answering_model(self, path: str = None) -> Any:
        """
        Load both tokenizer and model for question answering.

        Args:
            path (str): The path to the model.

        Returns:
            tuple: A tuple containing the loaded tokenizer and model.
        """
        modified_path = await self.path_config(path)
        tokenizer = await self.load_tokenizer(modified_path)
        model = await self.load_model(modified_path)
        return tokenizer, model
