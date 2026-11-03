import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, Table, Enum
)
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def get_utc_now():
    return datetime.now(timezone.utc)

# Many-to-Many Associations
service_districts = Table(
    "service_districts",
    Base.metadata,
    Column("service_id", String(36), ForeignKey("services.id"), primary_key=True),
    Column("district_id", String(36), ForeignKey("districts.id"), primary_key=True)
)

service_sources = Table(
    "service_sources",
    Base.metadata,
    Column("service_id", String(36), ForeignKey("services.id"), primary_key=True),
    Column("source_id", String(36), ForeignKey("sources.id"), primary_key=True)
)

# Geographic Entities
class State(Base):
    __tablename__ = "states"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    districts = relationship("District", back_populates="state", cascade="all, delete-orphan")


class District(Base):
    __tablename__ = "districts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    state_id = Column(String(36), ForeignKey("states.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    state = relationship("State", back_populates="districts")
    services = relationship("Service", secondary=service_districts, back_populates="districts")


class Department(Base):
    __tablename__ = "departments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name_en = Column(String(200), nullable=False)
    name_hi = Column(String(200), nullable=True)
    name_mr = Column(String(200), nullable=True)
    code = Column(String(50), unique=True, nullable=False)
    portal_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    services = relationship("Service", back_populates="department")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(300), nullable=False)
    url = Column(String(1000), nullable=False)
    publisher = Column(String(200), nullable=False)
    source_type = Column(String(50), default="official")  # official, gazette, citizen_charter
    supports = Column(String(500), default="service_guidance")  # document_requirements, eligibility_rules, fees
    last_checked_at = Column(DateTime(timezone=True), default=get_utc_now)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    services = relationship("Service", secondary=service_sources, back_populates="sources")
    chunks = relationship("KnowledgeChunk", back_populates="source", cascade="all, delete-orphan")


class Service(Base):
    __tablename__ = "services"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    name_en = Column(String(250), nullable=False)
    name_hi = Column(String(250), nullable=True)
    name_mr = Column(String(250), nullable=True)
    short_description_en = Column(Text, nullable=False)
    short_description_hi = Column(Text, nullable=True)
    short_description_mr = Column(Text, nullable=True)
    description_en = Column(Text, nullable=False)
    description_hi = Column(Text, nullable=True)
    description_mr = Column(Text, nullable=True)
    
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    jurisdiction_level = Column(String(50), default="state")  # state, district, central
    state = Column(String(100), default="Maharashtra")
    
    # Statutory values
    statutory_fee_inr = Column(Float, default=0.0)
    processing_days = Column(Integer, default=15)
    official_portal_url = Column(String(500), nullable=True)
    official_tracking_url = Column(String(500), nullable=True)
    
    # Governance status
    verification_status = Column(String(50), default="verified")  # verified, draft, needs_review, expired, disputed
    is_demo = Column(Boolean, default=False)
    last_verified_at = Column(DateTime(timezone=True), default=get_utc_now)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    department = relationship("Department", back_populates="services")
    districts = relationship("District", secondary=service_districts, back_populates="services")
    sources = relationship("Source", secondary=service_sources, back_populates="services")
    documents = relationship("ServiceDocument", back_populates="service", cascade="all, delete-orphan")
    application_steps = relationship("ApplicationStep", back_populates="service", order_by="ApplicationStep.step_number", cascade="all, delete-orphan")
    eligibility_questions = relationship("EligibilityQuestion", back_populates="service", order_by="EligibilityQuestion.display_order", cascade="all, delete-orphan")
    eligibility_rules = relationship("EligibilityRule", back_populates="service", cascade="all, delete-orphan")
    knowledge_chunks = relationship("KnowledgeChunk", back_populates="service", cascade="all, delete-orphan")


class ServiceDocument(Base):
    __tablename__ = "service_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    name_en = Column(String(200), nullable=False)
    name_hi = Column(String(200), nullable=True)
    name_mr = Column(String(200), nullable=True)
    category = Column(String(100), default="identity_proof")  # identity_proof, address_proof, income_proof, other
    is_mandatory = Column(Boolean, default=True)
    description_en = Column(Text, nullable=True)
    description_hi = Column(Text, nullable=True)
    description_mr = Column(Text, nullable=True)
    issuing_authority = Column(String(200), nullable=True)
    display_order = Column(Integer, default=1)

    service = relationship("Service", back_populates="documents")


class ApplicationStep(Base):
    __tablename__ = "application_steps"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title_en = Column(String(250), nullable=False)
    title_hi = Column(String(250), nullable=True)
    title_mr = Column(String(250), nullable=True)
    instructions_en = Column(Text, nullable=False)
    instructions_hi = Column(Text, nullable=True)
    instructions_mr = Column(Text, nullable=True)
    external_url = Column(String(500), nullable=True)

    service = relationship("Service", back_populates="application_steps")


class EligibilityQuestion(Base):
    __tablename__ = "eligibility_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    field_key = Column(String(100), nullable=False)  # e.g., is_maharashtra_resident, annual_family_income
    question_type = Column(String(50), default="boolean")  # boolean, number, single_choice, text
    label_en = Column(Text, nullable=False)
    label_hi = Column(Text, nullable=True)
    label_mr = Column(Text, nullable=True)
    help_text_en = Column(Text, nullable=True)
    help_text_hi = Column(Text, nullable=True)
    help_text_mr = Column(Text, nullable=True)
    required = Column(Boolean, default=True)
    display_order = Column(Integer, default=1)
    validation_json = Column(Text, nullable=True)  # JSON string for min, max, options

    service = relationship("Service", back_populates="eligibility_questions")


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    rule_code = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    field_key = Column(String(100), nullable=False)
    operator = Column(String(50), nullable=False)  # eq, ne, gt, lt, gte, lte, in
    expected_value = Column(String(200), nullable=False)  # Stringified value for comparison
    is_disqualifying = Column(Boolean, default=True)
    failure_message_en = Column(Text, nullable=False)
    failure_message_hi = Column(Text, nullable=True)
    failure_message_mr = Column(Text, nullable=True)

    service = relationship("Service", back_populates="eligibility_rules")


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=True)
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False)
    content_en = Column(Text, nullable=False)
    content_hi = Column(Text, nullable=True)
    content_mr = Column(Text, nullable=True)
    section_title = Column(String(250), nullable=True)
    keywords = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    service = relationship("Service", back_populates="knowledge_chunks")
    source = relationship("Source", back_populates="chunks")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=True)
    category = Column(String(50), default="clarity")  # clarity, incorrect_info, portal_broken, other
    comments = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    language = Column(String(10), default="en")
    is_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), default="admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    admin_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # CREATE_SERVICE, PUBLISH_SERVICE, UPDATE_RULES
    target_entity = Column(String(100), nullable=False)
    target_id = Column(String(36), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
