from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas import ApiResponse, HealthData

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=ApiResponse[HealthData])
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    data = HealthData(
        status="ok" if "error" not in db_status else "degraded",
        app="SAARTHI",
        version="1.0.0",
        database=db_status
    )
    return ApiResponse.ok(data)
