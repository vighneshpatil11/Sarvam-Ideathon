import uuid
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ApiResponse, AssistantChatRequest, AssistantChatResponse, ServiceSummary
from app.knowledge.retriever import retrieve_grounded_context
from app.prompts.assistant_prompts import build_assistant_system_prompt
from app.ai.factory import get_ai_provider

logger = logging.getLogger("saarthi.assistant")
router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.post("/chat", response_model=ApiResponse[AssistantChatResponse])
async def assistant_chat(
    req: AssistantChatRequest,
    db: Session = Depends(get_db)
):
    session_id = req.session_id or str(uuid.uuid4())
    service_slug = req.context.service_slug if req.context else None

    # Step 1: Grounded Context Retrieval
    service_facts, chunks, sources, related_services_models = retrieve_grounded_context(
        db=db,
        query=req.message,
        service_slug=service_slug,
        language=req.language
    )

    # Step 2: System prompt construction
    system_prompt = build_assistant_system_prompt(
        context_chunks=chunks,
        service_facts=service_facts,
        language=req.language
    )

    # Step 3: AI Provider invocation
    provider = get_ai_provider()
    provider_name = provider.get_provider_name()
    warnings = []

    # Build message list: history (last 6 turns) + current user message
    MAX_HISTORY = 6
    history = req.history or []
    history_messages = [
        {"role": m.role, "content": m.content}
        for m in history[-MAX_HISTORY:]
    ]
    history_messages.append({"role": "user", "content": req.message})

    try:
        answer = await provider.generate_response(
            messages=history_messages,
            system_prompt=system_prompt,
            language=req.language
        )
    except Exception as e:
        logger.error(f"Provider {provider_name} failed: {e}. Utilizing fallback.")
        warnings.append(f"Primary provider experienced a temporary error. Provided response is from local verified knowledge.")
        from app.ai.local_fallback import LocalFallbackProvider
        fallback = LocalFallbackProvider()
        provider_name = fallback.get_provider_name()
        answer = await fallback.generate_response(
            messages=history_messages,
            system_prompt=system_prompt,
            language=req.language
        )

    # Map related services
    related_services_out = []
    for s in related_services_models[:3]:
        name = s.name_en
        short_desc = s.short_description_en
        if req.language == "hi":
            name = s.name_hi or name
            short_desc = s.short_description_hi or short_desc
        elif req.language == "mr":
            name = s.name_mr or name
            short_desc = s.short_description_mr or short_desc

        related_services_out.append(
            ServiceSummary(
                id=s.id,
                slug=s.slug,
                name=name,
                short_description=short_desc,
                department_name=s.department.name_en if s.department else "Maharashtra Govt",
                state=s.state,
                districts=[d.name for d in s.districts] if s.districts else ["Pune"],
                languages=["en", "hi", "mr"],
                verification_status=s.verification_status,
                is_demo=s.is_demo,
                statutory_fee_inr=s.statutory_fee_inr,
                processing_days=s.processing_days,
                last_verified_at=s.last_verified_at.strftime("%Y-%m-%d") if s.last_verified_at else None
            )
        )

    response_data = AssistantChatResponse(
        session_id=session_id,
        answer=answer,
        related_services=related_services_out,
        sources=sources,
        warnings=warnings,
        provider=provider_name
    )
    return ApiResponse.ok(response_data)
