from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.models import Service, KnowledgeChunk, Source
from app.schemas import SourceOut

SERVICE_KEYWORD_MAP = {
    # 1. Income
    "उत्पन्न": "income-certificate",
    "income": "income-certificate",
    # 2. Caste
    "जात": "caste-certificate",
    "caste": "caste-certificate",
    # 3. Non-Creamy Layer
    "नॉन-क्रीमी": "non-creamy-layer-certificate",
    "क्रीमी": "non-creamy-layer-certificate",
    "non-creamy": "non-creamy-layer-certificate",
    "ncl": "non-creamy-layer-certificate",
    # 4 & 5. Domicile & Age/Nationality
    "अधिवास": "domicile-certificate",
    "domicile": "domicile-certificate",
    "वय, राष्ट्रीयत्व": "age-nationality-and-domicile-certificate",
    "nationality": "nationality-certificate",
    "राष्ट्रीयत्व": "nationality-certificate",
    # 6 & 26. Birth & Duplicate Birth
    "दुय्यम जन्म": "duplicate-birth-certificate",
    "duplicate birth": "duplicate-birth-certificate",
    "जन्म": "birth-certificate",
    "birth": "birth-certificate",
    # 7 & 27. Death & Duplicate Death
    "दुय्यम मृत्यू": "duplicate-death-certificate",
    "duplicate death": "duplicate-death-certificate",
    "मृत्यू": "death-certificate",
    "death": "death-certificate",
    # 8. Marriage
    "विवाह": "marriage-certificate",
    "लग्न": "marriage-certificate",
    "marriage": "marriage-certificate",
    # 9. Senior Citizen
    "ज्येष्ठ": "senior-citizen-certificate",
    "senior": "senior-citizen-certificate",
    # 10. Disability
    "दिव्यांग": "disability-certificate",
    "अपंग": "disability-certificate",
    "disability": "disability-certificate",
    "udid": "disability-certificate",
    # 11 & 22. Residence & Temporary Residence
    "तात्पुरता": "temporary-residence-certificate",
    "temporary": "temporary-residence-certificate",
    "रहिवासी": "residence-certificate",
    "residence": "residence-certificate",
    # 12. Character / Police Clearance
    "चारित्र्य": "character-certificate",
    "पोलीस": "character-certificate",
    "character": "character-certificate",
    "pcc": "character-certificate",
    # 13. Solvency
    "ऐपत": "solvency-certificate",
    "सधनता": "solvency-certificate",
    "solvency": "solvency-certificate",
    # 14 & 23. Agriculturist & Small Landholder
    "अल्पभूधारक": "small-landholder-certificate",
    "small land": "small-landholder-certificate",
    "शेतकरी": "agriculturist-certificate",
    "farmer": "agriculturist-certificate",
    "agriculturist": "agriculturist-certificate",
    # 15. Landless
    "भूमिहीन": "landless-labourer-certificate",
    "landless": "landless-labourer-certificate",
    # 16. BPL
    "bpl": "bpl-certificate",
    "दारिद्र्य": "bpl-certificate",
    "poverty": "bpl-certificate",
    # 17, 18, 19, 20. Ration Card variants
    "पत्ता बदल": "ration-card-address-change",
    "address change": "ration-card-address-change",
    "नाव कमी": "ration-card-name-deletion",
    "name deletion": "ration-card-name-deletion",
    "नाव समाविष्ट": "ration-card-name-addition",
    "नाव जोडणे": "ration-card-name-addition",
    "name addition": "ration-card-name-addition",
    "नवीन रेशन": "ration-card-new-application",
    "रेशन": "ration-card-new-application",
    "शिधापत्रिका": "ration-card-new-application",
    "ration": "ration-card-new-application",
    # 21. Shop & Est
    "गुमास्ता": "shop-and-establishment-registration",
    "gumasta": "shop-and-establishment-registration",
    "shop": "shop-and-establishment-registration",
    # 24. Widow
    "विधवा": "widow-certificate",
    "widow": "widow-certificate",
    # 25. Legal Heir / Varas
    "वारस": "legal-heir-certificate",
    "varas": "legal-heir-certificate",
    "legal heir": "legal-heir-certificate",
    # 29. Tree Cutting
    "झाडे": "permission-for-tree-cutting",
    "वृक्षतोड": "permission-for-tree-cutting",
    "tree": "permission-for-tree-cutting",
    # 30. Land Record 7/12 & 8-A
    "७/१२": "land-record-certified-copy",
    "7/12": "land-record-certified-copy",
    "सातबारा": "land-record-certified-copy",
    "satbara": "land-record-certified-copy",
    "फेरफार": "land-record-certified-copy",
    "land record": "land-record-certified-copy",
}

def retrieve_grounded_context(
    db: Session,
    query: str,
    service_slug: Optional[str] = None,
    language: str = "en"
) -> Tuple[str, str, List[SourceOut], List[Service]]:
    clean_query = query.lower()
    sources_dict = {}
    related_services: List[Service] = []

    target_service: Optional[Service] = None
    if service_slug:
        target_service = db.query(Service).filter(Service.slug == service_slug).first()

    if not target_service:
        for kw, slug in SERVICE_KEYWORD_MAP.items():
            if kw in clean_query:
                target_service = db.query(Service).filter(Service.slug == slug).first()
                if target_service:
                    break

    if not target_service:
        all_services = db.query(Service).filter(Service.verification_status.in_(["verified", "draft"])).all()
        for s in all_services:
            if (s.slug and s.slug in clean_query) or \
               (s.name_en and s.name_en.lower() in clean_query) or \
               (s.name_mr and s.name_mr in clean_query):
                target_service = s
                break

    service_facts_lines = []
    if target_service:
        related_services.append(target_service)
        for src in target_service.sources:
            sources_dict[src.id] = SourceOut(
                id=src.id,
                title=src.title,
                url=src.url,
                publisher=src.publisher,
                source_type=src.source_type,
                supports=src.supports,
                last_checked_at=src.last_checked_at.isoformat() if src.last_checked_at else None
            )

        name = target_service.name_mr if (language == "mr" and target_service.name_mr) else target_service.name_en
        dept = target_service.department.name_mr if (language == "mr" and target_service.department and target_service.department.name_mr) else (target_service.department.name_en if target_service.department else "Maharashtra Govt")

        service_facts_lines.append(f"Service: {name}")
        service_facts_lines.append(f"Department: {dept}")
        service_facts_lines.append(f"Statutory Processing Time (RTS Act): {target_service.processing_days} working days")
        service_facts_lines.append(f"Official Statutory Fee: ₹{target_service.statutory_fee_inr:.2f}")
        if target_service.official_portal_url:
            service_facts_lines.append(f"Official Application Portal: {target_service.official_portal_url}")

        docs = []
        for d in target_service.documents:
            if d.is_mandatory:
                dname = d.name_mr if (language == "mr" and d.name_mr) else d.name_en
                docs.append(dname)
        if docs:
            service_facts_lines.append(f"Mandatory Documents Required: {', '.join(docs)}")

        steps = []
        for st in target_service.application_steps:
            stitle = st.title_mr if (language == "mr" and st.title_mr) else st.title_en
            sinst = st.instructions_mr if (language == "mr" and st.instructions_mr) else st.instructions_en
            steps.append(f"Step {st.step_number}: {stitle} - {sinst}")
        if steps:
            service_facts_lines.append("Application Steps:\n" + "\n".join(steps))

    service_facts_str = "\n".join(service_facts_lines)

    chunks_query = db.query(KnowledgeChunk)
    if target_service:
        chunks_query = chunks_query.filter(KnowledgeChunk.service_id == target_service.id)

    chunks: List[KnowledgeChunk] = chunks_query.limit(5).all()

    chunk_texts = []
    for c in chunks:
        content = c.content_mr if (language == "mr" and c.content_mr) else (c.content_hi if language == "hi" and c.content_hi else c.content_en)
        chunk_texts.append(f"[{c.section_title or 'Fact'}]: {content}")

        if c.source and c.source.id not in sources_dict:
            sources_dict[c.source.id] = SourceOut(
                id=c.source.id,
                title=c.source.title,
                url=c.source.url,
                publisher=c.source.publisher,
                source_type=c.source.source_type,
                supports=c.source.supports,
                last_checked_at=c.source.last_checked_at.isoformat() if c.source.last_checked_at else None
            )

    chunks_str = "\n".join(chunk_texts)
    sources_list = list(sources_dict.values())

    return service_facts_str, chunks_str, sources_list, related_services
