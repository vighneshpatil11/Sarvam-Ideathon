from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service, ServiceDocument
from app.schemas import ApiResponse, ServiceDocumentsResponse, DocumentOut, SourceOut

router = APIRouter(prefix="/services", tags=["Documents"])

STATIC_DOCUMENTS: Dict[str, List[Dict[str, Any]]] = {
    "domicile-certificate": [
        {
            "id": "dom-1",
            "name_en": "Proof of Continuous 15-Year Residence in Maharashtra",
            "name_mr": "महाराष्ट्रात सलग १५ वर्षे वास्तव्याचा पुरावा (रेशन कार्ड / वीज बिल / भाडेकरार)",
            "category": "address_proof",
            "required": True,
            "description_en": "School Leaving Certificate, continuous 15-year utility bills, or registered property records."
        },
        {
            "id": "dom-2",
            "name_en": "Proof of Age & Birth (Birth Certificate / School TC)",
            "name_mr": "वय व जन्माचा पुरावा (जन्म दाखला / शाळा सोडल्याचा दाखला)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Certificate showing place and date of birth in Maharashtra."
        },
        {
            "id": "dom-3",
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / Passport)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Valid government-issued photo identity proof."
        },
        {
            "id": "dom-4",
            "name_en": "Domicile Self-Declaration Affidavit",
            "name_mr": "अधिवास स्वयंघोषणा प्रतिज्ञापत्र",
            "category": "other",
            "required": True,
            "description_en": "Statutory self-declaration affirming 15 years uninterrupted residence in Maharashtra."
        }
    ],
    "income-certificate": [
        {
            "id": "inc-1",
            "name_en": "Proof of Income (Salary Slip Form 16 / ITR / Talathi Income Report)",
            "name_mr": "उत्पन्नाचा पुरावा (वेतन प्रमाणपत्र फॉर्म १६ / आयटीआर / तलाठी अहवाल)",
            "category": "income_proof",
            "required": True,
            "description_en": "Employer salary certificate, Income Tax Return, or verified report from village Talathi."
        },
        {
            "id": "inc-2",
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / PAN Card)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / पॅन कार्ड)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Valid government photo identity document."
        },
        {
            "id": "inc-3",
            "name_en": "Proof of Address (Ration Card / Electricity Bill)",
            "name_mr": "पत्त्याचा पुरावा (रेशन कार्ड / वीज बिल)",
            "category": "address_proof",
            "required": True,
            "description_en": "Current residence utility or ration document."
        },
        {
            "id": "inc-4",
            "name_en": "Income Self-Declaration Affidavit",
            "name_mr": "उत्पन्न स्वयंघोषणा पत्र",
            "category": "other",
            "required": True,
            "description_en": "Statutory declaration of annual household income."
        }
    ],
    "caste-certificate": [
        {
            "id": "cst-1",
            "name_en": "Applicant & Father's School Leaving Certificate showing Caste entry",
            "name_mr": "अर्जदार व वडिलांचा शाळा सोडल्याचा दाखला (जातीची नोंद असलेला)",
            "category": "other",
            "required": True,
            "description_en": "Primary school register extract or SLC showing traditional caste and religion."
        },
        {
            "id": "cst-2",
            "name_en": "Caste Certificate of Paternal Relative or Validity Certificate",
            "name_mr": "रक्ताच्या नातेवाईकाचे जात प्रमाणपत्र किंवा वैधता प्रमाणपत्र",
            "category": "other",
            "required": True,
            "description_en": "Paternal blood relative certificate."
        },
        {
            "id": "cst-3",
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Valid identity card."
        },
        {
            "id": "cst-4",
            "name_en": "Proof of Address & Pre-Cutoff Residence Evidence",
            "name_mr": "पत्त्याचा पुरावा व जुने महसुली पुरावे (१९५०/१९६१/१९६७ पूर्वीचे)",
            "category": "address_proof",
            "required": True,
            "description_en": "Old revenue or school records prior to statutory cutoff dates."
        },
        {
            "id": "cst-5",
            "name_en": "Caste Affidavit (Form 3 / Form 17)",
            "name_mr": "जात प्रतिज्ञापत्र (नमुना ३ / १७)",
            "category": "other",
            "required": True,
            "description_en": "Prescribed statutory affidavit on Aaple Sarkar."
        }
    ],
    "non-creamy-layer-certificate": [
        {
            "id": "ncl-1",
            "name_en": "Income Proof for Last 3 Financial Years (ITR / Form 16 / Tahsildar Income Proof)",
            "name_mr": "मागील ३ आर्थिक वर्षांचा उत्पन्नाचा पुरावा (फॉर्म १६ / आयटीआर / दाखला)",
            "category": "income_proof",
            "required": True,
            "description_en": "Evidence showing annual income does not exceed ₹8 Lakhs threshold."
        },
        {
            "id": "ncl-2",
            "name_en": "Valid Caste Certificate of Applicant",
            "name_mr": "अर्जदाराचे अधिकृत जात प्रमाणपत्र",
            "category": "other",
            "required": True,
            "description_en": "OBC / VJNT / SBC caste certificate issued by Competent Authority."
        },
        {
            "id": "ncl-3",
            "name_en": "Proof of Identity & Address (Aadhaar Card & Electricity Bill)",
            "name_mr": "ओळख व पत्त्याचा पुरावा (आधार कार्ड व वीज बिल)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Valid photo ID and current address proof."
        },
        {
            "id": "ncl-4",
            "name_en": "Non-Creamy Layer Self-Declaration Affidavit",
            "name_mr": "नॉन-क्रीमी लेयर स्वयंघोषणा प्रतिज्ञापत्र",
            "category": "other",
            "required": True,
            "description_en": "Statutory self-declaration of family income and asset limits."
        }
    ]
}

def _default_service_documents(service_name_en: str, service_name_mr: str) -> List[Dict[str, Any]]:
    return [
        {
            "id": "gen-1",
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / PAN Card / Passport)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र / पॅन कार्ड)",
            "category": "identity_proof",
            "required": True,
            "description_en": "Valid government-issued photo identity proof."
        },
        {
            "id": "gen-2",
            "name_en": "Proof of Address (Ration Card / Electricity Bill / Property Tax Receipt)",
            "name_mr": "पत्त्याचा पुरावा (रेशन कार्ड / वीज बिल / कर पावती)",
            "category": "address_proof",
            "required": True,
            "description_en": "Current residence utility bill or official government address proof."
        },
        {
            "id": "gen-3",
            "name_en": f"Specific Supporting Records for {service_name_en}",
            "name_mr": f"{service_name_mr} साठी संबंधित मूळ कागदपत्रे / पुरावे",
            "category": "other",
            "required": True,
            "description_en": "Original supporting certificates or records required under the Maharashtra RTS Act."
        },
        {
            "id": "gen-4",
            "name_en": "Prescribed Self-Declaration Affidavit on Aaple Sarkar",
            "name_mr": "आपले सरकार पोर्टलवरील विहित नमुन्यातील स्वयंघोषणा पत्र",
            "category": "other",
            "required": True,
            "description_en": "Statutory self-declaration form available on aaplesarkar.mahaonline.gov.in."
        }
    ]

@router.get("/{slug}/documents", response_model=ApiResponse[ServiceDocumentsResponse])
def get_service_documents(
    slug: str,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()
    
    docs_out: List[DocumentOut] = []
    service_name = slug.replace("-", " ").title()

    if service and service.documents:
        service_name = service.name_mr if (language == "mr" and service.name_mr) else service.name_en
        for d in service.documents:
            name = d.name_mr if (language == "mr" and d.name_mr) else d.name_en
            desc = d.description_mr if (language == "mr" and d.description_mr) else d.description_en
            docs_out.append(
                DocumentOut(
                    id=str(d.id),
                    name=name,
                    category=d.category or "other",
                    is_mandatory=d.is_mandatory,
                    required=d.is_mandatory,
                    description=desc,
                    issuing_authority=d.issuing_authority,
                    display_order=d.display_order,
                    sources=[SourceOut(
                        id="aaple-sarkar",
                        title="Aaple Sarkar MahaOnline Portal",
                        url="https://aaplesarkar.mahaonline.gov.in",
                        publisher="Government of Maharashtra",
                        source_type="official_gazette",
                        supports="Statutory Documents Checklist"
                    )]
                )
            )
    else:
        # Static fallback for cold starts or unseeded database
        from app.seed import SUBMISSION_SERVICES
        s_meta = next((x for x in SUBMISSION_SERVICES if x["slug"] == slug), None)
        if s_meta:
            service_name = s_meta["name_mr"] if language == "mr" else s_meta["name_en"]
            raw_docs = STATIC_DOCUMENTS.get(slug) or _default_service_documents(s_meta["name_en"], s_meta["name_mr"])
        else:
            raw_docs = STATIC_DOCUMENTS.get(slug) or _default_service_documents(service_name, service_name)

        for idx, d in enumerate(raw_docs):
            name = d["name_mr"] if (language == "mr" and "name_mr" in d) else d["name_en"]
            desc = d.get("description_mr") if (language == "mr" and "description_mr" in d) else d.get("description_en")
            docs_out.append(
                DocumentOut(
                    id=d["id"],
                    name=name,
                    category=d.get("category", "other"),
                    is_mandatory=d.get("required", True),
                    required=d.get("required", True),
                    description=desc,
                    display_order=idx + 1,
                    sources=[SourceOut(
                        id="aaple-sarkar",
                        title="Aaple Sarkar MahaOnline Portal",
                        url="https://aaplesarkar.mahaonline.gov.in",
                        publisher="Government of Maharashtra",
                        source_type="official_gazette",
                        supports="Statutory Documents Checklist"
                    )]
                )
            )

    return ApiResponse.ok(
        ServiceDocumentsResponse(
            service_slug=slug,
            service_name=service_name,
            documents=docs_out
        )
    )
