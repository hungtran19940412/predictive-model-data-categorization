import re
import logging
from typing import Dict, Any, Optional
import pandas as pd
from pydantic import BaseModel, ValidationError

class DataSchema(BaseModel):
    text: str
    source: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Data validator initialized")

    def validate_single_record(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate a single data record"""
        try:
            validated = DataSchema(**record)
            return validated.dict()
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            return None

    def validate_batch(self, records: list) -> list:
        """Validate a batch of records"""
        return [self.validate_single_record(record) for record in records if record is not None]

    def check_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform data quality checks"""
        quality_report = {
            'total_records': len(data),
            'missing_values': data.isnull().sum().to_dict(),
            'duplicates': data.duplicated().sum(),
            'text_length_stats': {
                'min': data['text'].str.len().min(),
                'max': data['text'].str.len().max(),
                'mean': data['text'].str.len().mean()
            }
        }
        return quality_report

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    validator = DataValidator()
    sample_record = {
        'text': 'Sample text',
        'source': 'test',
        'timestamp': '2024-01-01T00:00:00Z'
    }
    validated = validator.validate_single_record(sample_record)
    print(f"Validated record: {validated}")