from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Service
from app.schemas import ApiResponse, ServiceStepsResponse, StepOut, SourceOut

router = APIRouter(prefix="/services", tags=["Application Steps"])

@router.get("/{slug}/steps", response_model=ApiResponse[ServiceStepsResponse])
def get_service_steps(
    slug: str,
    language: str = Query("en", pattern="^(en|hi|mr)$"),
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.slug == slug).first()

    from app.seed import SUBMISSION_SERVICES
    s_meta = next((x for x in SUBMISSION_SERVICES if x["slug"] == slug), None)

    service_name = slug.replace("-", " ").title()
    portal_url = "https://aaplesarkar.mahaonline.gov.in"
    fee = 33.60
    days = 15

    if s_meta:
        service_name = s_meta["name_mr"] if language == "mr" else s_meta["name_en"]
        portal_url = s_meta.get("source_url") or portal_url
        fee = s_meta.get("statutory_fee_inr", 33.60)
        days = s_meta.get("processing_days", 15)
    elif service:
        service_name = service.name_mr if (language == "mr" and service.name_mr) else service.name_en
        portal_url = service.official_portal_url or portal_url
        fee = service.statutory_fee_inr
        days = service.processing_days

    steps_out: List[StepOut] = []

    if service and service.application_steps:
        for step in service.application_steps:
            title = step.title_mr if (language == "mr" and step.title_mr) else step.title_en
            desc = step.instructions_mr if (language == "mr" and step.instructions_mr) else step.instructions_en
            url = step.external_url or portal_url
            steps_out.append(
                StepOut(
                    step_number=step.step_number,
                    title=title,
                    instructions=desc,
                    description=desc,
                    external_url=url,
                    action_url=url,
                    action_label="आपले सरकार पोर्टल उघडा" if language == "mr" else "Open Aaple Sarkar Portal",
                    sources=[SourceOut(
                        id="aaple-sarkar",
                        title="Aaple Sarkar Portal Guide",
                        url=portal_url,
                        publisher="Government of Maharashtra",
                        source_type="official_gazette",
                        supports="Step-by-step application workflow"
                    )]
                )
            )
    else:
        # Static verified 4-step workflow for Aaple Sarkar
        if language == "mr":
            raw_steps = [
                {
                    "step_number": 1,
                    "title": "आपले सरकार पोर्टलवर नोंदणी / लॉगिन करा",
                    "description": "aaplesarkar.mahaonline.gov.in या संकेतस्थळाला भेट द्या आणि नागरिक खात्याद्वारे (User ID & Password) लॉगिन करा."
                },
                {
                    "step_number": 2,
                    "title": f"विभागामध्ये जाऊन सेवा निवडा ({service_name})",
                    "description": f"पोर्टलच्या मुख्य डॅशबोर्डवर डाव्या बाजूला संबंधित विभाग निवडून {service_name} या सेवेवर क्लिक करा आणि विहित नमुन्यातील ऑनलाइन अर्ज भरा."
                },
                {
                    "step_number": 3,
                    "title": f"कागदपत्रे अपलोड करा व अधिकृत शुल्क (₹{fee:.2f}) भरा",
                    "description": f"आवश्यक सर्व स्कॅन केलेली कागदपत्रे व स्वयंघोषणा पत्र जोडा. त्यानंतर नेट बँकिंग, यूपीआय किंवा कार्डद्वारे अधिकृत शासकीय शुल्क ₹{fee:.2f} ऑनलाइन जमा करा."
                },
                {
                    "step_number": 4,
                    "title": f"डिजिटल स्वाक्षरी असलेले प्रमाणपत्र डाउनलोड करा ({days} दिवस)",
                    "description": f"महाराष्ट्र लोकसेवा हमी कायद्यानुसार (RTS) विहित मुदतीत ({days} कामकाजाचे दिवस) सक्षम अधिकाऱ्याची डिजिटल स्वाक्षरी असलेला दाखला थेट तुमच्या डॅशबोर्डवर उपलब्ध होतो."
                }
            ]
        else:
            raw_steps = [
                {
                    "step_number": 1,
                    "title": "Register / Login to Aaple Sarkar Portal",
                    "description": "Visit aaplesarkar.mahaonline.gov.in and log in with your citizen credentials or register with Aadhaar OTP."
                },
                {
                    "step_number": 2,
                    "title": f"Select Department & Apply for {service_name}",
                    "description": f"Navigate to the issuing department from the menu and select {service_name}. Fill out the online application form with accurate personal details."
                },
                {
                    "step_number": 3,
                    "title": f"Upload Documents & Pay Statutory Fee (₹{fee:.2f})",
                    "description": f"Upload the scanned identity, address, and supporting records along with the self-declaration affidavit. Pay the statutory government fee of ₹{fee:.2f} online."
                },
                {
                    "step_number": 4,
                    "title": f"Download Digitally Signed Certificate (RTS: {days} Days)",
                    "description": f"Under the Maharashtra Right to Public Services Act (RTS), your certificate will be delivered within {days} working days directly to your portal account."
                }
            ]

        for s in raw_steps:
            steps_out.append(
                StepOut(
                    step_number=s["step_number"],
                    title=s["title"],
                    instructions=s["description"],
                    description=s["description"],
                    external_url=portal_url,
                    action_url=portal_url,
                    action_label="आपले सरकार पोर्टल उघडा" if language == "mr" else "Open Aaple Sarkar Portal",
                    sources=[SourceOut(
                        id="aaple-sarkar",
                        title="Aaple Sarkar Portal Guide",
                        url=portal_url,
                        publisher="Government of Maharashtra",
                        source_type="official_gazette",
                        supports="Step-by-step application workflow"
                    )]
                )
            )

    steps_out.sort(key=lambda x: x.step_number)

    return ApiResponse.ok(
        ServiceStepsResponse(
            service_slug=slug,
            service_name=service_name,
            official_portal_url=portal_url,
            statutory_fee_inr=fee,
            processing_days=days,
            steps=steps_out
        )
    )
