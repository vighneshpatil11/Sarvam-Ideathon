from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AdminUser, AdminAuditLog, Service, Source, Feedback
from app.schemas import ApiResponse, AdminLoginRequest, TokenResponse
from app.security.auth import verify_password, create_access_token, get_current_admin
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/auth/login", response_model=ApiResponse[TokenResponse])
def admin_login(
    req: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(AdminUser).filter(AdminUser.email == req.email).first()
    if not admin or not verify_password(req.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )

    token = create_access_token(data={"sub": admin.email, "role": admin.role})
    return ApiResponse.ok(
        TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )

@router.get("/services", response_model=ApiResponse[List[dict]])
def list_admin_services(
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    services = db.query(Service).all()
    results = [
        {
            "id": s.id,
            "slug": s.slug,
            "name_en": s.name_en,
            "department": s.department.name_en if s.department else "N/A",
            "verification_status": s.verification_status,
            "is_demo": s.is_demo,
            "last_verified_at": s.last_verified_at.isoformat() if s.last_verified_at else None,
            "documents_count": len(s.documents),
            "rules_count": len(s.eligibility_rules)
        } for s in services
    ]
    return ApiResponse.ok(results)

@router.post("/services/{service_id}/publish", response_model=ApiResponse[dict])
def publish_service(
    service_id: str,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.verification_status = "verified"
    service.last_verified_at = datetime.now(timezone.utc)

    audit = AdminAuditLog(
        admin_id=admin.id,
        action="PUBLISH_SERVICE",
        target_entity="Service",
        target_id=service.id,
        details=f"Service '{service.slug}' published by {admin.email}"
    )
    db.add(audit)
    db.commit()

    return ApiResponse.ok({
        "id": service.id,
        "slug": service.slug,
        "verification_status": service.verification_status,
        "published_at": service.last_verified_at.isoformat()
    })

@router.get("/feedback", response_model=ApiResponse[List[dict]])
def get_admin_feedback(
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(100).all()
    return ApiResponse.ok([
        {
            "id": f.id,
            "service_id": f.service_id,
            "category": f.category,
            "comments": f.comments,
            "rating": f.rating,
            "created_at": f.created_at.isoformat()
        } for f in feedbacks
    ])

@router.get("/audit-logs", response_model=ApiResponse[List[dict]])
def get_audit_logs(
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    logs = db.query(AdminAuditLog).order_by(AdminAuditLog.created_at.desc()).limit(50).all()
    return ApiResponse.ok([
        {
            "id": l.id,
            "admin_id": l.admin_id,
            "action": l.action,
            "target_entity": l.target_entity,
            "target_id": l.target_id,
            "details": l.details,
            "created_at": l.created_at.isoformat()
        } for l in logs
    ])
