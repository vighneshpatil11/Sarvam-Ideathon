from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ApiResponse, SearchRequest, ServiceListResponse
from app.services.search_service import search_services

router = APIRouter(tags=["Search"])

@router.post("/search", response_model=ApiResponse[ServiceListResponse])
def search_endpoint(
    req: SearchRequest,
    db: Session = Depends(get_db)
):
    results = search_services(
        db=db,
        query=req.query,
        language=req.language,
        state=req.state,
        district=req.district
    )
    return ApiResponse.ok(ServiceListResponse(items=results, total=len(results)))
