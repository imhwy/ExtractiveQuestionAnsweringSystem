"""
mongodb function
"""
from pymongo import MongoClient

from src.services.logger import QAsystem

MONGODB_CONNECTION = "mongodb://localhost:27017/"
DB_NAME = "QAsystem"
if MONGODB_CONNECTION is None:
    MONGODB_CONNECTION = "mongodb://localhost:27017/"

LOG_LEVEL = "info"
WRITE_LOG_TO_FILE = False
log = QAsystem(
    file_name='log.txt',
    write_to_file=WRITE_LOG_TO_FILE,
    mode=LOG_LEVEL)


class MongoDBConnection():
    """
    Connect to the MongoDB, change the connection string per your MongoDB environment
    Connection String
    mongodb://username:password@host[:port]/defaultauthdb?<options>
    """
    url = MONGODB_CONNECTION
    col = DB_NAME

    def __init__(self):
        self.client = MongoClient(self.url)
        self.db = self.client[DB_NAME]
        print("DEBUG DEBUG")
        try:
            # check connection is available
            self.client.admin.command('ismaster')
            log.info("CONNECT TO DB {} SUCCESSFULLY".format(self.db))

        except ValueError as e:
            log.error("CONNECT TO DB {} FAIL, ERROR: {}".format(self.db, e))


class CRUDDocuments():
    """
    author: ngm1hc1
    """
    connection = MongoDBConnection()

    def __init__(self):
        self.collection = None

    def insert_one_doc(self, obj):
        """
        Insert a single document.
        Example:
            Input: x= {'x': 1}
                result = db.test.insert_one_doc(x)
            Output: result.inserted_id
                ObjectId('54f112defba522406c9cc208')
        Parameters:
            obj: The document to insert. Must be a mutable mapping type. 
                If the document does not have an _id field one will be added automatically.
            Returns:
                An instance of InsertOneResult.
        """
        return self.collection.insert_one(document=obj)

    def insert_many_doc(self, objs, ordered=True):
        """
        Insert an iterable of documents.
        Example:
            Input:  objs = []
            result = db.test.insert_many_doc([{'x': i} for i in range(2)])
            output:
            result.inserted_ids
            >>> [ObjectId('54f113fffba522406c9cc20e'), ObjectId('54f113fffba522406c9cc20f')]
        Parameters:
            - objs: A iterable of documents to insert.
            - ordered (optional): If True (the default) documents will be inserted on the server serially,
            in the order provided. If an error occurs all remaining inserts are aborted. 
            If False, documents will be inserted on the server in arbitrary order, 
            possibly in parallel, and all document inserts will be attempted.
            return: An instance of InsertManyResult.
        """
        return self.collection.insert_many(documents=objs, ordered=ordered)

    def replace_one_doc(self, filterObj, replaceObj, upsert=False):
        """
        Replace a single document matching the filter.
        Example:
            Input:
            {u'x': 1, u'_id': ObjectId('54f4c5befba5220aa4d6dee7')}
            result = db.test.replace_one_doc({'x': 1}, {'y': 1})
            Or
            result = db.test.replace_one_doc({'x': 1}, {'x': 1}, True)
            Output: 
            result.matched_count
            >>> result.matched_count
                1
            >>> result.modified_count
                1
        Parameters:
            - filterObj: A query that matches the document to replace.
            - replaceObj: The new document.
            - upsert (optional): If True, perform an insert if no documents match the filter.
        return:
            An instance of UpdateResult.
        """
        return self.collection.replace_one(filter=filterObj, replacement=replaceObj, upsert=upsert)

    def update_one_doc(self, filterObj, updateObj, upsert=False):
        """
        Update a single document matching the filter.
        Example:
            for doc in db.test.find_doc():
                print(doc)
                {u'x': 1, u'_id': 0}
                {u'x': 1, u'_id': 1}
                {u'x': 1, u'_id': 2}
        Input: filterObj, updateObj
            >>> result = db.test.update_one_doc({'x': 1}, {'$inc': {'x': 3}})
        Output:   
            >>> result.matched_count
                1
            >>> result.modified_count
                1
            >>> for doc in db.test.find_doc():
                print(doc)
                {u'x': 4, u'_id': 0}
                {u'x': 1, u'_id': 1}
                {u'x': 1, u'_id': 2}
        Parameters:
            - filterObj: A query that matches the document to update.
            - updateObj:The modifications to apply.
            - upsert (optional): If True, perform an insert if no documents match the filter.
        """
        return self.collection.update_one(filter=filterObj, update=updateObj, upsert=upsert)

    def update_many_doc(self, filterObj, updateObj, upsert=False, arrayfilters=None):
        """
        Update one or more documents that match the filter.
        Example:
                >>> for doc in db.test.find_doc():
                            print(doc)
                {u'x': 1, u'_id': 0}
                {u'x': 1, u'_id': 1}
                {u'x': 1, u'_id': 2}
            Input: filterObj, updateObj, upsert, arrayfilters
                    result = db.test.update_many_doc({'x': 1}, {'$inc': {'x': 3}})
            Output:    
                    result.matched_count
                    >>> 3
                    result.modified_count
                    >>> 3
                    for doc in db.test.find_doc():
                    print(doc)
                    {u'x': 4, u'_id': 0}
                    {u'x': 4, u'_id': 1}
                    {u'x': 4, u'_id': 2}
        Parameters:
            - filterObj: A query that matches the documents to update.
            - updateObj: The modifications to apply.
            - upsert (optional): If True, perform an insert if no documents match the filter.
            - arrayfilters: (optional): A list of filters specifying which array elements an update should apply. 
                Requires MongoDB 3.6+
        Return:
            An instance of UpdateResult.
        """
        return self.collection.update_many(filter=filterObj, update=updateObj, upsert=upsert,
                                           array_filters=arrayfilters)

    def delete_one_doc(self, filterObj):
        """
        Delete a single document matching the filter.
        Example:
            Input:
                db.test.count_documents({'x': 1})
                    >>> 3
                result = db.test.delete_one({'x': 1})
            Output:   
                result.deleted_count
                    >>> 1
                db.test.count_documents({'x': 1})
                    >>>2
        Parameters:
            - filterObj: A query that matches the document to delete.
        Return:
            An instance of DeleteResult.
        """
        return self.collection.delete_one(filterObj)

    def bulk_write_doc(self, requests, ordered=True):
        """
        Send a batch of write operations to the server.
        Requests are passed as a list of write operation instances ( InsertOne, UpdateOne, UpdateMany, ReplaceOne, 
        DeleteOne, or DeleteMany).
        Example :
            Input: 
                requests = [InsertOne({'y': 1}), DeleteOne({'x': 1}),
                        ReplaceOne({'w': 1}, {'z': 1}, upsert=True)]
                result = db.test.bulk_write(requests)
            output:
                >>> result.inserted_count
                1
                >>> result.deleted_count
                1
                >>> result.modified_count
                0
                >>> result.upserted_ids
                {2: ObjectId('54f62ee28891e756a6e1abd5')}
                >>> for doc in db.test.find({}):
                    print(doc)
                {u'x': 1, u'_id': ObjectId('54f62e60fba5226811f634f0')}
                {u'y': 1, u'_id': ObjectId('54f62ee2fba5226811f634f1')}
                {u'z': 1, u'_id': ObjectId('54f62ee28891e756a6e1abd5')}
        Parameter: 
            - requests: A list of write operations (see examples above).
            - ordered (optional): If True (the default) requests will be performed on the server serially, 
                in the order provided. If an error occurs all remaining operations are aborted. 
                If False requests will be performed on the server in arbitrary order,
                possibly in parallel, and all operations will be attempted.
        """
        return self.collection.bulk_write(requests=requests, ordered=ordered)

    def delete_many_doc(self, filterObj):
        """
        Delete one or more documents matching the filter.
        Example:
            db.test.count_documents({'x': 1})
                >>> 3
            Input:
                result = db.test.delete_many_doc({'x': 1})
            Output:
                result.deleted_count
                >>> 3
                db.test.count_documents({'x': 1})
                >>>   0
        Parameters:
            - filterObj: A query that matches the documents to delete.
        Return:
            An instance of DeleteResult.
        """
        return self.collection.delete_many(filterObj)

    def find_doc(self, filterObj=None, projection=None, limit=0, sort=None, allow_partial_results=False,
                 batch_size=0,
                 max_time_ms=None, max=None, min=None):
        """
        Query the database.
        The filter argument is a prototype document that all results must match. For example:
            >>> db.test.find_doc({"hello": "world"})
        - only matches documents that have a key “hello” with value “world”. Matches can have other keys in addition to 
        “hello”. The projection argument is used to specify a subset of fields that should be included in the result 
        documents. By limiting results to a certain subset of fields you can cut down on network traffic and decoding time.
        - Raises TypeError if any of the arguments are of improper type. Returns an instance of Cursor corresponding to this 
        query.
        - The find_doc() method obeys the read_preference of this Collection.
        Parameters: 
            - filterObj (optional): a SON object specifying elements which must be present for a document to be included in
            the result set
            - projection (optional): a list of field names that should be returned in the result set or a dict specifying 
            the fields to include or exclude.
            If projection is a list “_id” will always be returned. Use a dict to exclude fields from the result 
            (e.g. projection={‘_id’: False}).
            - limit (optional): the maximum number of results to return. A limit of 0 (the default) is equivalent to 
            setting no limit.
            - sort (optional): a list of (key, direction) pairs specifying the sort order for this query. See sort() for 
            details.
            - allow_partial_results (optional): if True, mongos will return partial results if some shards are down instead
            of returning an error.
            - batch_size (optional): Limits the number of documents returned in a single batch.
            - max_time_ms (optional): Specifies a time limit for a query operation. If the specified time is exceeded, 
            the operation will be aborted and ExecutionTimeout is raised. Pass this as an alternative to calling 
            max_time_ms() on the cursor.
            - min (optional): A list of field, limit pairs specifying the inclusive lower bound for all keys of a specific 
            index in order. 
            Pass this as an alternative to calling min() on the cursor. hint must also be passed to ensure the query
            utilizes the correct index.
            - max (optional): A list of field, limit pairs specifying the exclusive upper bound for all keys of a specific 
            index in order.
            Pass this as an alternative to calling max() on the cursor. hint must also be passed to ensure the query
            utilizes the correct index.
        """
        return self.collection.find(filter=filterObj, projection=projection, limit=limit, sort=sort,
                                    allow_partial_results=allow_partial_results, batch_size=batch_size,
                                    max_time_ms=max_time_ms, max=max, min=min)

    def find_one_doc(self, filterObj=None):
        """
        Get a single document from the database.
        All arguments to find_doc() are also valid arguments for find_one_doc(), although any limit argument will be ignored. 
        Returns a single document, or None if no matching document is found.
        The find_one_doc() method obeys the read_preference of this Collection.
        Parameters:
            - filterObj (optional): a dictionary specifying the query to be performed OR any other type to be used as the 
            value for a query for "_id".
        Return:
            Returns a single document 
        """
        return self.collection.find_one(filter=filterObj)

    def find_one_and_delete_doc(self, filterObj, projection=None, sort=None):
        """
        Finds a single document and deletes it, returning the document.
            For example:
                db.test.count_documents({'x': 1})
            >>>  2
            db.test.find_one_and_delete_doc({'x': 1})
            >>>  {u'x': 1, u'_id': ObjectId('54f4e12bfba5220aa4d6dee8')}
            db.test.count_documents({'x': 1})
            >>>  1
        If multiple documents match filter, a sort can be applied.
        for doc in db.test.find({'x': 1}):
            >>> print(doc)
            {u'x': 1, u'_id': 0}
            {u'x': 1, u'_id': 1}
            {u'x': 1, u'_id': 2}
            db.test.find_one_and_delete_doc({'x': 1}, sort=[('_id', pymongo.DESCENDING)])
            >>> {u'x': 1, u'_id': 2}
        The projection option can be used to limit the fields returned.
            db.test.find_one_and_delete({'x': 1}, projection={'_id': False})
            >>> {u'x': 1}
        Parameters:
            - filterObj: A query that matches the document to delete.
            - projection (optional): a list of field names that should be returned in 
            the result document or a mapping specifying the fields to include or exclude. 
            If projection is a list “_id” will always be returned. 
            Use a mapping to exclude fields from the result (e.g. projection={‘_id’: False}).
            - sort (optional): a list of (key, direction) pairs specifying the sort order for the query. 
            If multiple documents match the query, they are sorted and the first is deleted.
        """
        return self.collection.find_one_and_delete(filter=filterObj, projection=projection, sort=sort)

    def find_one_and_replace_doc(self, filterObj, replacement, projection=None, sort=None):
        """
        Finds a single document and replaces it, returning either the original or the replaced document.
        The find_one_and_replace_doc() method differs from find_one_and_update_doc() by replacing the document matched by 
        filter, rather than modifying the existing document.
        For example:
            for doc in db.test.find_doc({}):
                >>> print(doc)
                {u'x': 1, u'_id': 0}
                {u'x': 1, u'_id': 1}
                {u'x': 1, u'_id': 2}
            db.test.find_one_and_replace_doc({'x': 1}, {'y': 1})
                >>> {u'x': 1, u'_id': 0}
            for doc in db.test.find_doc({}):
                >>> print(doc)
                {u'y': 1, u'_id': 0}
                {u'x': 1, u'_id': 1}
                {u'x': 1, u'_id': 2}
        Parameters:
            - filterObj: A query that matches the document to replace.
            - replacement: The replacement document.
            - projection (optional): A list of field names that should be returned in the result document 
            or a mapping specifying the fields to include or exclude. If projection is a list “_id” will always be returned. 
            Use a mapping to exclude fields from the result (e.g. projection={‘_id’: False}).
            - sort (optional): a list of (key, direction) pairs specifying the sort order for the query. 
            If multiple documents match the query, they are sorted and the first is replaced.
            - upsert (optional): When True, inserts a new document if no document matches the query. Defaults to False.
        """
        return self.collection.find_one_and_replace(filter=filterObj, replacement=replacement, projection=projection,
                                                    sort=sort)

    def find_one_and_update_doc(self, filterObj, update, projection=None, sort=None):
        """
        Finds a single document and updates it, returning either the original or the updated document.
        For Example:
            db.test.find_one_and_update_doc( {'_id': 665}, {'$inc': {'count': 1}, '$set': {'done': True}})
                >>> {u'_id': 665, u'done': False, u'count': 25}}
        Returns None if no document matches the filter.        
        For Example:
            db.test.find_one_and_update_doc({'_exists': False}, {'$inc': {'count': 1}}) 
        You can limit the fields returned with the projection option
                db.example.find_one_and_update_doc(
                    {'_id': 'userid'},
                    {'$inc': {'seq': 1}},
                    projection={'seq': True, '_id': False})
                >>> {u'seq': 2}
        Parameters:
            - filterObj:A query that matches the document to update.
            - update:The update operations to apply.
            - projection (optional): A list of field names that should be returned in the result document 
            or a mapping specifying the fields to include or exclude. If projection is a list 
            “_id” will always be returned. Use a dict to exclude fields from the result (e.g. projection={‘_id’: False}).
            - Sort (optional): a list of (key, direction) pairs specifying the sort order for the query. 
            If multiple documents match the query, they are sorted and the first is updated.
        """
        return self.collection.find_one_and_update(filter=filterObj, update=update, projection=projection, sort=sort)

    def find_all_doc(self):
        return self.collection.find({})

    def count_documents(self, filterObj):
        """
        Count the number of documents in this collection.
        The count_documents() method is supported in a transaction.
        Parameters:
            - filterObj (required): A query document that selects which documents to count in the collection. 
            Can be an empty document to count all documents.
        """
        return self.collection.count_documents(filter=filterObj)
