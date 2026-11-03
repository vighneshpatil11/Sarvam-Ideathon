import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.database import engine, Base, SessionLocal
from app.models import Service, ServiceDocument, KnowledgeChunk

DETAILED_DOCUMENTS = {
    "domicile-certificate": [
        {
            "name_en": "Proof of Continuous 15-Year Residence in Maharashtra",
            "name_mr": "महाराष्ट्रात सलग १५ वर्षे वास्तव्याचा पुरावा (रेशन कार्ड, वीज बिल, कर पावती, भाडेकरार)",
            "category": "address_proof",
            "is_mandatory": True,
            "description_en": "School Leaving Certificate, continuous 15-year electricity bills, or registered property records."
        },
        {
            "name_en": "Proof of Age & Birth (Birth Certificate / School Leaving Certificate - TC/LC)",
            "name_mr": "वय व जन्माचा पुरावा (जन्म दाखला / शाळा सोडल्याचा दाखला)",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Certificate showing place and date of birth in Maharashtra."
        },
        {
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / Passport)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र / पासपोर्ट)",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Valid government-issued photo identity proof."
        },
        {
            "name_en": "Self-Declaration Form for Domicile",
            "name_mr": "अधिवास स्वयंघोषणा पत्र (विहित नमुना)",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Statutory self-declaration affirming 15 years uninterrupted residence in Maharashtra."
        }
    ],
    "age-nationality-and-domicile-certificate": [
        {
            "name_en": "Continuous 15-Year Residence Proof in Maharashtra",
            "name_mr": "महाराष्ट्रात सलग १५ वर्षे वास्तव्याचा पुरावा (वीज बिले, रेशन कार्ड)",
            "category": "address_proof",
            "is_mandatory": True,
            "description_en": "15 years continuous residential documentary proof."
        },
        {
            "name_en": "Birth Certificate / School Leaving Certificate (SLC)",
            "name_mr": "जन्म दाखला / शाळा सोडल्याचा दाखला",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Proof of Indian nationality and age."
        },
        {
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / Passport)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र)",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Government-issued photo identification."
        },
        {
            "name_en": "Domicile & Nationality Self-Declaration Affidavit",
            "name_mr": "अधिवास व राष्ट्रीयत्व स्वयंघोषणा प्रतिज्ञापत्र",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Prescribed statutory affidavit on Aaple Sarkar."
        }
    ],
    "income-certificate": [
        {
            "name_en": "Proof of Income (Salary Slip Form 16 / ITR / Talathi Income Report)",
            "name_mr": "उत्पन्नाचा पुरावा (वेतन प्रमाणपत्र फॉर्म १६ / आयटीआर / तलाठी अहवाल)",
            "category": "income_proof",
            "is_mandatory": True,
            "description_en": "Employer salary certificate, Income Tax Return, or verified report from village Talathi."
        },
        {
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID / PAN Card)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / पॅन कार्ड)",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Government photo identity document."
        },
        {
            "name_en": "Proof of Address (Ration Card / Electricity Bill)",
            "name_mr": "पत्त्याचा पुरावा (रेशन कार्ड / वीज बिल)",
            "category": "address_proof",
            "is_mandatory": True,
            "description_en": "Current residence utility or ration document."
        },
        {
            "name_en": "Income Self-Declaration Affidavit",
            "name_mr": "उत्पन्न स्वयंघोषणा पत्र",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Statutory declaration of annual household income."
        }
    ],
    "caste-certificate": [
        {
            "name_en": "Applicant & Father's School Leaving Certificate showing Caste entry",
            "name_mr": "अर्जदार व वडिलांचा शाळा सोडल्याचा दाखला (जातीची नोंद असलेला)",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Primary school register extract or SLC showing traditional caste and religion."
        },
        {
            "name_en": "Caste Certificate of Paternal Relative (Father/Uncle/Grandfather) or Validity",
            "name_mr": "रक्ताच्या नातेवाईकाचे जात प्रमाणपत्र किंवा जात वैधता प्रमाणपत्र",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Paternal blood relative certificate."
        },
        {
            "name_en": "Proof of Identity (Aadhaar Card / Voter ID)",
            "name_mr": "ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र)",
            "category": "identity_proof",
            "is_mandatory": True,
            "description_en": "Valid identity card."
        },
        {
            "name_en": "Proof of Address & Pre-Cutoff Residence Evidence",
            "name_mr": "पत्त्याचा पुरावा व जुने महसुली पुरावे (१९५०/१९६१/१९६७ पूर्वीचे)",
            "category": "address_proof",
            "is_mandatory": True,
            "description_en": "Old revenue or school records prior to statutory cutoff dates."
        },
        {
            "name_en": "Caste Affidavit (Form 3 / 17)",
            "name_mr": "जात प्रतिज्ञापत्र (नमुना ३ / १७)",
            "category": "other",
            "is_mandatory": True,
            "description_en": "Affidavit for caste claim."
        }
    ]
}

def enrich_specific_documents():
    db = SessionLocal()
    try:
        for slug, doc_list in DETAILED_DOCUMENTS.items():
            svc = db.query(Service).filter_by(slug=slug).first()
            if not svc:
                continue

            # Delete old generic docs
            db.query(ServiceDocument).filter_by(service_id=svc.id).delete()

            for idx, d in enumerate(doc_list):
                sdoc = ServiceDocument(
                    service_id=svc.id,
                    name_en=d["name_en"],
                    name_mr=d["name_mr"],
                    name_hi=d["name_en"],
                    category=d["category"],
                    is_mandatory=d["is_mandatory"],
                    description_en=d["description_en"],
                    display_order=idx + 1
                )
                db.add(sdoc)

            # Update knowledge chunks with clear mandatory document text
            doc_names_en = ", ".join([d["name_en"] for d in doc_list])
            doc_names_mr = ", ".join([d["name_mr"] for d in doc_list])

            kc = db.query(KnowledgeChunk).filter_by(service_id=svc.id).first()
            if kc:
                kc.content_en = (
                    f"To obtain a {svc.name_en} in Maharashtra, the applicant must provide the following mandatory documents: {doc_names_en}. "
                    f"For Domicile, continuous 15-year physical residence in Maharashtra is strictly mandatory. "
                    f"Official statutory fee is ₹{svc.statutory_fee_inr:.2f} and processing timeline under Maharashtra RTS Act is {svc.processing_days} working days."
                )
                kc.content_mr = (
                    f"{svc.name_mr} मिळवण्यासाठी खालील कागदपत्रे अनिवार्य आहेत: {doc_names_mr}. "
                    f"अधिवास प्रमाणपत्रासाठी महाराष्ट्रात सलग १५ वर्षे प्रत्यक्ष वास्तव्य असणे बंधनकारक आहे. "
                    f"अधिकृत शासकीय शुल्क ₹{svc.statutory_fee_inr:.2f} असून विहित मुदत {svc.processing_days} कामकाजाचे दिवस आहे."
                )

            print(f"Updated specific documents and knowledge chunks for: {svc.name_en}")

        db.commit()
        print("Detailed document enrichment complete!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    enrich_specific_documents()
