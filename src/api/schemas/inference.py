"""
This schemas is used for inference
"""
from pydantic import BaseModel
from typing import Optional


class RequestQuestionContext(BaseModel):
    """
    Represents a request payload containing a question and its context.
    """
    question: str
    context: str
