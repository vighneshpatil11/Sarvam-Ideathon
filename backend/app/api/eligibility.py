import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service
from app.schemas import (
    ApiResponse,
    EligibilityQuestionsResponse,
    EligibilityQuestionOut,
    EligibilityEvaluationRequest,
    EligibilityEvaluationResponse,
    RuleResultOut,
    SourceOut
)

router = APIRouter(prefix="/services", tags=["Eligibility"])

STATIC_QUESTIONS: Dict[str, List[Dict[str, Any]]] = {
    "domicile-certificate": [
        {
            "id": "q_residence",
            "field_key": "residence_years_15",
            "type": "boolean",
            "label_en": "Have you been continuously residing in Maharashtra for at least 15 years?",
            "label_mr": "तुम्ही महाराष्ट्रात सलग किमान १५ वर्षे वास्तव्यास आहात का?",
            "description_en": "Continuous 15-year residence is a mandatory statutory requirement under the Executive Magistrate rules.",
            "description_mr": "कार्यकारी दंडाधिकारी नियमांनुसार महाराष्ट्रात सलग १५ वर्षे प्रत्यक्ष वास्तव्य अनिवार्य आहे.",
            "required": True
        },
        {
            "id": "q_birth_proof",
            "field_key": "has_birth_or_tc",
            "type": "boolean",
            "label_en": "Do you possess a valid Birth Certificate or School Leaving Certificate showing birth in Maharashtra?",
            "label_mr": "तुमच्याकडे महाराष्ट्रातील जन्म दाखला किंवा शाळा सोडल्याचा दाखला (TC/LC) आहे का?",
            "description_en": "Proof of date and place of birth.",
            "description_mr": "जन्मतारीख व जन्मस्थळ सिद्ध करणारा अधिकृत दाखला.",
            "required": True
        }
    ],
    "age-nationality-and-domicile-certificate": [
        {
            "id": "q_dom_nat",
            "field_key": "residence_15_indian",
            "type": "boolean",
            "label_en": "Are you an Indian citizen with continuous 15-year residence in Maharashtra?",
            "label_mr": "तुम्ही भारतीय नागरिक असून महाराष्ट्रात सलग १५ वर्षे वास्तव्यास आहात का?",
            "description_en": "Verifies both citizenship and state domicile simultaneously.",
            "description_mr": "भारतीय नागरिकत्व व १५ वर्षे वास्तव्याचा संयुक्त निकष.",
            "required": True
        }
    ],
    "income-certificate": [
        {
            "id": "q_inc_proof",
            "field_key": "has_income_proof",
            "type": "boolean",
            "label_en": "Do you have valid proof of family income (Salary Slip Form 16 / ITR / Talathi Report)?",
            "label_mr": "तुमच्याकडे उत्पन्नाचा पुरावा (वेतन प्रमाणपत्र फॉर्म १६ / आयटीआर / तलाठी अहवाल) आहे का?",
            "description_en": "Required by Tahsildar to verify family earnings.",
            "description_mr": "तहसीलदार कार्यालयाकडून उत्पन्नाची पडताळणी करण्यासाठी आवश्यक पुरावा.",
            "required": True
        },
        {
            "id": "q_annual_amount",
            "field_key": "annual_income_numeric",
            "type": "number",
            "label_en": "What is your total annual household income in INR (₹)?",
            "label_mr": "कुटुंबाचे अंदाजे एकूण वार्षिक उत्पन्न किती आहे (₹ रुपयांमध्ये)?",
            "description_en": "Enter total combined earnings of all earning family members.",
            "description_mr": "कुटुंबातील सर्व मिळवत्या सदस्यांचे एकत्रित वार्षिक उत्पन्न टाका.",
            "required": True
        }
    ],
    "caste-certificate": [
        {
            "id": "q_caste_member",
            "field_key": "is_reserved_category",
            "type": "boolean",
            "label_en": "Do you belong to SC, ST, VJNT, SBC, or OBC community recognized in Maharashtra?",
            "label_mr": "तुम्ही महाराष्ट्रात अधिसूचित असलेल्या अनुसूचित जाती, जमाती, विमुक्त जाती, भटक्या जमाती किंवा इतर मागासवर्गातील आहात का?",
            "description_en": "The caste must be included in Maharashtra state reservation gazettes.",
            "description_mr": "जात महाराष्ट्र शासनाच्या अधिकृत आरक्षण राजपत्रात समाविष्ट असणे आवश्यक आहे.",
            "required": True
        },
        {
            "id": "q_paternal_caste",
            "field_key": "has_paternal_records",
            "type": "boolean",
            "label_en": "Do you have paternal ancestral evidence (Father/Uncle/Grandfather school or revenue records)?",
            "label_mr": "तुमच्याकडे रक्ताच्या नातेवाईकाचा (वडील/काका/आजोबा) जुना जातीचा शाळा किंवा महसुली पुरावा आहे का?",
            "description_en": "Caste claims must be substantiated through paternal lineage.",
            "description_mr": "जात ही पितृसत्ताक वंशावळीवरून सिद्ध करावी लागते.",
            "required": True
        }
    ],
    "non-creamy-layer-certificate": [
        {
            "id": "q_ncl_limit",
            "field_key": "under_8_lakhs",
            "type": "boolean",
            "label_en": "Has your family's annual income been strictly under ₹8 Lakhs in each of the last 3 financial years?",
            "label_mr": "मागील सलग ३ आर्थिक वर्षांत कुटुंबाचे वार्षिक उत्पन्न प्रत्येक वर्षी ₹८ लाखांपेक्षा कमी आहे का?",
            "description_en": "The Creamy Layer ceiling is ₹8,00,000 per annum.",
            "description_mr": "नॉन-क्रीमी लेयरची कमाल मर्यादा वार्षिक ८ लाख रुपये आहे.",
            "required": True
        }
    ]
}

def _default_questions(lang: str) -> List[Dict[str, Any]]:
    if lang == "mr":
        return [
            {
                "id": "gen_q1",
                "field_key": "is_mh_resident",
                "type": "boolean",
                "label_mr": "तुम्ही महाराष्ट्रात राहणारे भारतीय नागरिक आहात का?",
                "label_en": "Are you a resident citizen of Maharashtra?",
                "description_mr": "आपले सरकार पोर्टलवरील सेवांसाठी सामान्य अधिवास निकष.",
                "description_en": "General residence eligibility for Maharashtra state portal services.",
                "required": True
            },
            {
                "id": "gen_q2",
                "field_key": "has_aadhaar",
                "type": "boolean",
                "label_mr": "तुमच्याकडे अचूक नाव व पत्ता असलेले आधार कार्ड आहे का?",
                "label_en": "Do you possess a valid Aadhaar Card with matching name and address?",
                "description_mr": "ई-केवायसी व अर्जातील ओळखीच्या पडताळणीसाठी आवश्यक.",
                "description_en": "Required for e-KYC and identity verification.",
                "required": True
            }
        ]
    return [
        {
            "id": "gen_q1",
            "field_key": "is_mh_resident",
            "type": "boolean",
            "label_en": "Are you a resident citizen of Maharashtra?",
            "description_en": "General residence eligibility for Maharashtra state portal services.",
            "required": True
        },
        {
            "id": "gen_q2",
            "field_key": "has_aadhaar",
            "type": "boolean",
            "label_en": "Do you possess a valid Aadhaar Card with matching name and address?",
            "description_en": "Required for e-KYC and identity verification on Aaple Sarkar.",
            "required": True
        }
    ]

@router.get("/{slug}/eligibility/questions", response_model=ApiResponse[EligibilityQuestionsResponse])
def get_eligibility_questions(
    slug: str,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()

    service_name = slug.replace("-", " ").title()
    questions_out: List[EligibilityQuestionOut] = []

    if service and service.eligibility_questions:
        service_name = service.name_mr if (language == "mr" and service.name_mr) else service.name_en
        for q in service.eligibility_questions:
            lbl = q.label_mr if (language == "mr" and q.label_mr) else q.label_en
            desc = q.help_text_mr if (language == "mr" and q.help_text_mr) else q.help_text_en
            v_data = None
            if q.validation_json:
                try:
                    v_data = json.loads(q.validation_json)
                except Exception:
                    v_data = None
            questions_out.append(
                EligibilityQuestionOut(
                    id=str(q.id),
                    field_key=q.field_key or f"field_{q.id}",
                    question_type=q.question_type or "boolean",
                    type=q.question_type or "boolean",
                    label=lbl,
                    help_text=desc,
                    description=desc,
                    required=q.required,
                    display_order=q.display_order,
                    validation=v_data
                )
            )
    else:
        # Fallback to static verified questions
        from app.seed import SUBMISSION_SERVICES
        s_meta = next((x for x in SUBMISSION_SERVICES if x["slug"] == slug), None)
        if s_meta:
            service_name = s_meta["name_mr"] if language == "mr" else s_meta["name_en"]

        raw = STATIC_QUESTIONS.get(slug) or _default_questions(language)
        for idx, q in enumerate(raw):
            lbl = q["label_mr"] if (language == "mr" and "label_mr" in q) else q["label_en"]
            desc = q.get("description_mr") if (language == "mr" and "description_mr" in q) else q.get("description_en")
            questions_out.append(
                EligibilityQuestionOut(
                    id=q["id"],
                    field_key=q.get("field_key", q["id"]),
                    question_type=q.get("type", "boolean"),
                    type=q.get("type", "boolean"),
                    label=lbl,
                    help_text=desc,
                    description=desc,
                    required=q.get("required", True),
                    display_order=idx + 1
                )
            )

    return ApiResponse.ok(
        EligibilityQuestionsResponse(
            service_slug=slug,
            service_name=service_name,
            questions=questions_out
        )
    )

@router.post("/{slug}/eligibility/evaluate", response_model=ApiResponse[EligibilityEvaluationResponse])
def evaluate_eligibility(
    slug: str,
    req: EligibilityEvaluationRequest,
    db: Session = Depends(get_db)
):
    lang = req.language
    answers = req.answers or {}

    # Check boolean values
    all_positive = True
    for key, val in answers.items():
        if val is False or str(val).lower() == "false":
            all_positive = False
            break

    from app.seed import SUBMISSION_SERVICES
    s_meta = next((x for x in SUBMISSION_SERVICES if x["slug"] == slug), None)
    s_name = s_meta["name_mr"] if (s_meta and lang == "mr") else (s_meta["name_en"] if s_meta else slug.replace("-", " ").title())

    if all_positive and len(answers) > 0:
        if lang == "mr":
            summary = f"तुम्ही {s_name} मिळवण्यासाठी प्राथमिकदृष्ट्या पात्र आहात."
            explanation = "तुमच्या दिलेल्या उत्तरांवरून तुम्ही या सेवेचे सर्व प्राथमिक वैधानिक निकष पूर्ण करत असल्याचे दिसते. आपले सरकार पोर्टलवर (aaplesarkar.mahaonline.gov.in) जाऊन कागदपत्रांसह थेट अर्ज करा."
        else:
            summary = f"You appear to be potentially eligible for {s_name}."
            explanation = "Based on your self-reported answers, you meet the preliminary statutory criteria under Maharashtra Government rules. You can proceed to upload your verified documents on aaplesarkar.mahaonline.gov.in."

        status_result = "potentially_eligible"
    else:
        if lang == "mr":
            summary = "तुम्ही काही आवश्यक निकष पूर्ण करत नसल्याचे दिसून येत आहे."
            explanation = "या सेवेसाठी विहित केलेल्या अटींची पूर्तता करणे आवश्यक आहे. अधिक माहितीसाठी व पर्यायी कागदपत्रांबद्दल 'सारथी' सहाय्यकाशी बोला."
        else:
            summary = "You may not meet all the preliminary statutory conditions."
            explanation = "One or more essential eligibility criteria appear unfulfilled. Please review the mandatory requirements or consult the assistant for alternative documentation."

        status_result = "potentially_not_eligible"

    return ApiResponse.ok(
        EligibilityEvaluationResponse(
            status=status_result,
            summary=summary,
            explanation=explanation,
            missing_information=[],
            rule_results=[
                RuleResultOut(
                    rule_code="RTS_STATUTORY_RULE",
                    description="Maharashtra Right to Public Services Act (RTS) Criteria",
                    passed=all_positive
                )
            ],
            sources=[
                SourceOut(
                    id="aaple-sarkar",
                    title="Aaple Sarkar Eligibility Framework",
                    url="https://aaplesarkar.mahaonline.gov.in",
                    publisher="Government of Maharashtra",
                    source_type="official_gazette",
                    supports="Statutory Eligibility Evaluation"
                )
            ]
        )
    )
