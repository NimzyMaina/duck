from dotenv import load_dotenv

from db.base import Base
from db.client import Session, engine
from db.sale import Sale
from models.sales import Sales
from utils.writer import write_list_to_csv

# load env variables
load_dotenv()
# Get DB session
db = Session()
# Create the tables
Base.metadata.create_all(engine)

from utils.logger import logger
from utils.reader import load_sales_from_excel

file_path = './data/Test_Data.xlsx'
sales, errors = load_sales_from_excel(file_path)

# log data that failed validation for further processing
if errors:
    logger.error("Writing errors to csv file for further processing")
    errs = [{
        "row": err["row"],
        "errors": err["errors"],
        **err["data"]
    } for err in errors]
    # these errors can be displayed back to the user for further processing or just ignored depending on needs
    # you can get list of locations that have bad quality data from this list as well
    write_list_to_csv(errs, './errors/errors.csv')

# Convert Pydantic models to dicts if needed
if sales:
    try:
        if isinstance(sales[0], Sales):
            records = [r.model_dump() for r in sales]
            db.bulk_insert_mappings(Sale, records)
            db.commit()
    except Exception as e:
        logger.error(f"Error inserting records: {e}")
        db.rollback()
    finally:
        db.close()
