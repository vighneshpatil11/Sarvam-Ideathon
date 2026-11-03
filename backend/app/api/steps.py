from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service, ApplicationStep
from app.schemas import ApiResponse, ServiceStepsResponse, StepOut

router = APIRouter(prefix="/services", tags=["Application Steps"])

@router.get("/{slug}/steps", response_model=ApiResponse[ServiceStepsResponse])
def get_service_steps(
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

    steps_out = []
    for step in service.application_steps:
        title = step.title_en
        instructions = step.instructions_en

        if language == "hi":
            title = step.title_hi or title
            instructions = step.instructions_hi or instructions
        elif language == "mr":
            title = step.title_mr or title
            instructions = step.instructions_mr or instructions

        steps_out.append(
            StepOut(
                step_number=step.step_number,
                title=title,
                instructions=instructions,
                external_url=step.external_url or service.official_portal_url
            )
        )

    steps_out.sort(key=lambda x: x.step_number)

    return ApiResponse.ok(
        ServiceStepsResponse(
            service_slug=service.slug,
            service_name=service_name,
            official_portal_url=service.official_portal_url,
            statutory_fee_inr=service.statutory_fee_inr,
            processing_days=service.processing_days,
            steps=steps_out
        )
    )
