"""Create a small local MongoDB dataset for CS 499 Enhancement Three.

This script creates representative test records that use the fields
required by the original Grazioso Salvare dashboard. The records are
synthetic and are intended only for local development and testing.
"""

from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "aac"
COLLECTION_NAME = "animals"
TEST_SOURCE = "CS499_LOCAL_TEST_DATA"


TEST_ANIMALS = [
    {
        "animal_id": "CS499-A001",
        "name": "River",
        "animal_type": "Dog",
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 52,
        "location_lat": 30.2672,
        "location_long": -97.7431,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A002",
        "name": "Harbor",
        "animal_type": "Dog",
        "breed": "Chesapeake Bay Retriever",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 78,
        "location_lat": 30.2711,
        "location_long": -97.7437,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A003",
        "name": "Bay",
        "animal_type": "Dog",
        "breed": "Newfoundland",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 104,
        "location_lat": 30.2750,
        "location_long": -97.7460,
        "outcome_type": "Transfer",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A004",
        "name": "Summit",
        "animal_type": "Dog",
        "breed": "German Shepherd",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 104,
        "location_lat": 30.2800,
        "location_long": -97.7500,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A005",
        "name": "Aspen",
        "animal_type": "Dog",
        "breed": "Alaskan Malamute",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 90,
        "location_lat": 30.2900,
        "location_long": -97.7600,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A006",
        "name": "Snow",
        "animal_type": "Dog",
        "breed": "Siberian Husky",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 120,
        "location_lat": 30.2850,
        "location_long": -97.7550,
        "outcome_type": "Transfer",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A007",
        "name": "Tracker",
        "animal_type": "Dog",
        "breed": "Bloodhound",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 40,
        "location_lat": 30.2500,
        "location_long": -97.7300,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A008",
        "name": "Scout",
        "animal_type": "Dog",
        "breed": "Doberman Pinscher",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 60,
        "location_lat": 30.2450,
        "location_long": -97.7200,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A009",
        "name": "Justice",
        "animal_type": "Dog",
        "breed": "Rottweiler",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 48,
        "location_lat": 30.2400,
        "location_long": -97.7150,
        "outcome_type": "Transfer",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A010",
        "name": "Molly",
        "animal_type": "Dog",
        "breed": "Golden Retriever",
        "sex_upon_outcome": "Spayed Female",
        "age_upon_outcome_in_weeks": 130,
        "location_lat": 30.2600,
        "location_long": -97.7350,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A011",
        "name": "Puppy",
        "animal_type": "Dog",
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 10,
        "location_lat": 30.2580,
        "location_long": -97.7380,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
    {
        "animal_id": "CS499-A012",
        "name": "Whiskers",
        "animal_type": "Cat",
        "breed": "Domestic Shorthair",
        "sex_upon_outcome": "Neutered Male",
        "age_upon_outcome_in_weeks": 80,
        "location_lat": 30.2550,
        "location_long": -97.7450,
        "outcome_type": "Adoption",
        "test_data_source": TEST_SOURCE,
    },
]


def main() -> None:
    """Create the local test data and supporting index."""

    client = None

    try:
        print("Connecting to local MongoDB...")

        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
        )

        client.admin.command("ping")
        print("MongoDB connection successful.")

        database = client[DATABASE_NAME]
        collection = database[COLLECTION_NAME]

        print("\nRemoving previous CS 499 generated test records...")

        delete_result = collection.delete_many(
            {"test_data_source": TEST_SOURCE}
        )

        print(
            f"Removed {delete_result.deleted_count} previous test records."
        )

        print("\nInserting representative test records...")

        insert_result = collection.insert_many(TEST_ANIMALS)

        print(f"Inserted {len(insert_result.inserted_ids)} records.")

        print("\nCreating rescue-search index...")

        index_name = collection.create_index(
            [
                ("animal_type", ASCENDING),
                ("sex_upon_outcome", ASCENDING),
                ("age_upon_outcome_in_weeks", ASCENDING),
            ],
            name="rescue_search_idx",
        )

        print(f"Index available: {index_name}")

        record_count = collection.count_documents(
            {"test_data_source": TEST_SOURCE}
        )

        print("\nVerification")
        print("-" * 40)
        print(f"Database: {DATABASE_NAME}")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Generated test records: {record_count}")

        print("\nGenerated animal records:")

        records = collection.find(
            {"test_data_source": TEST_SOURCE},
            {
                "_id": 0,
                "animal_id": 1,
                "name": 1,
                "animal_type": 1,
                "breed": 1,
            },
        ).sort("animal_id", ASCENDING)

        for record in records:
            print(record)

        print("\nDatabase setup completed successfully.")

    except PyMongoError as error:
        print("\nDatabase setup failed.")
        print(f"{type(error).__name__}: {error}")
        raise

    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()