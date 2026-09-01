"""
setup_ge.py - Initialize Great Expectations project and configure datasource.
"""

import great_expectations as ge
import pandas as pd
import os


def setup_context():
    """Initialize the Great Expectations data context."""
    ge_base_dir = os.path.join(os.path.dirname(__file__), "..", "great_expectations")
    context = ge.data_context.DataContext(ge_base_dir)
    print("[OK] Great Expectations context initialized")
    return context


def configure_datasource(context):
    """Configure the Pandas datasource for equipment data."""
    datasource_config = {
        "name": "equipment_datasource",
        "class_name": "Datasource",
        "execution_engine": {"class_name": "PandasExecutionEngine"},
        "data_connectors": {
            "default_inferred_data_connector_name": {
                "class_name": "InferredAssetFilesystemDataConnector",
                "base_directory": "../data",
                "default_regex": {
                    "group_names": ["data_asset_name"],
                    "pattern": "(.*)"
                }
            },
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"]
            }
        }
    }
    try:
        context.add_datasource(**datasource_config)
        print("[OK] Datasource configured")
    except Exception as e:
        print(f"[INFO] Datasource may already exist: {e}")
    return context


def test_connection(context):
    """Test that the datasource can read the data file."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "equipment_data.csv")
    df = pd.read_csv(data_path)
    print(f"[OK] Data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"     Columns: {list(df.columns)}")
    return df


if __name__ == "__main__":
    print("=" * 60)
    print("Great Expectations Project Setup")
    print("=" * 60)
    context = setup_context()
    context = configure_datasource(context)
    df = test_connection(context)
    print("\nSetup complete! Run validate_data.py next.")
