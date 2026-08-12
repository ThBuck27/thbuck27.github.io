"""MongoDB CRUD module for the Grazioso Salvare dashboard."""

from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """Provide MongoDB CRUD operations for the AAC animals collection."""

    ALLOWED_QUERY_FIELDS = {
        "animal_id",
        "name",
        "animal_type",
        "breed",
        "sex_upon_outcome",
        "age_upon_outcome_in_weeks",
        "test_data_source",
    }

    ALLOWED_QUERY_OPERATORS = {
        "$or",
        "$gte",
        "$lte",
        "$regex",
        "$options",
    }    

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: str = "127.0.0.1",
        port: int = 27017,
        database_name: str = "aac",
        collection_name: str = "animals",
        auth_source: str = "admin",
    ) -> None:
        """Create and verify the MongoDB connection.

        When username and password are supplied, authentication is used.
        When both are omitted, the local MongoDB instance is used without
        authentication.
        """

        if bool(username) != bool(password):
            raise ValueError(
                "Username and password must either both be supplied "
                "or both be omitted."
            )

        try:
            if username and password:
                self.client = MongoClient(
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    authSource=auth_source,
                    serverSelectionTimeoutMS=5000,
                )
            else:
                self.client = MongoClient(
                    host=host,
                    port=port,
                    serverSelectionTimeoutMS=5000,
                )

            # Force PyMongo to verify the connection immediately.
            self.client.admin.command("ping")

            self.database = self.client[database_name]
            self.collection = self.database[collection_name]

        except PyMongoError as error:
            print(f"MongoDB connection failed: {error}")
            raise

    def _is_valid_query(self, query: Any) -> bool:
        """Return True when a query uses approved fields and operators."""

        if not isinstance(query, dict):
            return False

        # An empty query is allowed because the dashboard Reset option
        # intentionally retrieves all records.
        if not query:
            return True

        for key, value in query.items():
            if key == "$or":
                if not isinstance(value, list) or not value:
                    return False

                if not all(self._is_valid_query(item) for item in value):
                    return False

                continue

            if key.startswith("$"):
                return False

            if key not in self.ALLOWED_QUERY_FIELDS:
                return False

            if isinstance(value, dict):
                for operator, operator_value in value.items():
                    if operator not in self.ALLOWED_QUERY_OPERATORS:
                        return False

                    if operator == "$options":
                        if not isinstance(operator_value, str):
                            return False

                    elif operator == "$regex":
                        if not isinstance(operator_value, str):
                            return False

                    elif operator in {"$gte", "$lte"}:
                        if not isinstance(operator_value, (int, float)):
                            return False

        return True

    def create(self, data: Dict[str, Any]) -> bool:
        """Insert one document into the animals collection."""

        if not isinstance(data, dict) or not data:
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged

        except PyMongoError as error:
            print(f"Create failed: {error}")
            return False

    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return documents matching an approved MongoDB query."""

        if not self._is_valid_query(query):
            print("Read rejected: query contains unsupported content.")
            return []

        try:
            return list(self.collection.find(query))

        except PyMongoError as error:
            print(f"Read failed: {error}")
            return []

    def update(
        self,
        query: Dict[str, Any],
        new_values: Dict[str, Any],
    ) -> int:
        """Update documents matching the supplied query."""

        if not isinstance(query, dict) or not isinstance(new_values, dict):
            return 0

        if not query or not new_values:
            return 0

        try:
            result = self.collection.update_many(query, new_values)
            return result.modified_count

        except PyMongoError as error:
            print(f"Update failed: {error}")
            return 0

    def delete(self, query: Dict[str, Any]) -> int:
        """Delete documents matching the supplied query."""

        if not isinstance(query, dict) or not query:
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count

        except PyMongoError as error:
            print(f"Delete failed: {error}")
            return 0

    def create_rescue_search_index(self) -> str:
        """Create the compound index used by common rescue searches."""

        try:
            return self.collection.create_index(
                [
                    ("animal_type", 1),
                    ("sex_upon_outcome", 1),
                    ("age_upon_outcome_in_weeks", 1),
                ],
                name="rescue_search_idx",
            )

        except PyMongoError as error:
            print(f"Index creation failed: {error}")
            return ""

    def get_index_information(self) -> Dict[str, Any]:
        """Return metadata for all collection indexes."""

        try:
            return self.collection.index_information()

        except PyMongoError as error:
            print(f"Index inspection failed: {error}")
            return {}

    def close(self) -> None:
        """Close the MongoDB client connection."""

        self.client.close()