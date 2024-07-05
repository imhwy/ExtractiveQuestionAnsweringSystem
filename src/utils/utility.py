"""
Functions which is used for the project
"""

from typing import Optional
import uuid
import time


def create_new_id(prefix: Optional[str]='req') -> str:
    """
    Create a new unique id value
    Args:
        Any
    Returns:
        new_id: Unique id value
    """
    new_id = prefix + '-' + str(uuid.uuid4()) + str(int(time.time()))[-4:]
    return str(new_id)
