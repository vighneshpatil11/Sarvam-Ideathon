import os
import sys

# Ensure backend app is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.database import engine, Base, SessionLocal
from app.models import (
    State, District, Department, Source, Service, ServiceDocument,
    ApplicationStep, KnowledgeChunk
)

ADDITIONAL_SERVICES = [
  {
    "name_en": "Landless Labourer Certificate",
    "name_mr": "भूमिहीन शेतमजूर असल्याचा दाखला",
    "slug": "landless-labourer-certificate",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an applicant and family members do not own any agricultural land in Maharashtra.",
    "short_description_mr": "अर्जदाराच्या किंवा त्याच्या कुटुंबाच्या नावावर कोणतीही शेतजमीन नसल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "Provided by the Tahsildar to verify landless rural agricultural workers, enabling them to apply for government land allotments, housing schemes (Gharkul), and agricultural worker welfare grants.",
    "description_mr": "ग्रामीण भागातील भूमिहीन मजुरांना घरकुल योजना, शासकीय योजना आणि शेतमजूर कल्याणकारी लाभांसाठी हा दाखला दिला जातो.",
    "documents": [
      {"name_en": "Aadhaar Card / Voter ID", "name_mr": "आधार कार्ड / मतदार ओळखपत्र", "description_en": "Proof of Identity", "category": "identity_proof", "required": True},
      {"name_en": "Ration Card / Gram Panchayat Certificate", "name_mr": "रेशन कार्ड / ग्रामपंचायत दाखला", "description_en": "Proof of Residence", "category": "address_proof", "required": True},
      {"name_en": "Talathi Inquiry Report", "name_mr": "तलाठी अहवाल", "description_en": "Report certifying no land in village records", "category": "other", "required": True},
      {"name_en": "Self-Declaration Form", "name_mr": "स्वयंघोषणा पत्र", "description_en": "Declaration of having zero agricultural landholdings", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Apply Online", "title_mr": "ऑनलाइन अर्ज", "instructions_en": "Select Revenue Department -> Landless Certificate on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Upload Documents", "title_mr": "कागदपत्रे अपलोड करा", "instructions_en": "Upload identity, residence proof, and signed self-declaration.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Talathi Verification", "title_mr": "तलाठी पडताळणी", "instructions_en": "Application forwarded to local Talathi for field verification.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 4, "title_en": "Download Certificate", "title_mr": "दाखला डाऊनलोड करा", "instructions_en": "Download digitally signed certificate upon Tahsildar approval.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Birth Certificate (Urban)",
    "name_mr": "जन्म नोंदणी दाखला (नागरी / महानगरपालिका)",
    "slug": "birth-certificate-urban",
    "dept_code": "URBAN_DEV",
    "dept_name_en": "Urban Development Department",
    "dept_name_mr": "नगर विकास विभाग",
    "short_description_en": "Official registration and certificate of a child's birth within municipal corporation or council limits.",
    "short_description_mr": "महानगरपालिका किंवा नगरपालिका हद्दीत झालेल्या बालकाच्या जन्माचा अधिकृत नोंदणी दाखला.",
    "description_en": "Issued by the Medical Officer of Health (MOH) of the municipal body under the Registration of Births and Deaths Act. Mandatory for admissions, passports, and civil registrations.",
    "description_mr": "महानगरपालिकेच्या आरोग्य विभागामार्फत नागरी भागातील जन्माची अधिकृत नोंद करून हा दाखला दिला जातो.",
    "documents": [
      {"name_en": "Hospital Birth Report / Form 1", "name_mr": "हॉस्पिटल जन्म नोंद अहवाल / फॉर्म १", "description_en": "Report issued by maternity hospital", "category": "other", "required": True},
      {"name_en": "Parents' Aadhaar Card / ID Proof", "name_mr": "आई-वडिलांचे ओळख पुरावे", "description_en": "Proof of Identity of parents", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Search", "title_mr": "पोर्टलवर शोधा", "instructions_en": "Select Urban Development -> Birth Certificate on Aaple Sarkar or Municipal portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Enter Date & Hospital", "title_mr": "तारीख व हॉस्पिटल निवडा", "instructions_en": "Search record by birth date, mother's name, or hospital registration number.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Download Certificate", "title_mr": "दाखला डाऊनलोड करा", "instructions_en": "Download digitally signed certificate within 3 working days (Free within 21 days).", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 3,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Death Certificate (Urban)",
    "name_mr": "मृत्यू नोंदणी दाखला (नागरी / महानगरपालिका)",
    "slug": "death-certificate-urban",
    "dept_code": "URBAN_DEV",
    "dept_name_en": "Urban Development Department",
    "dept_name_mr": "नगर विकास विभाग",
    "short_description_en": "Official death certificate issued by Municipal Corporation / Council health authorities.",
    "short_description_mr": "महानगरपालिका हद्दीत झालेल्या मृत्यूची अधिकृत नोंद प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Medical Officer of Health under the Registration of Births and Deaths Act. Vital for insurance, legal heir transfers, and bank accounts.",
    "description_mr": "महानगरपालिका किंवा नगरपालिका हद्दीतील मृत्यूची अधिकृत नोंद करून आरोग्य विभागामार्फत हा दाखला दिला जातो.",
    "documents": [
      {"name_en": "Medical Certificate of Death", "name_mr": "वैद्यकीय मृत्यू प्रमाणपत्र", "description_en": "Doctor/Hospital death summary", "category": "other", "required": True},
      {"name_en": "Cremation / Burial Receipt", "name_mr": "स्मशानभूमी पावती", "description_en": "Receipt from municipal crematorium", "category": "other", "required": True},
      {"name_en": "Deceased's Aadhaar / ID", "name_mr": "मृत व्यक्तीचा ओळख पुरावा", "description_en": "Identity proof of deceased", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Online Application", "title_mr": "ऑनलाइन अर्ज", "instructions_en": "Select Urban Development -> Death Certificate.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Submit Details", "title_mr": "तपशील भरा", "instructions_en": "Enter deceased particulars and crematorium details.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Download Certificate", "title_mr": "दाखला डाऊनलोड", "instructions_en": "Download approved certificate within 3 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 3,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Marriage Registration Certificate (Urban)",
    "name_mr": "विवाह नोंदणी दाखला (महानगरपालिका / नागरी)",
    "slug": "marriage-registration-certificate-urban",
    "dept_code": "URBAN_DEV",
    "dept_name_en": "Urban Development Department",
    "dept_name_mr": "नगर विकास विभाग",
    "short_description_en": "Statutory marriage registration within municipal corporation and council limits.",
    "short_description_mr": "शहरी व महानगरपालिका हद्दीतील विवाहाची अधिकृत नोंदणी व प्रमाणपत्र.",
    "description_en": "Issued by the Municipal Marriage Registrar. Essential for passports, visa applications, joint finances, and spousal legal rights.",
    "description_mr": "महानगरपालिका विवाह नोंदणी अधिकाऱ्यांमार्फत विवाहाची अधिकृत नोंदणी करून हे प्रमाणपत्र दिले जाते.",
    "documents": [
      {"name_en": "Wedding Invitation Card", "name_mr": "लग्नपत्रिका", "description_en": "Solemnization evidence", "category": "other", "required": True},
      {"name_en": "Bride & Groom ID and Age Proofs", "name_mr": "वर-वधूचे ओळख व वय पुरावे", "description_en": "Aadhaar Card, Passport, or LC", "category": "identity_proof", "required": True},
      {"name_en": "Witness Proofs (3 Witnesses)", "name_mr": "३ साक्षीदारांचे ओळख पुरावे", "description_en": "Aadhaar cards of 3 witnesses", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Apply on Portal", "title_mr": "पोर्टलवर अर्ज करा", "instructions_en": "Select Urban Development -> Marriage Registration on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Upload Proofs & Book Slot", "title_mr": "कागदपत्रे अपलोड करा व वेळ निवडा", "instructions_en": "Upload photos, wedding card, IDs and book registrar appointment.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Physical Verification & Certificate", "title_mr": "स्वाक्षरी व दाखला प्राप्ती", "instructions_en": "Couple and witnesses sign register; digital certificate issued within 5 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 5,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Addition of Name in Ration Card",
    "name_mr": "शिधापत्रिकेत नाव समाविष्ट करणे",
    "slug": "addition-of-name-in-ration-card",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection Department",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Service to add a new family member (newborn child or spouse) into an existing ration card.",
    "short_description_mr": "विद्यमान रेशन कार्डमध्ये नवजात बालकाचे किंवा विवाहामुळे पत्नीचे नाव समाविष्ट करण्याची सेवा.",
    "description_en": "Issued by the Tahsildar / Food Distribution Officer to include newly eligible household members for food grain quota calculation and government records.",
    "description_mr": "तहसीलदार किंवा अन्न पुरवठा अधिकाऱ्यांमार्फत कुटुंबातील नवीन सदस्याचे नाव रेशन कार्डमध्ये समाविष्ट केले जाते.",
    "documents": [
      {"name_en": "Existing Ration Card Copy", "name_mr": "मूळ रेशन कार्ड प्रत", "description_en": "Active ration card", "category": "other", "required": True},
      {"name_en": "Birth Certificate (for child) / Marriage Certificate (for spouse)", "name_mr": "जन्म दाखला / विवाह नोंदणी दाखला", "description_en": "Legal relationship proof", "category": "other", "required": True},
      {"name_en": "Deletion Certificate from previous card (for spouse)", "name_mr": "मागील रेशन कार्डमधून नाव कमी केल्याचा दाखला", "description_en": "Mandatory for spouse", "category": "other", "required": True},
      {"name_en": "Aadhaar Card of member to be added", "name_mr": "समाविष्ट करावयाच्या सदस्याचे आधार कार्ड", "description_en": "Aadhaar proof", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Login to RCMS / Aaple Sarkar", "title_mr": "पोर्टलवर लॉगिन", "instructions_en": "Log in and select Addition of Name in Ration Card.", "external_url": "https://rcms.mahafood.gov.in"},
      {"step_number": 2, "title_en": "Enter Member Details", "title_mr": "सदस्याचा तपशील भरा", "instructions_en": "Enter Aadhaar, relationship, date of birth.", "external_url": "https://rcms.mahafood.gov.in"},
      {"step_number": 3, "title_en": "Upload Proofs & Submit", "title_mr": "कागदपत्रे जोडून अर्ज सबमिट करा", "instructions_en": "Upload birth/marriage certificate and prior deletion certificate; pay ₹20 fee.", "external_url": "https://rcms.mahafood.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 20.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  {
    "name_en": "Deletion of Name from Ration Card",
    "name_mr": "शिधापत्रिकेतून नाव कमी करणे",
    "slug": "deletion-of-name-from-ration-card",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection Department",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Service to delete a member's name from ration card due to marriage, relocation, or demise.",
    "short_description_mr": "लग्न, स्थलांतर किंवा मृत्यूमुळे रेशन कार्डमधून सदस्याचे नाव वगळून दाखला मिळवण्याची सेवा.",
    "description_en": "Provides an official Surrender/Deletion Certificate (नाव कमी केल्याचा दाखला) required to add the person to a new ration card.",
    "description_mr": "नवीन रेशन कार्ड बनवण्यासाठी किंवा दुसऱ्या रेशन कार्डमध्ये नाव जोडण्यासाठी नाव कमी केल्याचा अधिकृत दाखला दिला जातो.",
    "documents": [
      {"name_en": "Existing Ration Card Copy", "name_mr": "मूळ रेशन कार्ड प्रत", "description_en": "Active ration card", "category": "other", "required": True},
      {"name_en": "Marriage Certificate / Death Certificate / Address Change Proof", "name_mr": "विवाह दाखला / मृत्यू दाखला / स्थलांतर पुरावा", "description_en": "Reason for deletion", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Portal Login", "title_mr": "पोर्टल लॉगिन", "instructions_en": "Select Deletion of Name on Aaple Sarkar / RCMS.", "external_url": "https://rcms.mahafood.gov.in"},
      {"step_number": 2, "title_en": "Select Member & Reason", "title_mr": "सदस्य व कारण निवडा", "instructions_en": "Choose member and upload reason document.", "external_url": "https://rcms.mahafood.gov.in"},
      {"step_number": 3, "title_en": "Pay Fee & Download Deletion Slip", "title_mr": "शुल्क भरा व दाखला डाऊनलोड करा", "instructions_en": "Pay ₹20 fee; receive deletion certificate within 7 working days.", "external_url": "https://rcms.mahafood.gov.in"}
    ],
    "processing_days": 7,
    "statutory_fee_inr": 20.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  {
    "name_en": "Sanjay Gandhi Niradhar Anudan Yojana",
    "name_mr": "संजय गांधी निराधार अनुदान योजना",
    "slug": "sanjay-gandhi-niradhar-anudan-yojana",
    "dept_code": "SOC_JUSTICE",
    "dept_name_en": "Social Justice and Special Assistance Department",
    "dept_name_mr": "सामाजिक न्याय व विशेष सहाय्य विभाग",
    "short_description_en": "Monthly financial pension scheme (₹1,500/month) for destitute, widows, disabled, and terminally ill individuals.",
    "short_description_mr": "निराधार व्यक्ती, विधवा, दिव्यांग व दुर्धर आजारी व्यक्तींसाठी दरमहा ₹१,५०० आर्थिक सहाय्य योजना.",
    "description_en": "Provides social security pension to destitute persons aged under 65, widows, orphans, and persons with disabilities living below family income limit (≤ ₹21,000/year).",
    "description_mr": "दारिद्र्य रेषेखालील व कमी उत्पन्न असलेल्या निराधार महिला, विधवा, अनाथ व दिव्यांग व्यक्तींना सन्मानाने जगण्यासाठी दरमहा अर्थसहाय्य दिले जाते.",
    "documents": [
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Identity Proof", "category": "identity_proof", "required": True},
      {"name_en": "15-Year Maharashtra Residence Proof", "name_mr": "१५ वर्षे वास्तव्याचा पुरावा", "description_en": "Domicile / Residence proof", "category": "address_proof", "required": True},
      {"name_en": "Tahsildar Income Certificate (<= ₹21,000)", "name_mr": "तहसीलदार उत्पन्न दाखला (वार्षिक ₹२१,००० च्या आत)", "description_en": "Annual income proof", "category": "income_proof", "required": True},
      {"name_en": "Death Certificate of Husband (for widows) / UDID Card (for disabled)", "name_mr": "पतीचा मृत्यू दाखला / दिव्यांग प्रमाणपत्र", "description_en": "Eligibility justification document", "category": "other", "required": True},
      {"name_en": "Aadhaar-Seeded Bank Passbook", "name_mr": "आधार लिंक बँक पासबुक", "description_en": "For monthly DBT payment", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Apply Online / Tehsil Center", "title_mr": "ऑनलाइन / सेतू केंद्रावर अर्ज", "instructions_en": "Fill application on Aaple Sarkar under Social Justice Department.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Upload Proofs & Bank Details", "title_mr": "कागदपत्रे व बँक तपशील भरा", "instructions_en": "Upload income, residence, category proof, and bank passbook.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Tehsil Committee Approval", "title_mr": "तहसील समिती मंजुरी", "instructions_en": "Sanjay Gandhi Committee reviews and approves within 30 days; DBT credited monthly.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 0.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "Shravanbal Seva Rajya Nivruttivetan Yojana",
    "name_mr": "श्रावणबाळ सेवा राज्य निवृत्तीवेतन योजना",
    "slug": "shravanbal-seva-rajya-nivruttivetan-yojana",
    "dept_code": "SOC_JUSTICE",
    "dept_name_en": "Social Justice and Special Assistance Department",
    "dept_name_mr": "सामाजिक न्याय व विशेष सहाय्य विभाग",
    "short_description_en": "State pension providing ₹1,500 monthly financial allowance to destitute senior citizens aged 65 and above.",
    "short_description_mr": "६५ वर्षे किंवा त्याहून अधिक वयाच्या निराधार वृद्ध नागरिकांना दरमहा ₹१,५०० निवृत्तीवेतन देणारी योजना.",
    "description_en": "Guarantees monthly direct cash support to poor senior citizens residing in Maharashtra who lack family financial support, under Category A (non-BPL, income <= ₹21,000) or Category B (BPL cardholders).",
    "description_mr": "वृद्धापकाळात आधार नसलेल्या जेष्ठ नागरिकांना महाराष्ट्र शासनाकडून दरमहा ₹१,५०० निवृत्तीवेतन थेट बँक खात्यात जमा केले जाते.",
    "documents": [
      {"name_en": "Aadhaar Card and Age Proof (65+ years)", "name_mr": "आधार कार्ड व वयाचा पुरावा (६५ वर्षे पूर्ण)", "description_en": "Age and identity verification", "category": "identity_proof", "required": True},
      {"name_en": "15-Year Maharashtra Residence Proof", "name_mr": "१५ वर्षे वास्तव्याचा पुरावा", "description_en": "Domicile / continuous residence", "category": "address_proof", "required": True},
      {"name_en": "Income Certificate / BPL Ration Card", "name_mr": "उत्पन्न दाखला / बीपीएल रेशन कार्ड", "description_en": "Proof of annual income <= ₹21,000 or BPL", "category": "income_proof", "required": True},
      {"name_en": "Aadhaar Linked Bank Passbook", "name_mr": "आधार लिंक बँक पासबुक", "description_en": "DBT bank account", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Online Portal Application", "title_mr": "पोर्टलवर अर्ज करा", "instructions_en": "Select Social Justice -> Shravanbal Yojana on Aaple Sarkar.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Upload Age & Income Proof", "title_mr": "वय व उत्पन्न पुरावे जोडा", "instructions_en": "Upload scanned age proof, income report, and bank details.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Scrutiny & Sanction", "title_mr": "पडताळणी व पेन्शन मंजुरी", "instructions_en": "Sanction order issued by Tahsildar within 30 days.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 0.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  {
    "name_en": "MAHABOCW Construction Worker Welfare Registration",
    "name_mr": "बांधकाम कामगार कल्याणकारी नोंदणी (MAHABOCW)",
    "slug": "bocw-construction-worker-registration",
    "dept_code": "LABOUR_DEPT",
    "dept_name_en": "Labour Department",
    "dept_name_mr": "कामगार विभाग",
    "short_description_en": "Official registration card for building & construction workers entitling them to financial grants, toolkits, and health assistance.",
    "short_description_mr": "इमारत व इतर बांधकाम कामगारांसाठी अधिकृत नोंदणी (स्मार्ट कार्ड), कल्याणकारी योजना, शैक्षणिक अनुदान व वैद्यकीय मदत.",
    "description_en": "Administered by Maharashtra Building and Other Construction Workers Welfare Board (MAHABOCW). Registered workers receive toolkits, safety gear, ₹5,000 annual subsidy, marriage assistance, and children scholarships.",
    "description_mr": "महाराष्ट्र इमारत व इतर बांधकाम कामगार कल्याणकारी मंडळामार्फत नोंदणीकृत कामगारांना थेट आर्थिक सहाय्य, आरोग्य तपासणी, संसार संच व अवजारे किट दिले जातात.",
    "documents": [
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Identity Proof", "category": "identity_proof", "required": True},
      {"name_en": "90 Days Work Certificate (Form 91)", "name_mr": "९० दिवस काम केल्याचे प्रमाणपत्र (फॉर्म ९१)", "description_en": "Certificate from contractor / Gram Sevak / Municipal Engineer", "category": "other", "required": True},
      {"name_en": "Ration Card / Residence Proof", "name_mr": "रेशन कार्ड / वास्तव्याचा पुरावा", "description_en": "Address proof", "category": "address_proof", "required": True},
      {"name_en": "Aadhaar Seeded Bank Passbook", "name_mr": "आधार संलग्न बँक पासबुक", "description_en": "Bank account for DBT", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "MAHABOCW Portal Registration", "title_mr": "महाबीओसीडब्ल्यू नोंदणी", "instructions_en": "Sign in to mahabocw.in with mobile number and Aadhaar.", "external_url": "https://mahabocw.in"},
      {"step_number": 2, "title_en": "Fill Work History", "title_mr": "कामाचा तपशील भरा", "instructions_en": "Enter employer/contractor details and upload 90-day work certificate.", "external_url": "https://mahabocw.in"},
      {"step_number": 3, "title_en": "Biometric Verification & Card", "title_mr": "स्मार्ट कार्ड प्राप्ती", "instructions_en": "Verified by Labour Inspector within 15 days; Smart Registration Card issued free of cost.", "external_url": "https://mahabocw.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 0.00,
    "source_url": "https://mahabocw.in"
  },
  {
    "name_en": "Learner's Driving Licence (LLR)",
    "name_mr": "शिकाऊ वाहन चालक परवाना (LLR)",
    "slug": "learners-licence-llr",
    "dept_code": "TRANSPORT_DEPT",
    "dept_name_en": "Transport Department (Motor Vehicles Department / RTO)",
    "dept_name_mr": "परिवहन विभाग (प्रादेशिक परिवहन कार्यालय / RTO)",
    "short_description_en": "Statutory temporary licence allowing an individual to practice driving on public roads.",
    "short_description_mr": "वाहने चालविणे शिकण्यासाठी आरटीओकडून दिला जाणारा ६ महिने वैध असलेला शिकाऊ चालक परवाना.",
    "description_en": "Issued online under the Motor Vehicles Act by the Regional Transport Office (RTO). Applicants complete a computerized online road safety theory test from home via Aadhaar authentication.",
    "description_mr": "परिवहन विभागामार्फत घरबसल्या आधार प्रमाणीकरणाद्वारे ऑनलाइन संगणकीय परीक्षा देऊन हा शिकाऊ परवाना ३ दिवसांत मिळवता येतो.",
    "documents": [
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Proof of Identity and Address (Online Aadhaar eKYC)", "category": "identity_proof", "required": True},
      {"name_en": "Age Proof (School Leaving Certificate / Birth Certificate)", "name_mr": "वयाचा पुरावा (शाळा सोडल्याचा दाखला)", "description_en": "Proof of minimum age (18+ for LMV, 16+ for gearless 2-wheeler)", "category": "identity_proof", "required": True},
      {"name_en": "Medical Certificate (Form 1 / Form 1A for 40+ age or commercial)", "name_mr": "वैद्यकीय प्रमाणपत्र (फॉर्म १ / १-अ)", "description_en": "Physical fitness self-declaration", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Parivahan / Sarathi Portal", "title_mr": "सारथी पोर्टलवर जा", "instructions_en": "Visit Sarathi Parivahan -> Maharashtra -> Apply for Learner Licence.", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 2, "title_en": "Aadhaar e-KYC", "title_mr": "आधार ई-केवायसी", "instructions_en": "Authenticate using Aadhaar OTP (no physical RTO visit needed).", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 3, "title_en": "Pay Fee & Take Online LL Test", "title_mr": "शुल्क भरा व ऑनलाइन परीक्षा द्या", "instructions_en": "Pay ₹201 fee and pass the 15-question road signs test online from home.", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 4, "title_en": "Instant Download", "title_mr": "परवाना डाऊनलोड करा", "instructions_en": "Instantly download digital Learner's Licence valid for 6 months across India.", "external_url": "https://sarathi.parivahan.gov.in"}
    ],
    "processing_days": 3,
    "statutory_fee_inr": 201.00,
    "source_url": "https://sarathi.parivahan.gov.in"
  },
  {
    "name_en": "Permanent Driving Licence (DL)",
    "name_mr": "कायमस्वरूपी वाहन चालक परवाना (पक्का ड्रायव्हिंग लायसन्स)",
    "slug": "permanent-driving-licence-dl",
    "dept_code": "TRANSPORT_DEPT",
    "dept_name_en": "Transport Department (Motor Vehicles Department / RTO)",
    "dept_name_mr": "परिवहन विभाग (प्रादेशिक परिवहन कार्यालय / RTO)",
    "short_description_en": "Official permanent smart card driving licence authorizing an individual to drive motor vehicles in India.",
    "short_description_mr": "भारतात सार्वजनिक रस्त्यांवर अधिकृतपणे वाहन चालविण्याचा अधिकार देणारा आरटीओ पक्का ड्रायव्हिंग लायसन्स.",
    "description_en": "Issued by the RTO after the candidate passes a practical driving skill test on track, at least 30 days after obtaining a Learner's Licence.",
    "description_mr": "शिकाऊ परवाना मिळाल्यानंतर किमान ३० दिवसांनी आरटीओ ट्रॅकवर प्रत्यक्ष वाहन चालवून परीक्षा उत्तीर्ण झाल्यावर हा स्मार्ट कार्ड परवाना दिला जातो.",
    "documents": [
      {"name_en": "Valid Learner's Licence Number", "name_mr": "वैध शिकाऊ परवाना (LLR)", "description_en": "Active learner licence (completed at least 30 days)", "category": "other", "required": True},
      {"name_en": "Driving School Certificate (Form 5 for commercial/heavy vehicles)", "name_mr": "मोटर ड्रायव्हिंग स्कूल प्रमाणपत्र", "description_en": "Training completion certificate", "category": "other", "required": False},
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Identity proof", "category": "identity_proof", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Book Driving Test Slot", "title_mr": "आरटीओ चाचणी वेळ निवडा", "instructions_en": "Go to Sarathi Parivahan -> Apply for Driving Licence -> Book RTO test slot.", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 2, "title_en": "Pay Statutory Fees", "title_mr": "चाचणी व स्मार्ट कार्ड शुल्क भरा", "instructions_en": "Pay ₹716 statutory test and smart card fee online.", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 3, "title_en": "Pass RTO Driving Test", "title_mr": "आरटीओ ड्रायव्हिंग टेस्ट द्या", "instructions_en": "Visit RTO testing ground with your vehicle and pass the practical driving test.", "external_url": "https://sarathi.parivahan.gov.in"},
      {"step_number": 4, "title_en": "Smart Card Delivery", "title_mr": "लायसन्स प्राप्ती", "instructions_en": "Smart card dispatched to your residential address via Speed Post within 15 days.", "external_url": "https://sarathi.parivahan.gov.in"}
    ],
    "processing_days": 15,
    "statutory_fee_inr": 716.00,
    "source_url": "https://sarathi.parivahan.gov.in"
  },
  {
    "name_en": "Micro-Irrigation Subsidy (Drip & Sprinkler Scheme)",
    "name_mr": "सूक्ष्म सिंचन अनुदान योजना (ठिबक व तुषार सिंचन - महाडीबीटी)",
    "slug": "drip-and-sprinkler-irrigation-subsidy",
    "dept_code": "AGRI_DEPT",
    "dept_name_en": "Agriculture Department",
    "dept_name_mr": "कृषी विभाग",
    "short_description_en": "State and central subsidy (55% to 75%) for installing water-saving drip and sprinkler irrigation systems.",
    "short_description_mr": "शेतकऱ्यांना ठिबक व तुषार सिंचन संच बसविण्यासाठी ५५% ते ७५% पर्यंत शासकीय अनुदान देणारी योजना.",
    "description_en": "Operated through the MahaDBT Farmer Schemes portal under PMKSY. Small & marginal farmers receive up to 75% subsidy and other farmers receive 55% subsidy credited directly to their bank account.",
    "description_mr": "महाडीबीटी शेतकरी पोर्टलद्वारे पाणी बचत करणाऱ्या ठिबक व तुषार सिंचनासाठी लहान व अल्पभूधारक शेतकऱ्यांना ७५% पर्यंत अनुदान दिले जाते.",
    "documents": [
      {"name_en": "7/12 Extract showing water source (Well / Borewell / Canal)", "name_mr": "पाण्याची नोंद असलेला ७/१२ उतारा (विहीर/बोअरवेल)", "description_en": "Agricultural land and water source proof", "category": "other", "required": True},
      {"name_en": "8-A Land Extract", "name_mr": "८-अ खाते उतारा", "description_en": "Total acreage proof", "category": "other", "required": True},
      {"name_en": "Aadhaar Card", "name_mr": "आधार कार्ड", "description_en": "Identity Proof", "category": "identity_proof", "required": True},
      {"name_en": "GST Invoice & Warranty Card from Authorized Dealer", "name_mr": "अधिकृत विक्रेत्याचे जीएसटी बिल व वॉरंटी कार्ड", "description_en": "Proof of purchase of BIS approved equipment", "category": "other", "required": True},
      {"name_en": "Aadhaar Linked Bank Passbook", "name_mr": "आधार संलग्न बँक पासबुक", "description_en": "Bank account for subsidy DBT", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "Apply on MahaDBT Farmer Portal", "title_mr": "महाडीबीटी शेतकरी पोर्टलवर अर्ज", "instructions_en": "Log in and select Pradhan Mantri Krishi Sinchayee Yojana (Micro Irrigation).", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 2, "title_en": "Computerized Lottery & Pre-Sanction", "title_mr": "लॉटरी निवड व पूर्वसंमती पत्र", "instructions_en": "Upon lottery selection, download the official Pre-Sanction Order (पूर्वसंमती).", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 3, "title_en": "Install System & Upload Invoice", "title_mr": "सिंचन संच बसवून बिल अपलोड करा", "instructions_en": "Install drip/sprinkler through approved dealer within 30 days and upload GST bill.", "external_url": "https://mahadbt.maharashtra.gov.in"},
      {"step_number": 4, "title_en": "Geo-tagged Inspection & DBT", "title_mr": "मोका तपासणी व अनुदान जमा", "instructions_en": "Taluka Agriculture Officer conducts geo-tagged field verification; subsidy deposited via DBT.", "external_url": "https://mahadbt.maharashtra.gov.in"}
    ],
    "processing_days": 30,
    "statutory_fee_inr": 23.60,
    "source_url": "https://mahadbt.maharashtra.gov.in"
  },
  {
    "name_en": "Deemed Conveyance of Housing Society (MOFA Section 11)",
    "name_mr": "गृहनिर्माण संस्थांचे मानीव अभिहस्तांतरण (डीम्ड कन्व्हेयन्स)",
    "slug": "deemed-conveyance-housing-society",
    "dept_code": "COOP_DEPT",
    "dept_name_en": "Co-operation, Marketing and Textiles Department",
    "dept_name_mr": "सहकार, पणन व वस्त्रोद्योग विभाग",
    "short_description_en": "Statutory transfer of land title and ownership to a Co-operative Housing Society when the builder defaults.",
    "short_description_mr": "बिल्डरने जमीन नावावर न केल्यास सहकारी गृहनिर्माण संस्थेला जमिनीची अधिकृत मालकी देणारा कायदेशीर आदेश.",
    "description_en": "Issued by the District Deputy Registrar (DDR) acting as Competent Authority under MOFA Section 11. Transfers legal ownership of the building land and Property Card to the housing society without builder consent.",
    "description_mr": "सोसायटी स्थापन झाल्यानंतर बिल्डरने मानीव अभिहस्तांतरण करून न दिल्यास सहकार उपनिबंधकांमार्फत संस्थेला जागेचे मालकी हक्क मिळवून देणारा महत्त्वपूर्ण कायदेशीर आदेश.",
    "documents": [
      {"name_en": "Society Registration Certificate", "name_mr": "सोसायटी नोंदणी प्रमाणपत्र", "description_en": "Proof of CHS registration", "category": "other", "required": True},
      {"name_en": "Sanctioned Building Plan & Occupation Certificate (OC)", "name_mr": "मंजूर नकाशा व भोगवटा प्रमाणपत्र (OC)", "description_en": "Municipal approval records", "category": "other", "required": True},
      {"name_en": "Registered Agreement for Sale Copies of Flat Buyers", "name_mr": "सभासदांचे नोंदणीकृत खरेदी खत", "description_en": "Proof of flat ownership", "category": "other", "required": True},
      {"name_en": "Property Card & 7/12 Extract of Land", "name_mr": "जमिनीचे मालमत्ता पत्रक व ७/१२ उतारा", "description_en": "Title search documents", "category": "other", "required": True},
      {"name_en": "Architect Certificate of Society Area", "name_mr": "आर्किटेक्टचे क्षेत्रफळ प्रमाणपत्र", "description_en": "Area measurement certificate", "category": "other", "required": True}
    ],
    "steps": [
      {"step_number": 1, "title_en": "File Online Deemed Conveyance", "title_mr": "डीम्ड कन्व्हेयन्स अर्ज करा", "instructions_en": "File Form VII application on MahaSahakar / Aaple Sarkar portal.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 2, "title_en": "Submit Documents to DDR", "title_mr": "उपनिबंधकांकडे कागदपत्रे सादर करा", "instructions_en": "Upload society records, legal notice sent to builder, and pay ₹2,000 court fee.", "external_url": "https://aaplesarkar.mahaonline.gov.in"},
      {"step_number": 3, "title_en": "Hearings & Deemed Conveyance Order", "title_mr": "सुनावणी व अंतिम मालकी आदेश", "instructions_en": "DDR conducts hearings, passes Deemed Conveyance order, and executes unilateral deed.", "external_url": "https://aaplesarkar.mahaonline.gov.in"}
    ],
    "processing_days": 180,
    "statutory_fee_inr": 2000.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  }
]

def add_additional_services():
    print("Connecting to database to add additional services...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        mh_state = db.query(State).filter_by(code="MH").first()
        pune_district = db.query(District).filter_by(code="PUN").first()
        aaple_source = db.query(Source).filter_by(url="https://aaplesarkar.mahaonline.gov.in").first()

        for s_data in ADDITIONAL_SERVICES:
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
                if pune_district:
                    svc.districts.append(pune_district)
                if aaple_source:
                    svc.sources.append(aaple_source)
                db.add(svc)
                db.flush()
                print(f"Created: {s_data['name_en']}")
            else:
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
                print(f"Updated: {s_data['name_en']}")

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
                    external_url=step.get("external_url", s_data["source_url"])
                )
                db.add(astep)

            # 5. Knowledge Chunk
            existing_kc = db.query(KnowledgeChunk).filter_by(service_id=svc.id).first()
            if not existing_kc:
                kc = KnowledgeChunk(
                    service_id=svc.id,
                    source_id=aaple_source.id if aaple_source else None,
                    section_title=f"{s_data['name_en']} Overview and Process",
                    keywords=f"{s_data['name_en']} {s_data['name_mr']} fee timeline documents eligibility aaple sarkar maharashtra",
                    content_en=f"{s_data['name_en']} is provided by {s_data['dept_name_en']}. {s_data['description_en']} Statutory fee is ₹{s_data['statutory_fee_inr']} with delivery timeline of {s_data['processing_days']} working days under the Maharashtra Right to Public Services Act.",
                    content_mr=f"{s_data['name_mr']} ही सेवा {s_data.get('dept_name_mr', s_data['dept_name_en'])} मार्फत दिली जाते. {s_data['description_mr']} अधिकृत वैधानिक शुल्क ₹{s_data['statutory_fee_inr']} असून विहित मुदत {s_data['processing_days']} कामकाजाचे दिवस आहे.",
                    content_hi=f"{s_data['name_en']} सेवा {s_data['dept_name_en']} द्वारा प्रदान की जाती है।"
                )
                db.add(kc)

        db.commit()
        print("All additional services successfully added to database!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    add_additional_services()
