"""
create_expectations.py - Programmatically create the expectation suite.
"""

import great_expectations as ge
import os


def create_expectation_suite(context):
    """Create the expectation suite with all expectations."""
    suite_name = "equipment_data_suite"
    try:
        suite = context.get_expectation_suite(suite_name)
        print("[INFO] Suite already exists, updating...")
    except Exception:
        suite = context.add_expectation_suite(suite_name)
        print(f"[OK] Created suite '{suite_name}'")

    expectations = [
        ("expect_table_columns_to_match_ordered_list", {
            "column_list": ["equipment_id", "temperature", "vibration", "pressure", "age_hours", "load", "failure", "inspection_date"]
        }),
        ("expect_table_row_count_to_be_between", {"min_value": 1, "max_value": 100000}),
        ("expect_column_values_to_not_be_null", {"column": "equipment_id"}),
        ("expect_column_values_to_not_be_null", {"column": "temperature"}),
        ("expect_column_values_to_not_be_null", {"column": "failure"}),
        ("expect_column_values_to_be_between", {"column": "temperature", "min_value": 50, "max_value": 120}),
        ("expect_column_values_to_be_between", {"column": "vibration", "min_value": 0, "max_value": 10}),
        ("expect_column_values_to_be_between", {"column": "pressure", "min_value": 80, "max_value": 150}),
        ("expect_column_values_to_be_between", {"column": "age_hours", "min_value": 0, "max_value": 10000}),
        ("expect_column_values_to_be_between", {"column": "load", "min_value": 0.0, "max_value": 1.0}),
        ("expect_column_values_to_be_in_set", {"column": "failure", "value_set": [0, 1]}),
        ("expect_column_values_to_be_unique", {"column": "equipment_id"}),
    ]

    for exp_type, kwargs in expectations:
        suite.add_expectation(
            ge.core.ExpectationConfiguration(expectation_type=exp_type, kwargs=kwargs)
        )
        col = kwargs.get("column", "table-level")
        print(f"  [+] {exp_type} on '{col}'")

    context.save_expectation_suite(suite)
    print(f"\n[OK] Saved suite with {len(suite.expectations)} expectations")
    return suite


if __name__ == "__main__":
    print("=" * 60)
    print("Creating Great Expectations Suite")
    print("=" * 60)
    ge_base_dir = os.path.join(os.path.dirname(__file__), "..", "great_expectations")
    context = ge.data_context.DataContext(ge_base_dir)
    suite = create_expectation_suite(context)
    print("\nSuite created! Run validate_data.py to test.")
