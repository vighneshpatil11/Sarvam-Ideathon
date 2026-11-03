from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

# Standard Response Envelopes
class ErrorDetail(BaseModel):
    code: str = "ERROR"
    message: str
    details: Optional[Any] = None

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]] = None
    error: Optional[ErrorDetail] = None

    @classmethod
    def ok(cls, data: T, meta: Optional[Dict[str, Any]] = None) -> "ApiResponse[T]":
        return cls(success=True, data=data, meta=meta)

    @classmethod
    def fail(cls, code: str, message: str, details: Optional[Any] = None) -> "ApiResponse[None]":
        return cls(success=False, data=None, error=ErrorDetail(code=code, message=message, details=details))

# Health
class HealthData(BaseModel):
    status: str
    app: str
    version: str
    database: str

# Source Schema
class SourceOut(BaseModel):
    id: str
    title: str
    url: str
    publisher: str
    source_type: str
    supports: str
    last_checked_at: Optional[str] = None

# Service Schemas
class ServiceSummary(BaseModel):
    id: str
    slug: str
    name: str
    short_description: str
    department_name: str
    state: str
    districts: List[str]
    languages: List[str] = ["en", "hi", "mr"]
    verification_status: str
    is_demo: bool = False
    statutory_fee_inr: float
    processing_days: int
    last_verified_at: Optional[str] = None

class ServiceListResponse(BaseModel):
    items: List[ServiceSummary]
    total: int

class ServiceDetailOut(BaseModel):
    id: str
    slug: str
    name: str
    short_description: str
    description: str
    department_name: str
    department_code: str
    jurisdiction_level: str
    state: str
    districts: List[str]
    statutory_fee_inr: float
    processing_days: int
    official_portal_url: Optional[str] = None
    official_tracking_url: Optional[str] = None
    verification_status: str
    is_demo: bool = False
    last_verified_at: Optional[str] = None
    sources: List[SourceOut] = []

# Search Schemas
class SearchRequest(BaseModel):
    query: str
    language: str = "en"
    state: Optional[str] = "Maharashtra"
    district: Optional[str] = "Pune"

# Document Schemas
class DocumentOut(BaseModel):
    id: str
    name: str
    category: str
    is_mandatory: bool
    description: Optional[str] = None
    issuing_authority: Optional[str] = None
    display_order: int

class ServiceDocumentsResponse(BaseModel):
    service_slug: str
    service_name: str
    documents: List[DocumentOut]

# Application Steps Schemas
class StepOut(BaseModel):
    step_number: int
    title: str
    instructions: str
    external_url: Optional[str] = None

class ServiceStepsResponse(BaseModel):
    service_slug: str
    service_name: str
    official_portal_url: Optional[str] = None
    statutory_fee_inr: float
    processing_days: int
    steps: List[StepOut]

# Eligibility Schemas
class EligibilityQuestionOut(BaseModel):
    id: str
    field_key: str
    question_type: str
    label: str
    help_text: Optional[str] = None
    required: bool
    display_order: int
    validation: Optional[Dict[str, Any]] = None

class EligibilityQuestionsResponse(BaseModel):
    service_slug: str
    service_name: str
    questions: List[EligibilityQuestionOut]

class EligibilityEvaluationRequest(BaseModel):
    answers: Dict[str, Any]
    language: str = "en"

class RuleResultOut(BaseModel):
    rule_code: str
    description: str
    passed: bool
    failure_message: Optional[str] = None

class EligibilityEvaluationResponse(BaseModel):
    status: str  # potentially_eligible, potentially_not_eligible, more_information_required, unable_to_determine
    summary: str
    explanation: str
    missing_information: List[str] = []
    rule_results: List[RuleResultOut] = []
    sources: List[SourceOut] = []

# Assistant Schemas
class ChatHistoryMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class AssistantContext(BaseModel):
    service_slug: Optional[str] = None

class AssistantChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: str = "en"
    context: Optional[AssistantContext] = None
    history: Optional[List[ChatHistoryMessage]] = []

class AssistantChatResponse(BaseModel):
    session_id: str
    answer: str
    related_services: List[ServiceSummary] = []
    sources: List[SourceOut] = []
    warnings: List[str] = []
    provider: str = "sarvam"

# Feedback Schemas
class FeedbackCreate(BaseModel):
    service_id: Optional[str] = None
    category: str = "clarity"
    comments: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    language: str = "en"

class FeedbackOut(BaseModel):
    id: str
    category: str
    comments: str
    rating: Optional[int] = None
    language: str
    created_at: str

# Admin Auth & CRUD Schemas
class AdminLoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
