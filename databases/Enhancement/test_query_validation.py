"""Test approved and rejected MongoDB query structures."""

from CRUD_Python_Module import AnimalShelter


TEST_CASES = [
    {
        "name": "Empty reset query",
        "query": {},
        "expected": True,
    },
    {
        "name": "Simple animal-type query",
        "query": {"animal_type": "Dog"},
        "expected": True,
    },
    {
        "name": "Valid age-range query",
        "query": {
            "age_upon_outcome_in_weeks": {
                "$gte": 26,
                "$lte": 156,
            }
        },
        "expected": True,
    },
    {
        "name": "Valid Water Rescue query",
        "query": {
            "animal_type": "Dog",
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {
                "$gte": 26,
                "$lte": 156,
            },
            "$or": [
                {
                    "breed": {
                        "$regex": "Labrador Retriever",
                        "$options": "i",
                    }
                },
                {
                    "breed": {
                        "$regex": "Chesapeake Bay Retriever",
                        "$options": "i",
                    }
                },
                {
                    "breed": {
                        "$regex": "Newfoundland",
                        "$options": "i",
                    }
                },
            ],
        },
        "expected": True,
    },
    {
        "name": "Unknown field",
        "query": {"account_password": "test"},
        "expected": False,
    },
    {
        "name": "Unsupported operator",
        "query": {"breed": {"$ne": "Labrador Retriever"}},
        "expected": False,
    },
    {
        "name": "Top-level unsupported operator",
        "query": {"$where": "return true"},
        "expected": False,
    },
    {
        "name": "Malformed or condition",
        "query": {"$or": "not a list"},
        "expected": False,
    },
    {
        "name": "Invalid query type",
        "query": ["animal_type", "Dog"],
        "expected": False,
    },
    {
        "name": "Incorrect age value type",
        "query": {
            "age_upon_outcome_in_weeks": {
                "$gte": "twenty-six",
            }
        },
        "expected": False,
    },
]


def main() -> None:
    """Run validation and database-integration tests."""

    shelter = None
    failures = 0

    try:
        shelter = AnimalShelter()

        print("Running query-validation tests...\n")

        for test_case in TEST_CASES:
            actual = shelter._is_valid_query(test_case["query"])
            expected = test_case["expected"]

            if actual == expected:
                result = "PASS"
            else:
                result = "FAIL"
                failures += 1

            print(
                f"{result}: {test_case['name']} "
                f"(expected={expected}, actual={actual})"
            )

        print("\nTesting valid query through read()...")

        valid_records = shelter.read({"animal_type": "Dog"})

        if valid_records:
            print(
                f"PASS: Valid read returned "
                f"{len(valid_records)} records."
            )
        else:
            print("FAIL: Valid read returned no records.")
            failures += 1

        print("\nTesting invalid query through read()...")

        invalid_records = shelter.read(
            {"breed": {"$ne": "Labrador Retriever"}}
        )

        if invalid_records == []:
            print("PASS: Invalid read was rejected safely.")
        else:
            print("FAIL: Invalid read returned records.")
            failures += 1

        print()

        if failures:
            raise RuntimeError(
                f"{failures} query-validation test(s) failed."
            )

        print("QUERY VALIDATION TEST PASSED")

    finally:
        if shelter is not None:
            shelter.close()


if __name__ == "__main__":
    main()