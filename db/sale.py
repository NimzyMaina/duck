from db.base import Base
from sqlalchemy import Column, Integer, String, Float, Date

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String)
    item_code = Column(Integer)
    item_barcode = Column(Integer)
    description = Column(String)
    category = Column(String)
    department = Column(String)
    sub_department = Column(String)
    section = Column(String)
    quantity = Column(Integer)
    total_sales = Column(Float)
    rrp = Column(Float)
    supplier = Column(String)
    date_of_sale = Column(Date)


