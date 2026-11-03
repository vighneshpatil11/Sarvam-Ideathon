from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models import Service, Department, District
from app.schemas import ServiceSummary

def search_services(
    db: Session,
    query: str,
    language: str = "en",
    state: Optional[str] = None,
    district: Optional[str] = None
) -> List[ServiceSummary]:
    clean_query = query.strip().lower()
    terms = [term for term in clean_query.split() if len(term) > 2]
    
    # Query only verified or draft/demo services
    base_query = db.query(Service).filter(Service.verification_status.in_(["verified", "draft"]))

    if state:
        base_query = base_query.filter(Service.state.ilike(f"%{state}%"))

    services: List[Service] = base_query.all()

    # Vercel cold-start: DB is empty — search directly in static seed data
    if not services:
        from app.seed import SUBMISSION_SERVICES
        results = []
        for s in SUBMISSION_SERVICES:
            name = s["name_mr"] if language == "mr" else s["name_en"]
            short_desc = s.get("short_description_mr") if language == "mr" else s.get("short_description_en", "")
            dept = s.get("dept_name_mr") if language == "mr" else s.get("dept_name_en", "Maharashtra Govt")
            # Simple keyword match across both languages
            haystack = f"{s['name_en']} {s.get('name_mr','')} {s.get('short_description_en','')} {s.get('short_description_mr','')}".lower()
            if not clean_query or any(t in haystack for t in ([clean_query] + terms)):
                results.append(ServiceSummary(
                    id=s["slug"], slug=s["slug"],
                    name=name or s["name_en"],
                    short_description=short_desc or "",
                    department_name=dept or "Maharashtra Govt",
                    state="Maharashtra", districts=["Pune", "All Districts"],
                    languages=["en", "hi", "mr"], verification_status="verified", is_demo=False,
                    statutory_fee_inr=s["statutory_fee_inr"], processing_days=s["processing_days"],
                ))
        return results

    scored_services = []

    for s in services:
        score = 0
        
        # Exact slug match
        if clean_query == s.slug.lower():
            score += 100
        
        # Name matches in all languages
        name_en = (s.name_en or "").lower()
        name_hi = (s.name_hi or "").lower()
        name_mr = (s.name_mr or "").lower()

        if clean_query in name_en:
            score += 50
        if clean_query in name_hi or clean_query in name_mr:
            score += 50

        # Term matches
        for term in terms:
            if term in name_en or term in name_hi or term in name_mr:
                score += 20
            if s.description_en and term in s.description_en.lower():
                score += 5
            if s.short_description_en and term in s.short_description_en.lower():
                score += 10
            if s.department and term in s.department.name_en.lower():
                score += 15

        # Domain keywords mapping
        keywords_map = {
            "income": ["income-certificate"],
            "उत्पन्न": ["income-certificate"],
            "आय": ["income-certificate"],
            "domicile": ["domicile-certificate"],
            "रहिवासी": ["domicile-certificate"],
            "निवास": ["domicile-certificate"],
            "caste": ["caste-certificate"],
            "जात": ["caste-certificate"],
            "जाति": ["caste-certificate"],
            "creamy": ["non-creamy-layer-certificate"],
            "नॉन-क्रीमी": ["non-creamy-layer-certificate"],
            "scholarship": ["mahadbt-post-matric-scholarship"],
            "शिष्यवृत्ती": ["mahadbt-post-matric-scholarship"],
            "छात्रवृत्ति": ["mahadbt-post-matric-scholarship"],
            "certificate": ["income-certificate", "domicile-certificate", "caste-certificate"],
            "प्रमाणपत्र": ["income-certificate", "domicile-certificate", "caste-certificate"],
            "दाखला": ["income-certificate", "domicile-certificate", "caste-certificate"]
        }

        for kw, matching_slugs in keywords_map.items():
            if kw in clean_query and s.slug in matching_slugs:
                score += 25

        if score > 0 or not clean_query:
            scored_services.append((score, s))

    # Sort descending by score
    scored_services.sort(key=lambda x: x[0], reverse=True)

    results: List[ServiceSummary] = []
    for _, s in scored_services:
        # Determine language specific fields
        name = s.name_en
        short_desc = s.short_description_en
        dept_name = s.department.name_en if s.department else "Government of Maharashtra"

        if language == "hi":
            if s.name_hi:
                name = s.name_hi
            if s.short_description_hi:
                short_desc = s.short_description_hi
            if s.department and s.department.name_hi:
                dept_name = s.department.name_hi
        elif language == "mr":
            if s.name_mr:
                name = s.name_mr
            if s.short_description_mr:
                short_desc = s.short_description_mr
            if s.department and s.department.name_mr:
                dept_name = s.department.name_mr

        district_names = [d.name for d in s.districts] if s.districts else ["Pune", "All Districts"]

        results.append(
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

    return results
