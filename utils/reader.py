from pydantic import ValidationError

from models.sales import Sales
from utils.logger import logger
import pandas as pd



def load_sales_from_excel(file_path: str) -> tuple[list[Sales], list[dict]]:
    with logger.span("Loading sales from excel={file_path}", file_path=file_path):
        # Read Excel file
        df = pd.read_excel(file_path)

        # Normalize column names (remove spaces, make snake_case)
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
        )

        records = []
        errors = []

        for i, row in df.iterrows():
            try:
                record = Sales(**row.to_dict())
                records.append(record)
            except ValidationError as e:
                errors.append({
                    "row": i + 2,
                    "errors": e.errors(),
                    "data": row.to_dict()
                })

        if errors:
            logger.error("Validation errors found:")
            for err in errors:
                logger.debug("Row {row}: {errors}, {data}", row=err['row'], errors=err['errors'], data=err['data'])
        else:
            logger.info("✅ All rows validated successfully!")

        return records, errors