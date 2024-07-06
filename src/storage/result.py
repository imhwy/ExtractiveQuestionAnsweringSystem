"""
Module for CRUD operations on the result collection.
"""

from src.storage.mongodb import CRUDDocuments

class CRUDResultCollection(CRUDDocuments):
    """
    A class to handle CRUD operations for the result collection in the MongoDB database.
    """
    def __init__(self):
        """
        This constructor initializes the CRUDDocuments base class 
        and sets the collection attribute to the result collection.
        """
        CRUDDocuments.__init__(self)
        self.collection = CRUDDocuments.connection.db.result_collection
