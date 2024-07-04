"""
This schemas is used for inference
"""
from pydantic import BaseModel


class RequestQuestionContext(BaseModel):
    """
    Represents a request payload containing a question and its context.
    """
    question: str
    context: str
