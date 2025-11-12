from fastapi import FastAPI
from db.client import Session
from db.sale import Sale
from sqlalchemy import func, case

app = FastAPI(title="Duck Data Quality API")
@app.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}

@app.get("/api/v1/quality")
def quality():
    with Session() as db:
        results = (
            db.query(
                Sale.store_name,
                (
                        func.sum(
                            case((Sale.validation_passed == True, 1), else_=0)
                        )
                        * 100.0
                        / func.count()
                ).label("quality_percentage")
            )
            .group_by(Sale.store_name)
            .all()
        )
        return {
            "success": True,
            "message": "Success",
            "data":  [
                {
                    "store_name": row.store_name,
                    "quality_percentage": round(float(row.quality_percentage), 2)
                }
                for row in results
            ]
        }

