import os
import sys
import uuid
from datetime import datetime, timezone

# Ensure backend app is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.database import engine, Base, SessionLocal
from app.models import (
    State, District, Department, Source, Service, ServiceDocument,
    ApplicationStep, EligibilityQuestion, EligibilityRule, KnowledgeChunk
)

# Comprehensive list of Aaple Sarkar Services
SERVICES_DATA = [
  {
    "name_en": "Income Certificate",
    "name_mr": "उत्पन्नाचे प्रमाणपत्र",
    "slug": "income-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate certifying the annual income of an individual or family from all sources.",
    "short_description_mr": "व्यक्ती किंवा कुटुंबाचे सर्व स्रोतांकडून मिळणारे वार्षिक उत्पन्न प्रमाणित करणारा दाखला.",
    "description_en": "The Income Certificate is issued by the Revenue Department under the Tahsildar to verify the total annual earnings of a family. It is required for availing educational scholarships, fee concessions, government welfare schemes, and reservation benefits.",
    "description_mr": "महसूल विभागामार्फत तहसीलदार यांच्या स्वाक्षरीने कुटुंबाचे वार्षिक उत्पन्न प्रमाणित करणारा दाखला दिला जातो. शैक्षणिक शिष्यवृत्ती, फी सवलत आणि विविध शासकीय योजनांचा लाभ घेण्यासाठी हा दाखला आवश्यक आहे.",
    "eligibility": [
      "Permanent resident of Maharashtra",
      "Individual or family head earning income within the state"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID / PAN Card", "name_mr": "आधार कार्ड / मतदार ओळखपत्र / पॅन कार्ड", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill", "name_mr": "रेशन कार्ड / वीज बिल", "description_en": "Proof of Address", "category": "address_proof", "required": True},
      {"name_en": "Salary Slip / Form 16 / Talathi Income Report / ITR", "name_mr": "वेतन प्रमाणपत्र / फॉर्म १६ / तलाठी अहवाल", "description_en": "Proof of Income", "category": "income_proof", "required": True},
      {"name_en": "Self-Declaration Affidavit", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Standard self-declaration format on portal", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Registration", "title_mr": "पोर्टल नोंदणी", "instructions_en": "Register on Aaple Sarkar portal using Aadhaar OTP verification.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Service Selection", "title_mr": "सेवा निवड", "instructions_en": "Navigate to Revenue Department -> Revenue Services -> Income Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Fill Details & Upload Documents", "title_mr": "माहिती भरा व कागदपत्रे अपलोड करा", "instructions_en": "Fill personal, family, and income details; upload scanned photo, ID, address proof, and income proof.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Pay Fee & Submit", "title_mr": "शुल्क भरा व अर्ज सादर करा", "instructions_en": "Pay statutory fee online via GRAS gateway and download acknowledgement slip.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Age, Nationality and Domicile Certificate",
    "name_mr": "वय, राष्ट्रीयत्व आणि अधिवास प्रमाणपत्र",
    "slug": "age-nationality-and-domicile-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certificate proving continuous residence for at least 15 years in Maharashtra and Indian nationality.",
    "short_description_mr": "महाराष्ट्र राज्यात किमान १५ वर्षे सलग वास्तव्याचा पुरावा आणि भारतीय राष्ट्रीयत्व सिद्ध करणारा दाखला.",
    "description_en": "Issued by the Executive Magistrate/Tahsildar to certify that the applicant is an Indian citizen and has resided in Maharashtra for not less than 15 years. Essential for admission to educational institutes under state quotas and state government employment.",
    "description_mr": "अर्जदार भारतीय नागरिक असून महाराष्ट्रात किमान १५ वर्षे वास्तव्य करत असल्याचे प्रमाणित करणारा दाखला. शासकीय नोकऱ्या व राज्यातील शैक्षणिक प्रवेशांसाठी अनिवार्य आहे.",
    "eligibility": [
      "Indian citizen",
      "Resident of Maharashtra for continuous 15 years or more"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID / Passport", "name_mr": "आधार कार्ड / मतदार ओळखपत्र / पासपोर्ट", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill / Property Tax Receipt (spanning 15 years)", "name_mr": "रेशन कार्ड / वीज बिल / कर पावती (१५ वर्षे)", "description_en": "Proof of Residence for 15 years", "category": "address_proof", "required": True},
      {"name_en": "School Leaving Certificate / Birth Certificate", "name_mr": "शाळा सोडल्याचा दाखला / जन्म दाखला", "description_en": "Proof of Age & Birthplace", "category": "identity_proof", "required": True},
      {"name_en": "Self-Declaration Form", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Prescribed domicile declaration form", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Register / Login", "title_mr": "नोंदणी / लॉगिन", "instructions_en": "Log in to Aaple Sarkar portal with citizen credentials.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Apply for Domicile", "title_mr": "अधिवास प्रमाणपत्रासाठी अर्ज", "instructions_en": "Select Revenue Department -> Age, Nationality and Domicile Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload 15-Year Residence Evidence", "title_mr": "१५ वर्षांच्या वास्तव्याचे पुरावे जोडा", "instructions_en": "Upload applicant documents and proof of continuous 15-year stay in Maharashtra.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Payment & Track", "title_mr": "शुल्क भरा व अर्ज ट्रॅक करा", "instructions_en": "Pay statutory fee and track status using the generated application ID.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Caste Certificate",
    "name_mr": "जात प्रमाणपत्र",
    "slug": "caste-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate authenticating an individual's membership in a recognized SC, ST, VJNT, SBC, or OBC community.",
    "short_description_mr": "अनुसूचित जाती, जमाती, विमुक्त जाती, भटक्या जमाती किंवा इतर मागासवर्गातील सदस्यत्व प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Sub-Divisional Officer (SDO) to substantiate an applicant's claim of belonging to a reserved category. Mandatory for quota-based college admissions, competitive exam concessions, and reserved government recruitments.",
    "description_mr": "उपविभागीय अधिकारी (प्रांताधिकारी) यांच्याकडून दिले जाणारे अधिकृत जात प्रमाणपत्र. आरक्षण, शैक्षणिक सवलती आणि नोकऱ्यांसाठी हे अत्यंत आवश्यक आहे.",
    "eligibility": [
      "Permanent resident of Maharashtra",
      "Must belong to an officially notified SC, ST, VJ, NT, SBC, or OBC community of Maharashtra with roots prior to state cutoff dates (1950/1961/1967)"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID", "name_mr": "आधार कार्ड / मतदार ओळखपत्र", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill", "name_mr": "रेशन कार्ड / वीज बिल", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "School Leaving Certificate / Primary School Register Extract (Applicant & Father/Grandfather)", "name_mr": "शाळा सोडल्याचा दाखला (स्वतःचा व वडिलांचा/आजोबांचा)", "description_en": "Showing caste entry prior to deemed cutoff date", "category": "other", "required": True},
      {"name_en": "Caste Certificate of Blood Relative", "name_mr": "रक्ताच्या नातेवाईकाचे जात प्रमाणपत्र", "description_en": "Father/Paternal uncle/Grandfather caste certificate or validity", "category": "other", "required": False},
      {"name_en": "Affidavit (Form 3 / 17)", "name_mr": "प्रतिज्ञापत्र", "description_en": "Affidavit for caste claim in prescribed format", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Login to Portal", "title_mr": "पोर्टलवर लॉगिन", "instructions_en": "Access Aaple Sarkar account.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Select Caste Service", "title_mr": "जात प्रमाणपत्र सेवा निवडा", "instructions_en": "Go to Revenue Department -> Caste Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Paternal Genealogy Proofs", "title_mr": "वंशावळीचे व जुने महसुली पुरावे जोडा", "instructions_en": "Fill caste category, sub-caste, lineage details and upload school and old revenue proofs.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Fee Payment", "title_mr": "शुल्क भरा", "instructions_en": "Pay statutory fee of ₹40 plus gateway charges and note Application ID.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 21,
    "statutory_fee_inr": 40.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Non-Creamy Layer Certificate",
    "name_mr": "नॉन-क्रीमी लेयर प्रमाणपत्र",
    "slug": "non-creamy-layer-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an OBC/VJNT/SBC category applicant's family income does not exceed the creamy layer threshold (₹8 Lakhs/year).",
    "short_description_mr": "ओबीसी/व्हीजेएनटी/एसबीसी प्रवर्गातील कुटुंबाचे वार्षिक उत्पन्न ८ लाख रुपयांपेक्षा कमी असल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "The Non-Creamy Layer (NCL) certificate enables beneficiaries of OBC, VJNT, and SBC categories to avail statutory reservation benefits in higher education admissions and public sector employment in Maharashtra.",
    "description_mr": "इतर मागास वर्ग, विमुक्त जाती आणि भटक्या जमाती प्रवर्गातील उमेदवारांना आरक्षणाचा लाभ मिळवण्यासाठी हे प्रमाणपत्र तहसीलदार/उपविभागीय अधिकाऱ्यांकडून दिले जाते.",
    "eligibility": [
      "Must possess a valid Caste Certificate under OBC, VJ, NT, or SBC category in Maharashtra",
      "Gross annual family income from all sources must be less than ₹8,00,000 for the last 3 consecutive financial years"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / PAN Card", "name_mr": "आधार कार्ड / पॅन कार्ड", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill", "name_mr": "रेशन कार्ड / वीज बिल", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "Caste Certificate", "name_mr": "जात प्रमाणपत्र", "description_en": "Applicant's Caste Certificate", "category": "other", "required": True},
      {"name_en": "3-Year Income Proof / ITR / Form 16", "name_mr": "मागील ३ वर्षांचा उत्पन्नाचा पुरावा", "description_en": "Income proof for last 3 financial years", "category": "income_proof", "required": True},
      {"name_en": "Self-Declaration Undertaking", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Declaration stating non-creamy layer status", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Login", "title_mr": "पोर्टल लॉगिन", "instructions_en": "Log in to Aaple Sarkar portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Service Navigation", "title_mr": "सेवा निवड", "instructions_en": "Select Revenue Department -> Non-Creamy Layer Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Submit 3-Year Income Figures", "title_mr": "३ वर्षांच्या उत्पन्नाची माहिती भरा", "instructions_en": "Fill father/mother occupation, agricultural landholding, and 3 years income breakdown.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Payment & Processing", "title_mr": "शुल्क भरणा व सबमिशन", "instructions_en": "Pay statutory fee of ₹50 online and submit application.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Economically Weaker Section (EWS) Certificate",
    "name_mr": "आर्थिकदृष्ट्या दुर्बल घटक पात्रता प्रमाणपत्र (EWS)",
    "slug": "economically-weaker-section-ews-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certificate providing 10% reservation in government jobs and educational institutions for General/Open category citizens.",
    "short_description_mr": "खुल्या प्रवर्गातील आर्थिकदृष्ट्या दुर्बल घटकांसाठी शासकीय नोकऱ्या व शिक्षणात १०% आरक्षण देणारा दाखला.",
    "description_en": "Issued to individuals belonging to the General/Open category who are not covered under SC, ST, or OBC reservation schemes and whose family gross annual income is below ₹8 Lakhs per annum.",
    "description_mr": "अनुसूचित जाती, जमाती किंवा इतर मागासवर्गात न मोडणाऱ्या खुल्या प्रवर्गातील कुटुंबांचे वार्षिक उत्पन्न ८ लाखांपेक्षा कमी असल्यास महसूल अधिकाऱ्यांमार्फत हे प्रमाणपत्र दिले जाते.",
    "eligibility": [
      "Permanent resident / Domiciled in Maharashtra",
      "Belongs to General/Open category (not covered under SC/ST/OBC/VJNT)",
      "Gross family annual income strictly below ₹8,00,000",
      "Agricultural landholding less than 5 acres and residential flat less than 1,000 sq ft"
    ],
    "documents": [
      {"name_en": "Aadhaar Card and PAN Card", "name_mr": "आधार कार्ड आणि पॅन कार्ड", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Domicile Certificate / Proof of Residence", "name_mr": "अधिवास प्रमाणपत्र / वास्तव्याचा पुरावा", "description_en": "Proof of Maharashtra domicile", "category": "address_proof", "required": True},
      {"name_en": "Tahsildar Income Certificate / ITR Statements", "name_mr": "तहसीलदार उत्पन्न दाखला / आयटीआर", "description_en": "Proof of annual income below ₹8 Lakhs", "category": "income_proof", "required": True},
      {"name_en": "School Leaving Certificate", "name_mr": "शाळा सोडल्याचा दाखला", "description_en": "Proof of belonging to Open/General category", "category": "other", "required": True},
      {"name_en": "7/12 & 8-A Extract or Property Document", "name_mr": "७/१२ व ८-अ उतारा किंवा मालमत्ता पत्रक", "description_en": "Proof of family asset holdings", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Access", "title_mr": "पोर्टलवर जा", "instructions_en": "Sign in to Aaple Sarkar portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Form Filling", "title_mr": "माहिती भरा", "instructions_en": "Select Revenue Department -> EWS Certificate. Enter family income and asset valuation.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Documentation", "title_mr": "कागदपत्रे अपलोड करा", "instructions_en": "Upload scanned income, open category proof, land holding, and residence proofs.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Submit & Pay", "title_mr": "शुल्क भरून अर्ज सादर करा", "instructions_en": "Pay statutory fee of ₹50 and submit for Tahsildar approval.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Senior Citizen Certificate",
    "name_mr": "ज्येष्ठ नागरिक प्रमाणपत्र",
    "slug": "senior-citizen-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official identification card and certificate verifying an individual has attained 60 years of age.",
    "short_description_mr": "व्यक्तीने वयाची ६० वर्षे पूर्ण केल्याचे प्रमाणित करणारे शासकीय ज्येष्ठ नागरिक ओळखपत्र व दाखला.",
    "description_en": "Issued by the Tahsildar to senior citizens aged 60 and above. Enables cardholders to avail concessions in public transport (MSRTC), priority healthcare in state hospitals, and specialized municipal welfare facilities.",
    "description_mr": "६० वर्षे किंवा त्याहून अधिक वयाच्या नागरिकांना शासकीय सवलती, एसटी बस प्रवास सवलत आणि आरोग्य सेवांचा प्राधान्याने लाभ मिळण्यासाठी हा दाखला दिला जातो.",
    "eligibility": [
      "Resident of Maharashtra",
      "Attained minimum age of 60 years"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / PAN Card / Passport", "name_mr": "आधार कार्ड / पॅन कार्ड / पासपोर्ट", "description_en": "Proof of Identity & Age", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill / Voter ID", "name_mr": "रेशन कार्ड / वीज बिल / मतदार ओळखपत्र", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "School Leaving Certificate / Birth Certificate", "name_mr": "शाळा सोडल्याचा दाखला / जन्म दाखला", "description_en": "Proof of Date of Birth", "category": "identity_proof", "required": True},
      {"name_en": "Passport Size Photograph", "name_mr": "पासपोर्ट आकाराचा फोटो", "description_en": "Applicant photo for card generation", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Login", "title_mr": "लॉगिन", "instructions_en": "Login to Aaple Sarkar portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Select Service", "title_mr": "सेवा निवडा", "instructions_en": "Go to Revenue Department -> Senior Citizen Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Proofs", "title_mr": "कागदपत्रे जोडा", "instructions_en": "Enter birth details, upload age proof and residential documents.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Download Certificate", "title_mr": "दाखला डाउनलोड करा", "instructions_en": "Receive approved digitally signed Senior Citizen certificate within 7 working days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 7,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Solvency Certificate",
    "name_mr": "ऐपतीचा दाखला / सधनता प्रमाणपत्र",
    "slug": "solvency-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certification of an individual's financial stability and unencumbered asset net worth.",
    "short_description_mr": "व्यक्तीची आर्थिक पत आणि संपत्तीचे मूल्य प्रमाणित करणारा सधनतेचा दाखला.",
    "description_en": "Issued by the Sub-Divisional Officer / Tahsildar to verify that an applicant holds unencumbered assets equal to or greater than the required solvency amount. Necessary for government tenders, bail bonds, court sureties, and customs warehousing.",
    "description_mr": "शासकीय कंत्राटे, न्यायालयीन जामीन किंवा निविदा प्रक्रियेसाठी संबंधित व्यक्तीची मालमत्ता व आर्थिक पत प्रमाणित करण्यासाठी हा दाखला दिला जातो.",
    "eligibility": [
      "Property/Asset owner resident in Maharashtra",
      "Possession of clear, unencumbered immovable/movable assets in the state"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / PAN Card", "name_mr": "आधार कार्ड / पॅन कार्ड", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill", "name_mr": "रेशन कार्ड / वीज बिल", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "7/12 & 8-A Extract or Property Card (PR Card)", "name_mr": "७/१२ व ८-अ उतारा किंवा मालमत्ता पत्रक", "description_en": "Land/building ownership proof", "category": "other", "required": True},
      {"name_en": "Government Approved Valuer Report", "name_mr": "शासकीय मूल्यांकन अहवाल", "description_en": "Property valuation certificate", "category": "other", "required": True},
      {"name_en": "No Encumbrance Certificate", "name_mr": "भारमुक्त प्रमाणपत्र (Non-Encumbrance)", "description_en": "Sub-Registrar non-encumbrance certificate", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Online Application", "title_mr": "ऑनलाईन अर्ज", "instructions_en": "Select Revenue Department -> Solvency Certificate on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Asset Declaration", "title_mr": "मालमत्ता माहिती", "instructions_en": "Specify required solvency sum and details of properties submitted as surety.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Valuation Reports", "title_mr": "मूल्यांकन अहवाल जोडा", "instructions_en": "Upload certified valuation, 7/12 extracts, and search reports.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Scrutiny & Issuance", "title_mr": "पडताळणी व दाखला प्राप्ती", "instructions_en": "Tahsildar conducts field inquiry and issues certificate within 21 working days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Agriculturist Certificate",
    "name_mr": "शेतकरी असल्याचा दाखला",
    "slug": "agriculturist-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an individual or ancestral family holds lawful agricultural land cultivation status.",
    "short_description_mr": "अर्जदार किंवा त्याचे कुटुंबीय अधिकृत शेतकरी असल्याचे सिद्ध करणारा दाखला.",
    "description_en": "Under the Maharashtra Tenancy and Agricultural Lands Act, only a recognized farmer can buy agricultural land in Maharashtra. This certificate validates the farmer status of an applicant based on land revenue records.",
    "description_mr": "महाराष्ट्रात शेतजमीन खरेदी करण्यासाठी व्यक्ती शेतकरी असणे आवश्यक आहे. अर्जदार शेतकरी असल्याचा पुरावा म्हणून तहसीलदार हा दाखला देतात.",
    "eligibility": [
      "Individual owning or cultivating agricultural land in Maharashtra or an ancestral farmer lineage"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID", "name_mr": "आधार कार्ड / मतदार ओळखपत्र", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Address Proof", "name_mr": "रेशन कार्ड / पत्त्याचा पुरावा", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "7/12 Extract and 8-A Extract", "name_mr": "७/१२ आणि ८-अ उतारा", "description_en": "Recent agricultural land record extracts", "category": "other", "required": True},
      {"name_en": "Self-Declaration", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Standard declaration of farming activity", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Login to Portal", "title_mr": "पोर्टल लॉगिन", "instructions_en": "Access Aaple Sarkar portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Select Service", "title_mr": "सेवा निवडा", "instructions_en": "Navigate to Revenue Department -> Agriculturist Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Link Land Records", "title_mr": "जमीन माहिती भरा", "instructions_en": "Provide District, Taluka, Village, and Survey/Gat number of the farm.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Verification & Issuance", "title_mr": "पडताळणी व दाखला", "instructions_en": "Talathi and Tahsildar verify Mahabhulekh records and issue certificate within 15 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Small Land Holder Farmer Certificate",
    "name_mr": "अल्पभूधारक शेतकरी प्रमाणपत्र",
    "slug": "small-land-holder-farmer-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that a farmer owns agricultural land within smallholder limits (up to 2 hectares / 5 acres).",
    "short_description_mr": "शेतकऱ्याकडे कमाल २ हेक्टर (५ एकर) पर्यंत शेतजमीन असल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Tahsildar to verify small and marginal farmer status. Necessary for claiming state agriculture subsidies (drip irrigation, farm machinery, solar pumps) and subsidized credit schemes.",
    "description_mr": "शासकीय कृषी योजना, ठिबक सिंचन अनुदान, बी-बियाणे सवलत आणि कृषी कर्जासाठी अल्पभूधारक दाखला अत्यंत महत्त्वाचा आहे.",
    "eligibility": [
      "Cultivator whose total family agricultural land ownership does not exceed 2 hectares (5 acres) of dryland (or 1 hectare irrigated)"
    ],
    "documents": [
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Identity Proof", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card", "name_mr": "रेशन कार्ड", "description_en": "Address Proof", "category": "address_proof", "required": True},
      {"name_en": "Latest 7/12 & 8-A Extract", "name_mr": "नवीनतम ७/१२ आणि ८-अ उतारा", "description_en": "Land records showing exact acreage", "category": "other", "required": True},
      {"name_en": "Self-Declaration", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Declaration of total family landholdings across all villages", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Application", "title_mr": "पोर्टलवर अर्ज", "instructions_en": "Go to Revenue Department -> Small Land Holder Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Enter Landholdings", "title_mr": "जमीन क्षेत्र नोंदवा", "instructions_en": "Enter Gat number and verified acreage as per 8-A register.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Documents", "title_mr": "कागदपत्रे अपलोड करा", "instructions_en": "Upload scanned land documents and self-declaration.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Payment & Download", "title_mr": "शुल्क व दाखला प्राप्ती", "instructions_en": "Pay fee and receive digital certificate within 15 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Digitally Signed 7/12 Extract (Digital Satbara)",
    "name_mr": "डिजिटल स्वाक्षरीत ७/१२ उतारा",
    "slug": "digitally-signed-7-12-extract",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Legally valid, digitally signed land record extract depicting ownership, survey numbers, crops, and encumbrances.",
    "short_description_mr": "जमीन मालकी हक्क, गट क्रमांक, पिकांची नोंद व बोजा दर्शवणारा कायदेशीर डिजिटल स्वाक्षरीत सातबारा उतारा.",
    "description_en": "Integrated into Aaple Sarkar and Mahabhumi, this service issues instant digitally signed copies of Village Form VII and XII with a verifiable QR code. Admissible in all courts, banks, and sub-registrar offices without requiring a manual Talathi signature.",
    "description_mr": "महाभूमी आणि आपले सरकार पोर्टलद्वारे डिजिटल स्वाक्षरी असलेला ७/१२ उतारा त्वरित उपलब्ध होतो. बँक कर्ज, जमीन खरेदी-विक्री आणि न्यायालयीन कामांसाठी हा ग्राह्य धरला जातो.",
    "eligibility": [
      "Any citizen seeking legal land record extract for any plot/gat in Maharashtra"
    ],
    "documents": [
      {"name_en": "Survey / Gat Number & Village Details", "name_mr": "गट/सर्व्हे नंबर व गाव तपशील", "description_en": "District, Taluka, Village, and Survey/Gat Number", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Access Digital Satbara", "title_mr": "पोर्टल उघडा", "instructions_en": "Visit Aaple Sarkar / Digital Satbara portal.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 2, "title_en": "Select Land Location", "title_mr": "जमीन स्थान निवडा", "instructions_en": "Select District, Taluka, Village, and enter Survey / Gat Number.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 3, "title_en": "Pay Fee", "title_mr": "शुल्क भरा", "instructions_en": "Pay ₹15 per 7/12 extract via online wallet/UPI.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 4, "title_en": "Instant Download", "title_mr": "त्वरित डाऊनलोड करा", "instructions_en": "Instantly download PDF with digital signature and QR verification code.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"}
    ],
    "processing_days": 1,
    "statutory_fee_inr": 15.00,
    "source_url": "https://digitalsatbara.mahabhumi.gov.in"
  },
  {
    "name_en": "Digitally Signed Ferfar / Mutation Extract (Form 6)",
    "name_mr": "डिजिटल स्वाक्षरीत फेरफार उतारा (गाव नमुना ६)",
    "slug": "digitally-signed-ferfar-extract",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Digitally signed copy of Village Form 6 (Mutation Register) documenting historical changes in land title.",
    "short_description_mr": "जमिनीच्या मालकी हक्कात झालेल्या बदलांची नोंद दाखवणारा डिजिटल स्वाक्षरीत फेरफार (गाव नमुना ६) उतारा.",
    "description_en": "Provides the complete mutation entry extract reflecting land transfers via sale deed, partition, gift, legal heir registration (Varas), or bank loan hypothecation. Crucial for title due diligence.",
    "description_mr": "खरेदी-विक्री, वारस नोंद, वाटप किंवा कर्जाच्या बोज्यामुळे सातबाऱ्यावर झालेल्या बदलांचा कायदेशीर इतिहास फेरफार उताऱ्यावरून समजतो.",
    "eligibility": [
      "Any landowner, prospective buyer, or citizen checking land title history"
    ],
    "documents": [
      {"name_en": "Ferfar Number & Village Name", "name_mr": "फेरफार नंबर व गावाचे नाव", "description_en": "Mutation number and village details", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Visit", "title_mr": "पोर्टलला भेट द्या", "instructions_en": "Navigate to Aaple Sarkar / Mahabhumi digital portal.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 2, "title_en": "Enter Ferfar Details", "title_mr": "तपशील भरा", "instructions_en": "Input District, Taluka, Village, and Ferfar Number.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 3, "title_en": "Online Payment", "title_mr": "शुल्क भरणा", "instructions_en": "Pay ₹15 statutory fee online.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"},
      {"step_number": 4, "title_en": "Download Extract", "title_mr": "उतारा डाऊनलोड", "instructions_en": "Instantly download digitally signed e-Ferfar copy with QR code.", "external_url": "https://digitalsatbara.mahabhumi.gov.in"}
    ],
    "processing_days": 1,
    "statutory_fee_inr": 15.00,
    "source_url": "https://digitalsatbara.mahabhumi.gov.in"
  },
  {
    "name_en": "Birth Certificate (Rural)",
    "name_mr": "जन्म नोंदणी दाखला (ग्रामीण)",
    "slug": "birth-certificate-rural",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development and Panchayat Raj Department",
    "dept_name_mr": "ग्रामविकास व पंचायत राज विभाग",
    "short_description_en": "Official registration and certificate of a child's birth in a Gram Panchayat jurisdiction.",
    "short_description_mr": "ग्रामपंचायत हद्दीत झालेल्या बालकाच्या जन्माचा अधिकृत नोंदणी दाखला.",
    "description_en": "Issued by the Village Development Officer (Gram Sevak) acting as the Local Registrar under the Registration of Births and Deaths Act. Serves as conclusive proof of age and identity for school admissions, passports, and government IDs.",
    "description_mr": "ग्रामविकास विभागामार्फत ग्रामसेवक/रजिस्ट्रार यांच्याकडून ग्रामपंचायत हद्दीतील जन्म नोंदीचा दाखला दिला जातो. शाळा प्रवेश, आधार व पासपोर्टसाठी हा अनिवार्य आहे.",
    "eligibility": [
      "Child born within the territorial limits of the Gram Panchayat in Maharashtra"
    ],
    "documents": [
      {"name_en": "Hospital Birth Discharge Summary / Form 1", "name_mr": "हॉस्पिटल डिस्चार्ज कार्ड / फॉर्म १", "description_en": "Proof of birth issued by PHC / hospital", "category": "other", "required": True},
      {"name_en": "Parents' Aadhaar Cards", "name_mr": "आई-वडिलांचे आधार कार्ड", "description_en": "Identity proof of father and mother", "category": "identity_proof", "required": True},
      {"name_en": "Self-Declaration Form", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Declaration of birth particulars", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Login to Aaple Sarkar", "title_mr": "आपले सरकार लॉगिन", "instructions_en": "Login to portal and select Rural Development -> Birth Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Enter Birth Data", "title_mr": "जन्म तपशील नोंदवा", "instructions_en": "Enter child's name, gender, date of birth, place of birth, and parents details.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Documents", "title_mr": "कागदपत्रे अपलोड करा", "instructions_en": "Upload hospital report and parents' ID proofs.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Verification & Issuance", "title_mr": "पडताळणी व दाखला", "instructions_en": "Gram Sevak approves and issues certificate within 5 working days (free if reported within 21 days).", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Death Certificate (Rural)",
    "name_mr": "मृत्यू नोंदणी दाखला (ग्रामीण)",
    "slug": "death-certificate-rural",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development and Panchayat Raj Department",
    "dept_name_mr": "ग्रामविकास व पंचायत राज विभाग",
    "short_description_en": "Official certificate confirming the registration of a person's death within a Gram Panchayat.",
    "short_description_mr": "ग्रामपंचायत हद्दीत झालेल्या व्यक्तीच्या मृत्यूची अधिकृत नोंद प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Gram Sevak / Registrar under the Registration of Births and Deaths Act. Indispensable for legal heir succession, insurance claims, pension transfers, and property title mutations.",
    "description_mr": "मृत्यूची अधिकृत नोंद करून ग्रामसेवकांमार्फत हा दाखला दिला जातो. वारस नोंद, विमा दावा, बँक खात्यातील रक्कम मिळवण्यासाठी हा दाखला लागतो.",
    "eligibility": [
      "Death occurred within the jurisdiction of the concerned Gram Panchayat"
    ],
    "documents": [
      {"name_en": "Medical Certificate of Cause of Death / Form 4", "name_mr": "मृत्यू दाखला (डॉक्टर/रुग्णालय)", "description_en": "Doctor's / Hospital death report", "category": "other", "required": True},
      {"name_en": "Cremation / Burial Ground Receipt", "name_mr": "दफनभूमी/स्मशानभूमी पावती", "description_en": "Proof of cremation or burial", "category": "other", "required": True},
      {"name_en": "Deceased Person's Aadhaar / Voter ID", "name_mr": "मृत व्यक्तीचा ओळख पुरावा", "description_en": "Identity proof of deceased", "category": "identity_proof", "required": True},
      {"name_en": "Applicant's Identity Proof", "name_mr": "अर्जदाराचा ओळख पुरावा", "description_en": "Proof of relation of the informant", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Application", "title_mr": "पोर्टलवर अर्ज", "instructions_en": "Select Rural Development -> Death Certificate on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Provide Death Details", "title_mr": "मृत्यू तपशील नोंदवा", "instructions_en": "Enter deceased details, date, cause, and exact place of death.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Records", "title_mr": "पुरावे जोडा", "instructions_en": "Upload hospital certificate and cremation receipt.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Download Certificate", "title_mr": "दाखला डाऊनलोड करा", "instructions_en": "Gram Sevak issues certificate within 5 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Marriage Registration Certificate (Gram Panchayat)",
    "name_mr": "विवाह नोंदणी प्रमाणपत्र (ग्रामपंचायत)",
    "slug": "marriage-registration-certificate-rural",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development and Panchayat Raj Department",
    "dept_name_mr": "ग्रामविकास व पंचायत राज विभाग",
    "short_description_en": "Statutory registration of a marriage solemnized within a Gram Panchayat jurisdiction.",
    "short_description_mr": "ग्रामपंचायत हद्दीत झालेल्या विवाहाची अधिकृत नोंदणी व प्रमाणपत्र.",
    "description_en": "Issued under the Maharashtra Regulation of Marriage Bureaus and Registration of Marriages Act, 1998 by the Gram Sevak. Mandatory for passport applications with spouse name, joint property purchases, visa processing, and spousal benefits.",
    "description_mr": "विवाह नोंदणी कायद्यानुसार ग्रामपंचायत हद्दीतील विवाहांची नोंद करून ग्रामसेवक हे प्रमाणपत्र देतात. पासपोर्ट, बँक खाते आणि कायदेशीर हक्कांसाठी हे आवश्यक आहे.",
    "eligibility": [
      "Groom aged 21 or older; Bride aged 18 or older",
      "Marriage solemnized in the Gram Panchayat or either spouse residing in the village"
    ],
    "documents": [
      {"name_en": "Marriage Invitation Card / Priest Certificate", "name_mr": "लग्नपत्रिका / भटजींचे प्रमाणपत्र", "description_en": "Proof of solemnization of marriage", "category": "other", "required": True},
      {"name_en": "Bride & Groom Age & Identity Proof", "name_mr": "वर-वधूचे वय व ओळख पुरावे", "description_en": "Aadhaar Card, School Leaving Certificate", "category": "identity_proof", "required": True},
      {"name_en": "Photographs of Couple", "name_mr": "दाम्पत्याचे छायाचित्र", "description_en": "Joint photograph and wedding ceremony photo", "category": "other", "required": True},
      {"name_en": "Witness ID Proofs (3 Witnesses)", "name_mr": "३ साक्षीदारांचे ओळख पुरावे", "description_en": "Aadhaar cards of 3 witnesses who attended the wedding", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Fill Memorandum", "title_mr": "विवाह नोंदणी अर्ज भरा", "instructions_en": "Fill Form D Marriage Memorandum on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Upload Proofs & Photos", "title_mr": "कागदपत्रे व फोटो जोडा", "instructions_en": "Upload wedding card, bride/groom IDs, witness details, and photos.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Pay Statutory Fee", "title_mr": "शुल्क भरा", "instructions_en": "Pay ₹50 statutory fee online.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Sign Register & Download", "title_mr": "स्वाक्षरी व दाखला प्राप्ती", "instructions_en": "Spouses sign marriage register before Gram Sevak and receive digital certificate within 5 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 5,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Property Tax Assessment List Extract (Namuna 8)",
    "name_mr": "मालमत्ता कर आकारणी नोंदवही उतारा (नमुना ८)",
    "slug": "property-assessment-extract-namuna-8",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development and Panchayat Raj Department",
    "dept_name_mr": "ग्रामविकास व पंचायत राज विभाग",
    "short_description_en": "Extract of Gram Panchayat property assessment register proving ownership, area, and tax dues.",
    "short_description_mr": "ग्रामपंचायत हद्दीतील घराची किंवा जागेची अधिकृत मालकी व कर आकारणी दर्शवणारा नमुना ८ उतारा.",
    "description_en": "Namuna 8 (Form 8) is the rural municipal equivalent of a Property Card. It records the owner's name, house number, construction type, built-up area, and annual tax assessment in the village.",
    "description_mr": "गावातील घर, जागा किंवा इमारतीची ग्रामपंचायतीकडील अधिकृत मालकी सिद्ध करण्यासाठी नमुना ८ उतारा आवश्यक असतो. घर खरेदी-विक्री व बँक कर्जासाठी हा वापरला जातो.",
    "eligibility": [
      "Owner or lawful occupier of residential/commercial property in a Gram Panchayat"
    ],
    "documents": [
      {"name_en": "Property House Number / Assessment Details", "name_mr": "घर नंबर / मालमत्ता क्रमांक", "description_en": "Gram Panchayat property identification", "category": "other", "required": True},
      {"name_en": "Identity Proof of Owner", "name_mr": "मालकाचा ओळख पुरावा", "description_en": "Aadhaar Card / Voter ID", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Search", "title_mr": "पोर्टलवर शोधा", "instructions_en": "Select Rural Development -> Namuna 8 Extract on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Select Gram Panchayat", "title_mr": "ग्रामपंचायत निवडा", "instructions_en": "Select District, Taluka, Gram Panchayat, and enter House / Property Number.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Pay Nominal Fee", "title_mr": "शुल्क भरा", "instructions_en": "Pay ₹20 online fee.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Download Extract", "title_mr": "उतारा डाऊनलोड", "instructions_en": "Download digitally signed Namuna 8 extract within 5 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Post-Matric Scholarship Scheme (MahaDBT)",
    "name_mr": "मॅट्रिकोत्तर शिष्यवृत्ती योजना (महाडीबीटी)",
    "slug": "mahadbt-post-matric-scholarship",
    "dept_code": "SOC_JUSTICE",
    "dept_name_en": "Social Justice and Special Assistance Department",
    "dept_name_mr": "सामाजिक न्याय व विशेष सहाय्य विभाग",
    "short_description_en": "State scholarship providing tuition fee waiver and maintenance allowance for post-secondary college students in Maharashtra.",
    "short_description_mr": "महाराष्ट्रातील उच्च शिक्षण घेणाऱ्या विद्यार्थ्यांसाठी परीक्षा फी, शिक्षण शुल्क माफी आणि निर्वाह भत्ता देणारी राज्य शिष्यवृत्ती योजना.",
    "description_en": "Administered by the Social Justice & Special Assistance Department via the central MahaDBT portal. Provides financial support to eligible SC, ST, OBC, VJNT, and SBC students pursuing higher education.",
    "description_mr": "सामाजिक न्याय व विशेष सहाय्य विभागामार्फत महाडीबीटी पोर्टलद्वारे थेट बँक खात्यात शिष्यवृत्ती वितरित केली जाते. मागासवर्गीय विद्यार्थ्यांना शिक्षणासाठी शुल्क सवलत मिळते.",
    "eligibility": [
      "Maharashtra Domicile student enrolled in recognized post-matric course",
      "Family annual income limits according to caste category (SC/ST <= ₹2.5L, OBC/VJNT/SBC <= ₹1.5L for freeship / ₹1.0L for scholarship)"
    ],
    "documents": [
      {"name_en": "Caste Certificate & Caste Validity Certificate", "name_mr": "जात प्रमाणपत्र व जात पडताळणी प्रमाणपत्र", "description_en": "Authenticating reserved category status", "category": "other", "required": True},
      {"name_en": "Income Certificate issued by Tahsildar", "name_mr": "तहसीलदार उत्पन्न दाखला", "description_en": "Current financial year family income", "category": "income_proof", "required": True},
      {"name_en": "Domicile Certificate", "name_mr": "अधिवास दाखला", "description_en": "Proof of residence in Maharashtra", "category": "address_proof", "required": True},
      {"name_en": "College Fee Receipt & Allotment Letter", "name_mr": "कॉलेज फी पावती व प्रवेश पत्र", "description_en": "Admission proof under CAP / merit round", "category": "other", "required": True},
      {"name_en": "Aadhaar Linked Bank Account Passbook", "name_mr": "आधार संलग्न बँक पासबुक", "description_en": "Bank details with active DBT seeding", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Aadhaar-authenticated Login", "title_mr": "आधार आधारित नोंदणी", "instructions_en": "Register and log in on MahaDBT portal with biometric/OTP Aadhaar auth.", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 2, "title_en": "Create Profile", "title_mr": "प्रोफाइल तयार करा", "instructions_en": "Complete 6-step profile: Personal, Address, Other, Caste, Income, and Hostel details.", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 3, "title_en": "Select Scheme & Apply", "title_mr": "योजना निवडून अर्ज करा", "instructions_en": "Choose Department -> Social Justice -> Post-Matric Scholarship Scheme and select current course.", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 4, "title_en": "College Verification & Disbursement", "title_mr": "कॉलेज पडताळणी व शिष्यवृत्ती वाटप", "instructions_en": "College scrutinizes documents online; scholarship funds directly credited to bank account.", "external_url": "https://mahadbt.maharashtra.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 0.00,
    "source_url": "https://mahadbt.maharashtra.gov.in"
  },
  {
    "name_en": "Ration Card (New / Separate)",
    "name_mr": "नवीन / विभक्त रेशन कार्ड",
    "slug": "new-ration-card",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection Department",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Official entitlement card for subsidised food grains under the National Food Security Act (NFSA).",
    "short_description_mr": "राष्ट्रीय अन्न सुरक्षा कायद्यांतर्गत रास्त भाव दुकानातून अनुदानित अन्नधान्य मिळवण्यासाठीचे अधिकृत रेशन कार्ड.",
    "description_en": "Issued by the District Food and Civil Supplies Officer / Tahsildar. Serves as an essential proof of family composition and address for obtaining food security and state welfare benefits.",
    "description_mr": "तहसीलदार किंवा जिल्हा पुरवठा अधिकाऱ्यांमार्फत कुटुंबातील सदस्यांची नोंद असणारे रेशन कार्ड दिले जाते. स्वस्त धान्य, शासकीय योजना आणि पत्त्याचा पुरावा म्हणून हे वापरले जाते.",
    "eligibility": [
      "Citizen of India residing in Maharashtra",
      "Must not possess any other active ration card in India"
    ],
    "documents": [
      {"name_en": "Aadhaar Card of all family members", "name_mr": "कुटुंबातील सर्व सदस्यांचे आधार कार्ड", "description_en": "Proof of identity and family composition", "category": "identity_proof", "required": True},
      {"name_en": "Proof of Residence (Electricity bill / Property tax / Rent agreement)", "name_mr": "वास्तव्याचा पुरावा (वीज बिल / कर पावती / भाडेकरार)", "description_en": "Current residential address proof", "category": "address_proof", "required": True},
      {"name_en": "Surrender / Deletion Certificate from previous Ration Card", "name_mr": "पूर्वीच्या रेशन कार्डमधून नाव वगळल्याचा दाखला", "description_en": "Mandatory if previously included in parents' card", "category": "other", "required": True},
      {"name_en": "Income Certificate / Proof", "name_mr": "उत्पन्नाचा दाखला", "description_en": "To determine AAY / BPL / APL category", "category": "income_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Login", "title_mr": "पोर्टल लॉगिन", "instructions_en": "Sign in to Aaple Sarkar / RCMS portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Fill Family Details", "title_mr": "कुटुंबाचा तपशील भरा", "instructions_en": "Fill Head of Family (preferably woman) and all family members' Aadhaar details.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Proofs & Deletion Slip", "title_mr": "पुरावे जोडा", "instructions_en": "Upload scanned address proof, identity proofs, and name deletion certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Physical Verification & Card Issue", "title_mr": "पडताळणी व रेशन कार्ड प्राप्ती", "instructions_en": "Supply inspector verifies details and booklet is printed within 30 working days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 45.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Police Clearance Certificate (PCC / Character Certificate)",
    "name_mr": "पोलीस चारित्र्य पडताळणी प्रमाणपत्र",
    "slug": "police-clearance-certificate",
    "dept_code": "HOME_DEPT",
    "dept_name_en": "Home Department (Maharashtra Police)",
    "dept_name_mr": "गृह विभाग (महाराष्ट्र पोलीस)",
    "short_description_en": "Official background verification report certifying that an individual has no adverse criminal record.",
    "short_description_mr": "संबंधित व्यक्तीवर कोणताही फौजदारी गुन्हा दाखल नसल्याचे पोलीस पडताळणी प्रमाणपत्र.",
    "description_en": "Issued by the Superintendent of Police / Commissioner of Police via the Aaple Sarkar Citizen Portal (CCTNS). Required for government employment, private IT security clearances, school bus driver hiring, and overseas travel/visa.",
    "description_mr": "पोलीस आयुक्तालय किंवा जिल्हा पोलीस अधीक्षकांमार्फत गुन्हेगारी पार्श्वभूमी पडताळून हे चारित्र्य प्रमाणपत्र दिले जाते. शासकीय नोकऱ्या, परदेशी व्हिसा व सुरक्षा कामांसाठी हे अनिवार्य आहे.",
    "eligibility": [
      "Indian citizen residing within the jurisdiction of Maharashtra Police"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID / Passport", "name_mr": "आधार कार्ड / पासपोर्ट / मतदार ओळखपत्र", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Current Address Proof (Utility bill / Rent agreement)", "name_mr": "सध्याच्या पत्त्याचा पुरावा", "description_en": "Proof of residence in current police station limit", "category": "address_proof", "required": True},
      {"name_en": "Letter from Employer or Institution", "name_mr": "संस्थेचे शिफारस पत्र", "description_en": "Letter requesting character verification", "category": "other", "required": False},
      {"name_en": "Passport Size Photograph", "name_mr": "पासपोर्ट फोटो", "description_en": "Recent color photograph", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Online PCC Registration", "title_mr": "ऑनलाईन नोंदणी", "instructions_en": "Log in to Aaple Sarkar / PCS Police portal and select Character Verification.", "external_url": "https://pcs.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Provide Address History", "title_mr": "पत्त्याचा इतिहास द्या", "instructions_en": "Provide residential address history for the last 3 years and select jurisdictional police station.", "external_url": "https://pcs.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Pay Verification Fee", "title_mr": "पडताळणी शुल्क भरा", "instructions_en": "Pay statutory fee of ₹123.60 online.", "external_url": "https://pcs.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Police Station Visit & Download", "title_mr": "पोलीस ठाण्यात पडताळणी व दाखला", "instructions_en": "Visit local police station for physical document verification; download digitally signed PCC in 15 days.", "external_url": "https://pcs.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 123.60,
    "source_url": "https://pcs.mahaonline.gov.in"
  },
  {
    "name_en": "Shop and Establishment Registration (Gumasta License / Intimation)",
    "name_mr": "दुकाने व आस्थापना नोंदणी (गुमास्ता परवाना / सूचना पत्र)",
    "slug": "gumasta-shop-act-registration",
    "dept_code": "LABOUR_DEPT",
    "dept_name_en": "Labour Department",
    "dept_name_mr": "कामगार विभाग",
    "short_description_en": "Statutory registration for commercial establishments, offices, and shops under the Maharashtra Shops Act.",
    "short_description_mr": "महाराष्ट्र दुकाने व आस्थापना कायद्यांतर्गत व्यवसाय, कार्यालय किंवा दुकानाची अधिकृत नोंदणी (गुमास्ता).",
    "description_en": "Issued under the Maharashtra Shops and Establishments (Regulation of Employment and Conditions of Service) Act, 2017. Establishments with 0 to 9 workers obtain an online Form F Intimation receipt, while 10+ employees receive Form C Registration.",
    "description_mr": "कामगार विभागाकडून दिला जाणारा गुमास्ता परवाना दुकाने व व्यावसायिक आस्थापनांसाठी अनिवार्य आहे. बँक चालू खाते (Current Account) उघडण्यासाठी व जीएसटी नोंदणीसाठी हा दाखला लागतो.",
    "eligibility": [
      "Any individual, partnership, LLP, or company operating a commercial shop or establishment in Maharashtra"
    ],
    "documents": [
      {"name_en": "Aadhaar Card and PAN Card of Proprietor / Partners", "name_mr": "मालकाचे आधार कार्ड आणि पॅन कार्ड", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Shop / Office Electricity Bill & Rent Agreement / Property Tax", "name_mr": "दुकानाचे वीज बिल व भाडेकरार / कर पावती", "description_en": "Proof of business premises", "category": "address_proof", "required": True},
      {"name_en": "Photo of Shop Front with Signboard in Marathi Devanagari", "name_mr": "मराठी नामफलकासह दुकानाचा समोरचा फोटो", "description_en": "Signboard in Marathi script as required by law", "category": "other", "required": True},
      {"name_en": "Self-Declaration of Undertaking", "name_mr": "हमीपत्र / स्वयंघोषणा पत्र", "description_en": "Compliance declaration under Shops Act", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Login", "title_mr": "पोर्टल लॉगिन", "instructions_en": "Log in to Aaple Sarkar / Labour Department portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Select Category", "title_mr": "प्रवर्ग निवडा", "instructions_en": "Choose Intimation (0-9 workers) or Registration (10+ workers).", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Upload Signboard Photo & Address Proof", "title_mr": "फोटो व कागदपत्रे जोडा", "instructions_en": "Upload business address proof, photo with Marathi signboard, and ID.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Instant Download", "title_mr": "त्वरित प्रमाणपत्र डाऊनलोड", "instructions_en": "Pay fee and instantly download digitally signed Form F Intimation or Form C Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 1,
    "statutory_fee_inr": 23.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Disability Certificate (Divyangjan Certificate / UDID)",
    "name_mr": "दिव्यांगत्व प्रमाणपत्र (UDID)",
    "slug": "disability-certificate-udid",
    "dept_code": "PUBLIC_HEALTH",
    "dept_name_en": "Public Health Department",
    "dept_name_mr": "सार्वजनिक आरोग्य विभाग",
    "short_description_en": "Official medical disability certificate and Unique Disability ID (UDID) card for individuals with benchmark disabilities.",
    "short_description_mr": "४०% किंवा त्याहून अधिक दिव्यांगत्व असणाऱ्या व्यक्तींसाठी अधिकृत वैद्यकीय प्रमाणपत्र व UDID कार्ड.",
    "description_en": "Issued by the District Medical Board under the Civil Surgeon. Certifies benchmark disability (40% or above), entitling beneficiaries to state pensions (Sanjay Gandhi Niradhar Yojana), bus/railway travel concessions, and educational reservations.",
    "description_mr": "जिल्हा शल्यचिकित्सक (सिव्हिल सर्जन) यांच्या अध्यक्षतेखालील वैद्यकीय मंडळाकडून तपासणी करून हे प्रमाणपत्र दिले जाते. शासकीय योजना, मोफत एसटी प्रवास व पेन्शनसाठी हे आवश्यक आहे.",
    "eligibility": [
      "Resident of Maharashtra with a diagnosed physical, sensory, intellectual, or neurological disability"
    ],
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID", "name_mr": "आधार कार्ड / मतदार ओळखपत्र", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Electricity Bill", "name_mr": "रेशन कार्ड / पत्त्याचा पुरावा", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "Medical Treatment Records / Hospital Reports", "name_mr": "वैद्यकीय उपचारांचे कागदपत्र", "description_en": "Previous medical history from specialist doctor", "category": "other", "required": True},
      {"name_en": "Passport Size Photographs showing disability", "name_mr": "दिव्यांगत्व स्पष्ट दिसणारे पासपोर्ट फोटो", "description_en": "Recent color photographs", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Online Registration", "title_mr": "ऑनलाईन नोंदणी", "instructions_en": "Register on Aaple Sarkar or Swavlamban UDID portal.", "external_url": "https://swavlambancard.gov.in"},
      {"step_number": 2, "title_en": "Upload Clinical Records", "title_mr": "वैद्यकीय नोंदी अपलोड करा", "instructions_en": "Fill disability type, upload ID, residence proof, and medical reports.", "external_url": "https://swavlambancard.gov.in"},
      {"step_number": 3, "title_en": "Hospital Assessment Visit", "title_mr": "रुग्णालयात तपासणी", "instructions_en": "Visit District Civil Hospital on designated date for clinical evaluation by medical board.", "external_url": "https://swavlambancard.gov.in"},
      {"step_number": 4, "title_en": "Digital Certificate & UDID Card", "title_mr": "प्रमाणपत्र व UDID कार्ड प्राप्ती", "instructions_en": "Download digital certificate and receive permanent plastic UDID card by post.", "external_url": "https://swavlambancard.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 0.00,
    "source_url": "https://swavlambancard.gov.in"
  }
]

def update_seed():
    print("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Ensure state
        mh_state = db.query(State).filter_by(code="MH").first()
        if not mh_state:
            mh_state = State(name="Maharashtra", code="MH")
            db.add(mh_state)
            db.flush()

        # Ensure district
        pune_district = db.query(District).filter_by(code="PUN").first()
        if not pune_district:
            pune_district = District(name="Pune", code="PUN", state_id=mh_state.id)
            db.add(pune_district)
            db.flush()

        # Ensure main source
        aaple_source = db.query(Source).filter_by(url="https://aaplesarkar.mahaonline.gov.in").first()
        if not aaple_source:
            aaple_source = Source(
                title="Aaple Sarkar Citizen Services Portal - Government of Maharashtra",
                url="https://aaplesarkar.mahaonline.gov.in",
                publisher="Government of Maharashtra",
                source_type="official",
                supports="statutory_fees,processing_timelines,document_checklists,steps"
            )
            db.add(aaple_source)
            db.flush()

        for s_data in SERVICES_DATA:
            # 1. Department
            dept = db.query(Department).filter_by(code=s_data["dept_code"]).first()
            if not dept:
                dept = Department(
                    code=s_data["dept_code"],
                    name_en=s_data["dept_name_en"],
                    name_mr=s_data.get("dept_name_mr", s_data["dept_name_en"]),
                    name_hi=s_data["dept_name_en"],
                    portal_url=s_data.get("source_url", "https://aaplesarkar.mahaonline.gov.in")
                )
                db.add(dept)
                db.flush()

            # 2. Service
            svc = db.query(Service).filter_by(slug=s_data["slug"]).first()
            if not svc:
                svc = Service(
                    slug=s_data["slug"],
                    name_en=s_data["name_en"],
                    name_mr=s_data["name_mr"],
                    name_hi=s_data["name_en"],
                    short_description_en=s_data["short_description_en"],
                    short_description_mr=s_data["short_description_mr"],
                    short_description_hi=s_data["short_description_en"],
                    description_en=s_data["description_en"],
                    description_mr=s_data["description_mr"],
                    description_hi=s_data["description_en"],
                    department_id=dept.id,
                    jurisdiction_level="state",
                    state="Maharashtra",
                    statutory_fee_inr=s_data["statutory_fee_inr"],
                    processing_days=s_data["processing_days"],
                    official_portal_url=s_data["source_url"],
                    official_tracking_url="https://aaplesarkar.mahaonline.gov.in/en/TrackStatus",
                    verification_status="verified",
                    is_demo=False
                )
                svc.districts.append(pune_district)
                svc.sources.append(aaple_source)
                db.add(svc)
                db.flush()
                print(f"Created service: {s_data['name_en']}")
            else:
                # Update existing service with rich data
                svc.name_en = s_data["name_en"]
                svc.name_mr = s_data["name_mr"]
                svc.short_description_en = s_data["short_description_en"]
                svc.short_description_mr = s_data["short_description_mr"]
                svc.description_en = s_data["description_en"]
                svc.description_mr = s_data["description_mr"]
                svc.statutory_fee_inr = s_data["statutory_fee_inr"]
                svc.processing_days = s_data["processing_days"]
                svc.official_portal_url = s_data["source_url"]
                svc.verification_status = "verified"
                svc.is_demo = False
                print(f"Updated service: {s_data['name_en']}")

            # 3. Documents
            db.query(ServiceDocument).filter_by(service_id=svc.id).delete()
            for idx, doc in enumerate(s_data.get("documents", [])):
                sdoc = ServiceDocument(
                    service_id=svc.id,
                    name_en=doc["name_en"],
                    name_mr=doc.get("name_mr", doc["name_en"]),
                    name_hi=doc["name_en"],
                    category=doc.get("category", "identity_proof"),
                    is_mandatory=doc.get("required", True),
                    description_en=doc.get("description_en", ""),
                    display_order=idx + 1
                )
                db.add(sdoc)

            # 4. Steps
            db.query(ApplicationStep).filter_by(service_id=svc.id).delete()
            for step in s_data.get("steps", []):
                astep = ApplicationStep(
                    service_id=svc.id,
                    step_number=step["step_number"],
                    title_en=step["title_en"],
                    title_mr=step.get("title_mr", step["title_en"]),
                    title_hi=step["title_en"],
                    instructions_en=step["instructions_en"],
                    instructions_mr=step.get("instructions_mr", step["instructions_en"]),
                    instructions_hi=step["instructions_en"],
                    external_url=step.get("action_url", s_data["source_url"])
                )
                db.add(astep)

            # 5. Knowledge Chunks for AI
            existing_kc = db.query(KnowledgeChunk).filter_by(service_id=svc.id).first()
            if not existing_kc:
                kc = KnowledgeChunk(
                    service_id=svc.id,
                    source_id=aaple_source.id,
                    section_title=f"{s_data['name_en']} Overview and Process",
                    keywords=f"{s_data['name_en']} {s_data['name_mr']} fee timeline documents eligibility aaple sarkar maharashtra",
                    content_en=f"{s_data['name_en']} is provided by {s_data['dept_name_en']}. {s_data['description_en']} Statutory fee is ₹{s_data['statutory_fee_inr']} with delivery timeline of {s_data['processing_days']} working days under the Maharashtra Right to Public Services Act.",
                    content_mr=f"{s_data['name_mr']} ही सेवा {s_data.get('dept_name_mr', s_data['dept_name_en'])} मार्फत दिली जाते. {s_data['description_mr']} अधिकृत वैधानिक शुल्क ₹{s_data['statutory_fee_inr']} असून विहित मुदत {s_data['processing_days']} कामकाजाचे दिवस आहे.",
                    content_hi=f"{s_data['name_en']} सेवा {s_data['dept_name_en']} द्वारा प्रदान की जाती है।"
                )
                db.add(kc)

        db.commit()
        print("Database successfully updated with all Aaple Sarkar services!")

    except Exception as e:
        db.rollback()
        print(f"Error updating database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    update_seed()
