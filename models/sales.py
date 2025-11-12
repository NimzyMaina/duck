from pydantic import BaseModel, Field
from datetime import date

class Sales(BaseModel):
    store_name: str = Field(..., description="Name of the store where the sale occurred")
    item_code: int = Field(..., description="Unique item code")
    item_barcode: int = Field(..., description="Barcode of the item")
    description: str = Field(None, description="Description of the item")
    category: str = Field(None, description="Product category")
    department: str = Field(None, description="Main department")
    sub_department: str = Field(None, description="Sub-department of the product")
    section: str = Field(None, description="Section where the item is sold")
    quantity: int = Field(..., ge=0, description="Number of items sold")
    total_sales: float = Field(..., ge=0, description="Total sales amount for the item")
    rrp: float = Field(None, ge=0, description="Recommended retail price")
    supplier: str = Field(None, description="Supplier of the item")
    date_of_sale: date = Field(..., description="Date when the sale occurred")
