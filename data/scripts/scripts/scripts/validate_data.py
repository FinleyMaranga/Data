"""
validate_data.py - Run Great Expectations validation on equipment data.
"""

import great_expectations as ge
from great_expectations.core.batch import BatchRequest
import pandas as pd
import os
import sys


def load_data():
    """Load the equipment dataset."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "equipment_data.csv")
    df = pd.read_csv(data_path)
    print(f"[OK] Loaded {len(df)} rows from equipment_data.csv")
    return df


def run_validation(context, df):
    """Run the expectation suite against the data."""
    batch_request = BatchRequest(
        datasource_name="equipment_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="equipment_data",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "default_identifier"}
    )
    results = context.run_checkpoint(
        checkpoint_name="equipment_checkpoint",
        batch_request=batch_request
    )
    return results


def display_results(results):
    """Display validation results summary."""
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    if results.success:
        print("\n[PASS] All expectations passed!")
    else:
        print("\n[FAIL] Some expectations failed:")
    for run_result in results.run_results.values():
        for exp_result in run_result["validation_result"].results:
            status = "PASS" if exp_result.success else "FAIL"
            exp_type = exp_result.expectation_config.expectation_type
            column = exp_result.expectation_config.kwargs.get("column", "table-level")
            print(f"  [{status}] {exp_type} on '{column}'")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("Equipment Data Validation with Great Expectations")
    print("=" * 60)
    ge_base_dir = os.path.join(os.path.dirname(__file__), "..", "great_expectations")
    context = ge.data_context.DataContext(ge_base_dir)
    print("[OK] Context loaded")
    df = load_data()
    try:
        results = run_validation(context, df)
        display_results(results)
        context.build_data_docs()
        print("[OK] Data docs generated")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    print("\nValidation complete!")
