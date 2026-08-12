from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """CRUD operations for the AAC animals collection in MongoDB."""

    def __init__(self, username, password):
        """
        Initialize MongoDB connection settings and connect to the database.

        Args:
            username (str): MongoDB username
            password (str): MongoDB password
        """
        # Connection variables
        HOST = "localhost"
        PORT = 27017
        DB = "aac"
        COL = "animals"

        try:
            # Initialize MongoDB client with authentication
            self.client = MongoClient(
                f"mongodb://{username}:{password}@{HOST}:{PORT}"
            )
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except PyMongoError as e:
            print(f"Connection failed: {e}")
            raise

    def create(self, data):
        """
        Insert a document into the animals collection.

        Args:
            data (dict): Dictionary containing document data

        Returns:
            bool: True if insert succeeds, otherwise False
        """
        try:
            if data is not None:
                self.collection.insert_one(data)
                return True
            else:
                return False
        except PyMongoError as e:
            print(f"Create failed: {e}")
            return False

    def read(self, query):
        """
        Query documents from the animals collection.

        Args:
            query (dict): MongoDB query dictionary

        Returns:
            list: List of matching documents, or empty list if none/failure
        """
        try:
            if query is not None:
                cursor = self.collection.find(query)
                return list(cursor)
            else:
                return []
        except PyMongoError as e:
            print(f"Read failed: {e}")
            return []

    def update(self, query, new_values):
        """
        Update document(s) in the animals collection.

        Args:
            query (dict): MongoDB query dictionary used to match documents
            new_values (dict): Update operation dictionary such as
                               {"$set": {"name": "New Name"}}

        Returns:
            int: Number of documents modified
        """
        try:
            if query is not None and new_values is not None:
                result = self.collection.update_many(query, new_values)
                return result.modified_count
            else:
                return 0
        except PyMongoError as e:
            print(f"Update failed: {e}")
            return 0

    def delete(self, query):
        """
        Delete document(s) from the animals collection.

        Args:
            query (dict): MongoDB query dictionary used to match documents

        Returns:
            int: Number of documents deleted
        """
        try:
            if query is not None:
                result = self.collection.delete_many(query)
                return result.deleted_count
            else:
                return 0
        except PyMongoError as e:
            print(f"Delete failed: {e}")
            return 0