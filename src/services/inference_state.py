"""
This module is represented as a singleton object that stores the tokenizer and model state.
"""
class InferenceState:
    """
    Encapsulates the tokenizer and model state for better management.
    """

    def __init__(self):
        self.tokenizer = None
        self.model = None
