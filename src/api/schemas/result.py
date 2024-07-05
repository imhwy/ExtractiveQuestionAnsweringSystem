"""
This module defines the Result class used to represent a document in the question answering system.
"""
from pydantic import BaseModel


class Result(BaseModel):
    """
    A class to represent a result document in the question answering system.
    """
    Id: str
    model: str
    question: str
    context: str
    answer: str

    def to_dict(self):
        """
        Convert the Result object to a dictionary.

        Returns:
            dict: A dictionary representation of the Result object.
        """
        return vars(self)
