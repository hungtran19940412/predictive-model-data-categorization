import logging
import pandas as pd
from typing import Dict, Any, Optional
import json
from jsonschema import validate, ValidationError

class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Data validator initialized")

    def validate_csv(self, file_path: str, schema: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """Validate CSV file against schema"""
        try:
            df = pd.read_csv(file_path)
            self._validate_dataframe(df, schema)
            return df
        except Exception as e:
            self.logger.error(f"CSV validation error: {e}")
            return None

    def validate_json(self, file_path: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate JSON file against schema"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            validate(instance=data, schema=schema)
            return data
        except (ValidationError, json.JSONDecodeError) as e:
            self.logger.error(f"JSON validation error: {e}")
            return None

    def _validate_dataframe(self, df: pd.DataFrame, schema: Dict[str, Any]) -> bool:
        """Validate DataFrame against schema"""
        try:
            # Check required columns
            for col in schema.get('required_columns', []):
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            # Check data types
            for col, dtype in schema.get('column_types', {}).items():
                if col in df.columns and not pd.api.types.is_dtype(df[col].dtype, dtype):
                    raise ValueError(f"Invalid data type for column {col}. Expected {dtype}")
            
            # Check for null values in required columns
            for col in schema.get('non_null_columns', []):
                if df[col].isnull().any():
                    raise ValueError(f"Null values found in column {col}")
            
            return True
        except Exception as e:
            self.logger.error(f"DataFrame validation error: {e}")
            raise

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    validator = DataValidator()
    
    # Example CSV validation
    csv_schema = {
        'required_columns': ['id', 'name', 'age'],
        'column_types': {'age': 'int64'},
        'non_null_columns': ['id', 'name']
    }
    
    # Example JSON validation
    json_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "age": {"type": "number"}
        },
        "required": ["id", "name"]
    }
    
    print("Data validator initialized successfully")