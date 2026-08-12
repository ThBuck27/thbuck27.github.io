"""Verify the enhanced MongoDB CRUD connection and index."""

from CRUD_Python_Module import AnimalShelter


def main() -> None:
    """Run basic local database checks."""

    shelter = None

    try:
        print("Creating local AnimalShelter connection...")

        shelter = AnimalShelter()

        print("Connection successful.")

        records = shelter.read(
            {"test_data_source": "CS499_LOCAL_TEST_DATA"}
        )

        print(f"Generated test records found: {len(records)}")

        if not records:
            raise RuntimeError(
                "No generated test records were found. "
                "Run seed_local_database.py first."
            )

        print("\nFirst record:")

        first_record = records[0].copy()
        first_record.pop("_id", None)

        print(first_record)

        index_name = shelter.create_rescue_search_index()

        print(f"\nIndex creation result: {index_name}")

        indexes = shelter.get_index_information()

        print("\nAvailable indexes:")

        for name, details in indexes.items():
            print(f"- {name}: {details.get('key')}")

        if "rescue_search_idx" not in indexes:
            raise RuntimeError(
                "The rescue_search_idx index was not found."
            )

        print("\nDATABASE CONNECTION TEST PASSED")

    except Exception as error:
        print("\nDATABASE CONNECTION TEST FAILED")
        print(f"{type(error).__name__}: {error}")
        raise

    finally:
        if shelter is not None:
            shelter.close()


if __name__ == "__main__":
    main()