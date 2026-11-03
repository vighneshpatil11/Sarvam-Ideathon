from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Feedback
from app.schemas import ApiResponse, FeedbackCreate, FeedbackOut

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=ApiResponse[FeedbackOut], status_code=status.HTTP_201_CREATED)
def submit_feedback(
    fb: FeedbackCreate,
    db: Session = Depends(get_db)
):
    entry = Feedback(
        service_id=fb.service_id,
        category=fb.category,
        comments=fb.comments,
        rating=fb.rating,
        language=fb.language
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    out = FeedbackOut(
        id=entry.id,
        category=entry.category,
        comments=entry.comments,
        rating=entry.rating,
        language=entry.language,
        created_at=entry.created_at.isoformat()
    )
    return ApiResponse.ok(out)
