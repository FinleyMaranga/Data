# Great Expectations Data Validation Project

## Part A: Data Quality Validation with Great Expectations

This project uses Great Expectations to validate equipment sensor data for predictive maintenance.

## Usage

Step 1: python scripts/setup_ge.py
Step 2: python scripts/create_expectations.py
Step 3: python scripts/validate_data.py

## Expectations Defined

1. Column order matches expected schema (8 columns)
2. Row count between 1 and 100,000
3. No null values in equipment_id, temperature, failure
4. Temperature between 50-120
5. Vibration between 0-10
6. Pressure between 80-150
7. Age hours between 0-10,000
8. Load between 0.0-1.0
9. Failure values must be 0 or 1
10. Equipment IDs must be unique
