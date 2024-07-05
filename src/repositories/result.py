"""
This repository class for managing result documents in the question answering system.
"""

from src.schemas.result import Result
from src.storage.result import CRUDResultCollection


class ResultRepository():
    """
    A repository class for managing result documents in the question answering system.
    """

    def __init__(self):
        """
        Initializes the collection attribute with a CRUDResultCollection instance 
        and loads all data into the data attribute.
        """
        self.collection = CRUDResultCollection()
        self.data = self.load_all_data()

    def load_all_data(self):
        """
        Load all documents from the collection.

        Returns:
            list: A list of documents with '_id' field as a string.
        """
        self.data = list(self.collection.find_all_doc())
        for doc in self.data:
            doc['_id'] = str(doc['_id'])
        return self.data

    async def add_new_result(self, result: Result):
        """
        Add a new result document to the collection.

        Args:
            result (Result): The result document to be added.
        """
        self.collection.insert_one_doc(result.__dict__)
