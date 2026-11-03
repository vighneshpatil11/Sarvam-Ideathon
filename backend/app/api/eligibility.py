import json
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service, EligibilityQuestion
from app.schemas import (
    ApiResponse,
    EligibilityQuestionsResponse,
    EligibilityQuestionOut,
    EligibilityEvaluationRequest,
    EligibilityEvaluationResponse
)
from app.eligibility.evaluator import evaluate_service_eligibility

router = APIRouter(prefix="/services", tags=["Eligibility"])

@router.get("/{slug}/eligibility/questions", response_model=ApiResponse[EligibilityQuestionsResponse])
def get_eligibility_questions(
    slug: str,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with slug '{slug}' not found"
        )

    service_name = service.name_en
    if language == "hi" and service.name_hi:
        service_name = service.name_hi
    elif language == "mr" and service.name_mr:
        service_name = service.name_mr

    questions_out = []
    for q in service.eligibility_questions:
        label = q.label_en
        help_text = q.help_text_en

        if language == "hi":
            label = q.label_hi or label
            help_text = q.help_text_hi or help_text
        elif language == "mr":
            label = q.label_mr or label
            help_text = q.help_text_mr or help_text

        validation_data = None
        if q.validation_json:
            try:
                validation_data = json.loads(q.validation_json)
            except Exception:
                validation_data = None

        questions_out.append(
            EligibilityQuestionOut(
                id=q.id,
                field_key=q.field_key,
                question_type=q.question_type,
                label=label,
                help_text=help_text,
                required=q.required,
                display_order=q.display_order,
                validation=validation_data
            )
        )

    questions_out.sort(key=lambda x: x.display_order)

    return ApiResponse.ok(
        EligibilityQuestionsResponse(
            service_slug=service.slug,
            service_name=service_name,
            questions=questions_out
        )
    )


@router.post("/{slug}/eligibility/evaluate", response_model=ApiResponse[EligibilityEvaluationResponse])
def evaluate_eligibility(
    slug: str,
    req: EligibilityEvaluationRequest,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with slug '{slug}' not found"
        )

    result = evaluate_service_eligibility(
        service=service,
        answers=req.answers,
        language=req.language
    )
    return ApiResponse.ok(result)
