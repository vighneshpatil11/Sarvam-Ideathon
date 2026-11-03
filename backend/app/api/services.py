from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service, Department, District
from app.schemas import ApiResponse, ServiceSummary, ServiceListResponse, ServiceDetailOut, SourceOut

router = APIRouter(prefix="/services", tags=["Services"])


def _static_service_list(language: str = "en") -> List[ServiceSummary]:
    """Return hardcoded service list directly from seed data — works even if SQLite is empty."""
    from app.seed import SUBMISSION_SERVICES
    items = []
    for s in SUBMISSION_SERVICES:
        name = s["name_mr"] if language == "mr" else s["name_en"]
        short_desc = s.get("short_description_mr") if language == "mr" else s.get("short_description_en", "")
        dept = s.get("dept_name_mr") if language == "mr" else s.get("dept_name_en", "Maharashtra Govt")
        items.append(ServiceSummary(
            id=s["slug"],
            slug=s["slug"],
            name=name or s["name_en"],
            short_description=short_desc or s.get("short_description_en", ""),
            department_name=dept or s.get("dept_name_en", "Maharashtra Govt"),
            state="Maharashtra",
            districts=["Pune", "All Districts"],
            languages=["en", "hi", "mr"],
            verification_status="verified",
            is_demo=False,
            statutory_fee_inr=s["statutory_fee_inr"],
            processing_days=s["processing_days"],
        ))
    return items

@router.get("", response_model=ApiResponse[ServiceListResponse])
def list_services(
    department_id: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Service).filter(Service.verification_status.in_(["verified", "draft"]))

    if department_id:
        query = query.filter(Service.department_id == department_id)
    if state:
        query = query.filter(Service.state.ilike(f"%{state}%"))

    services = query.all()

    # Vercel cold-start: DB is empty — serve static seed data directly
    if not services:
        items = _static_service_list(language)
        return ApiResponse.ok(ServiceListResponse(items=items, total=len(items)))

    items: List[ServiceSummary] = []
    for s in services:
        name = s.name_en
        short_desc = s.short_description_en
        dept_name = s.department.name_en if s.department else "Maharashtra Govt"

        if language == "hi":
            name = s.name_hi or name
            short_desc = s.short_description_hi or short_desc
            dept_name = s.department.name_hi if s.department and s.department.name_hi else dept_name
        elif language == "mr":
            name = s.name_mr or name
            short_desc = s.short_description_mr or short_desc
            dept_name = s.department.name_mr if s.department and s.department.name_mr else dept_name

        district_names = [d.name for d in s.districts] if s.districts else ["Pune", "All Districts"]

        items.append(
            ServiceSummary(
                id=s.id,
                slug=s.slug,
                name=name,
                short_description=short_desc,
                department_name=dept_name,
                state=s.state,
                districts=district_names,
                languages=["en", "hi", "mr"],
                verification_status=s.verification_status,
                is_demo=s.is_demo,
                statutory_fee_inr=s.statutory_fee_inr,
                processing_days=s.processing_days,
                last_verified_at=s.last_verified_at.strftime("%Y-%m-%d") if s.last_verified_at else None
            )
        )

    return ApiResponse.ok(ServiceListResponse(items=items, total=len(items)))


@router.get("/{slug}", response_model=ApiResponse[ServiceDetailOut])
def get_service_details(
    slug: str,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()

    # Vercel cold-start fallback: serve from static seed data
    if not service:
        from app.seed import SUBMISSION_SERVICES
        s = next((x for x in SUBMISSION_SERVICES if x["slug"] == slug), None)
        if not s:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with slug '{slug}' not found"
            )
        name = s["name_mr"] if language == "mr" else s["name_en"]
        desc = s.get("description_mr") if language == "mr" else s.get("description_en", "")
        short_desc = s.get("short_description_mr") if language == "mr" else s.get("short_description_en", "")
        dept = s.get("dept_name_mr") if language == "mr" else s.get("dept_name_en", "Maharashtra Govt")
        detail = ServiceDetailOut(
            id=s["slug"], slug=s["slug"],
            name=name or s["name_en"],
            short_description=short_desc or "",
            description=desc or "",
            department_name=dept or "Maharashtra Govt",
            department_code=s.get("dept_code", "REV_DEPT"),
            jurisdiction_level="state",
            state="Maharashtra",
            districts=["Pune", "All Districts"],
            statutory_fee_inr=s["statutory_fee_inr"],
            processing_days=s["processing_days"],
            official_portal_url=s.get("source_url", "https://aaplesarkar.mahaonline.gov.in"),
            official_tracking_url="https://aaplesarkar.mahaonline.gov.in/en/TrackStatus",
            verification_status="verified",
            is_demo=False,
            sources=[]
        )
        return ApiResponse.ok(detail)

    name = service.name_en
    short_desc = service.short_description_en
    desc = service.description_en
    dept_name = service.department.name_en if service.department else "Maharashtra Govt"
    dept_code = service.department.code if service.department else "REV"

    if language == "hi":
        name = service.name_hi or name
        short_desc = service.short_description_hi or short_desc
        desc = service.description_hi or desc
        dept_name = service.department.name_hi if service.department and service.department.name_hi else dept_name
    elif language == "mr":
        name = service.name_mr or name
        short_desc = service.short_description_mr or short_desc
        desc = service.description_mr or desc
        dept_name = service.department.name_mr if service.department and service.department.name_mr else dept_name

    district_names = [d.name for d in service.districts] if service.districts else ["Pune"]

    sources_out = [
        SourceOut(
            id=src.id,
            title=src.title,
            url=src.url,
            publisher=src.publisher,
            source_type=src.source_type,
            supports=src.supports,
            last_checked_at=src.last_checked_at.strftime("%Y-%m-%d") if src.last_checked_at else None
        ) for src in service.sources
    ]

    detail = ServiceDetailOut(
        id=service.id,
        slug=service.slug,
        name=name,
        short_description=short_desc,
        description=desc,
        department_name=dept_name,
        department_code=dept_code,
        jurisdiction_level=service.jurisdiction_level,
        state=service.state,
        districts=district_names,
        statutory_fee_inr=service.statutory_fee_inr,
        processing_days=service.processing_days,
        official_portal_url=service.official_portal_url,
        official_tracking_url=service.official_tracking_url,
        verification_status=service.verification_status,
        is_demo=service.is_demo,
        last_verified_at=service.last_verified_at.strftime("%Y-%m-%d") if service.last_verified_at else None,
        sources=sources_out
    )

    return ApiResponse.ok(detail)
