from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service, ServiceDocument
from app.schemas import ApiResponse, ServiceDocumentsResponse, DocumentOut

router = APIRouter(prefix="/services", tags=["Documents"])

@router.get("/{slug}/documents", response_model=ApiResponse[ServiceDocumentsResponse])
def get_service_documents(
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

    docs = []
    for d in service.documents:
        name = d.name_en
        desc = d.description_en

        if language == "hi":
            name = d.name_hi or name
            desc = d.description_hi or desc
        elif language == "mr":
            name = d.name_mr or name
            desc = d.description_mr or desc

        docs.append(
            DocumentOut(
                id=d.id,
                name=name,
                category=d.category,
                is_mandatory=d.is_mandatory,
                description=desc,
                issuing_authority=d.issuing_authority,
                display_order=d.display_order
            )
        )

    docs.sort(key=lambda x: (not x.is_mandatory, x.display_order))

    response_data = ServiceDocumentsResponse(
        service_slug=service.slug,
        service_name=service_name,
        documents=docs
    )
    return ApiResponse.ok(response_data)
