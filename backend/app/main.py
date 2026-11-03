from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.schemas import ApiResponse
from app.models import AdminUser
from app.security.auth import get_password_hash

# Import API routers
from app.api.health import router as health_router
from app.api.services import router as services_router
from app.api.search import router as search_router
from app.api.documents import router as documents_router
from app.api.eligibility import router as eligibility_router
from app.api.steps import router as steps_router
from app.api.assistant import router as assistant_router
from app.api.feedback import router as feedback_router
from app.api.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist & admin user is bootstrapped
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_admin = db.query(AdminUser).filter(AdminUser.email == settings.ADMIN_BOOTSTRAP_EMAIL).first()
        if not existing_admin:
            admin = AdminUser(
                email=settings.ADMIN_BOOTSTRAP_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_BOOTSTRAP_PASSWORD),
                full_name="SAARTHI Administrator",
                role="superadmin",
                is_active=True
            )
            db.add(admin)
            db.commit()

        # Seed core Maharashtra submission services if DB is uninitialized
        from app.seed import seed_if_empty
        seed_if_empty(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Multilingual Government Service Navigation Platform for Maharashtra",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
is_wildcard = "*" in settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=not is_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Error Handlers to guarantee API Envelope Contract
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse.fail(
            code="VALIDATION_ERROR",
            message="Request parameter validation failed.",
            details=exc.errors()
        ).model_dump()
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse.fail(
            code=f"HTTP_{exc.status_code}",
            message=exc.detail if isinstance(exc.detail, str) else "An HTTP error occurred."
        ).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse.fail(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected server error occurred."
        ).model_dump()
    )

# Mount API Routers under /api/v1
api_prefix = settings.API_V1_PREFIX
app.include_router(health_router, prefix=api_prefix)
app.include_router(services_router, prefix=api_prefix)
app.include_router(search_router, prefix=api_prefix)
app.include_router(documents_router, prefix=api_prefix)
app.include_router(eligibility_router, prefix=api_prefix)
app.include_router(steps_router, prefix=api_prefix)
app.include_router(assistant_router, prefix=api_prefix)
app.include_router(feedback_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)
