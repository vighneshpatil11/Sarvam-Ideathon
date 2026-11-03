import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.database import engine, Base, SessionLocal
from app.models import (
    State, District, Department, Source, Service, ServiceDocument,
    ApplicationStep, KnowledgeChunk
)

SUBMISSION_SERVICES = [
  # 1. Income Certificate
  {
    "slug": "income-certificate",
    "name_en": "Income Certificate",
    "name_mr": "उत्पन्नाचे प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate verifying total annual family income for scholarships, fee concessions, and government welfare schemes.",
    "short_description_mr": "शिष्यवृत्ती, शैक्षणिक सवलती आणि विविध शासकीय योजनांचा लाभ घेण्यासाठी कुटुंबाच्या वार्षिक उत्पन्नाचा अधिकृत दाखला.",
    "description_en": "Issued by the Tahsildar / Sub-Divisional Officer under the Revenue Department. Valid for 1 or 3 financial years.",
    "description_mr": "महसूल विभागातील तहसीलदार यांच्या स्वाक्षरीने दिला जाणारा उत्पन्नाचा दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 2. Caste Certificate
  {
    "slug": "caste-certificate",
    "name_en": "Caste Certificate",
    "name_mr": "जात प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate authenticating membership in a recognized SC, ST, VJNT, SBC, or OBC community.",
    "short_description_mr": "अनुसूचित जाती, जमाती, विमुक्त जाती, भटक्या जमाती किंवा इतर मागासवर्गातील सदस्यत्व प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Sub-Divisional Officer (SDO) for reserved category concessions and government recruitments.",
    "description_mr": "उपविभागीय अधिकारी (प्रांताधिकारी) यांच्याकडून दिले जाणारे अधिकृत जात प्रमाणपत्र.",
    "processing_days": 21,
    "statutory_fee_inr": 40.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 3. Non-Creamy Layer Certificate
  {
    "slug": "non-creamy-layer-certificate",
    "name_en": "Non-Creamy Layer Certificate",
    "name_mr": "नॉन-क्रीमी लेयर प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an applicant's family income does not exceed the creamy layer threshold (₹8 Lakhs/year) for OBC/VJNT/SBC.",
    "short_description_mr": "ओबीसी/व्हीजेएनटी प्रवर्गातील कुटुंबाचे वार्षिक उत्पन्न ८ लाख रुपयांपेक्षा कमी असल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "Enables OBC, VJNT, and SBC candidates to avail reservation benefits in education and employment.",
    "description_mr": "मागील सलग ३ आर्थिक वर्षांतील कुटुंबाचे उत्पन्न ₹८ लाखांपेक्षा जास्त नसल्याचे प्रमाणपत्र.",
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 4. Domicile Certificate
  {
    "slug": "domicile-certificate",
    "name_en": "Domicile Certificate",
    "name_mr": "अधिवास प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate proving continuous residence of at least 15 years in Maharashtra.",
    "short_description_mr": "महाराष्ट्रात सलग किमान १५ वर्षे वास्तव्याचा पुरावा देणारे अधिवास प्रमाणपत्र.",
    "description_en": "Issued by the Executive Magistrate / Tahsildar for state educational admissions and employment quotas.",
    "description_mr": "शैक्षणिक प्रवेश आणि शासकीय नोकऱ्यांसाठी आवश्यक अधिवास दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 5. Age, Nationality and Domicile Certificate
  {
    "slug": "age-nationality-and-domicile-certificate",
    "name_en": "Age, Nationality and Domicile Certificate",
    "name_mr": "वय, राष्ट्रीयत्व आणि अधिवास प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Comprehensive certificate verifying age, Indian nationality, and 15-year Maharashtra domicile in a single document.",
    "short_description_mr": "वय, भारतीय राष्ट्रीयत्व आणि १५ वर्षे अधिवास एकत्रित सिद्ध करणारा सर्वसमावेशक दाखला.",
    "description_en": "Required for higher educational admissions under CAP rounds and Maharashtra public services.",
    "description_mr": "कार्यकारी दंडाधिकारी (तहसीलदार) यांच्याकडून जारी केले जाणारे अधिकृत संयुक्त प्रमाणपत्र.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 6. Birth Certificate
  {
    "slug": "birth-certificate",
    "name_en": "Birth Certificate",
    "name_mr": "जन्म नोंदणी दाखला",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Official record and certificate verifying a person's birth under the Registration of Births and Deaths Act.",
    "short_description_mr": "जन्म व मृत्यू नोंदणी कायद्यानुसार दिला जाणारा अधिकृत जन्म दाखला.",
    "description_en": "Issued by Gram Sevak (Rural) or Medical Officer of Health (Urban). Essential for school admission and passports.",
    "description_mr": "ग्रामसेवक किंवा महानगरपालिका आरोग्य अधिकाऱ्यांमार्फत अधिकृत नोंद करून दिला जाणारा दाखला.",
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 7. Death Certificate
  {
    "slug": "death-certificate",
    "name_en": "Death Certificate",
    "name_mr": "मृत्यू नोंदणी दाखला",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Official registration and certificate confirming a person's demise.",
    "short_description_mr": "व्यक्तीच्या मृत्यूची अधिकृत नोंद प्रमाणित करणारा दाखला.",
    "description_en": "Issued by Gram Sevak or Municipal Health Officer. Essential for insurance claims, inheritance, and title transfer.",
    "description_mr": "वारस नोंद, विमा दावा आणि बँक खात्यातील रक्कम मिळवण्यासाठी आवश्यक दाखला.",
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 8. Marriage Certificate
  {
    "slug": "marriage-certificate",
    "name_en": "Marriage Certificate",
    "name_mr": "विवाह नोंदणी प्रमाणपत्र",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Statutory registration of marriage solemnized in Maharashtra.",
    "short_description_mr": "विवाह नोंदणी कायद्यांतर्गत दिलेला अधिकृत विवाह दाखला.",
    "description_en": "Issued by the Marriage Registrar (Gram Sevak or Municipal authority). Mandatory for passport name change and spousal visa.",
    "description_mr": "पासपोर्ट, व्हिसा आणि कायदेशीर हक्कांसाठी आवश्यक विवाह नोंदणी प्रमाणपत्र.",
    "processing_days": 5,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 9. Senior Citizen Certificate
  {
    "slug": "senior-citizen-certificate",
    "name_en": "Senior Citizen Certificate",
    "name_mr": "ज्येष्ठ नागरिक प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official card certifying an individual has attained 60 years of age for transport and health concessions.",
    "short_description_mr": "वयाची ६० वर्षे पूर्ण करणाऱ्या नागरिकांसाठी एसटी बस सवलत व शासकीय सवलती देणारा दाखला.",
    "description_en": "Issued by the Tahsildar to avail state welfare benefits and healthcare priorities.",
    "description_mr": "तहसीलदारांमार्फत जारी केलेले ज्येष्ठ नागरिक ओळखपत्र व दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 10. Disability Certificate
  {
    "slug": "disability-certificate",
    "name_en": "Disability Certificate (UDID)",
    "name_mr": "दिव्यांगत्व प्रमाणपत्र (UDID)",
    "dept_code": "PUBLIC_HEALTH",
    "dept_name_en": "Public Health Department",
    "dept_name_mr": "सार्वजनिक आरोग्य विभाग",
    "short_description_en": "Official medical certificate validating 40%+ benchmark disability and Unique Disability ID (UDID).",
    "short_description_mr": "४०% किंवा त्याहून अधिक दिव्यांगत्वाचे अधिकृत वैद्यकीय प्रमाणपत्र व UDID कार्ड.",
    "description_en": "Issued by District Medical Board under the Civil Surgeon for pensions, free travel, and reservations.",
    "description_mr": "जिल्हा शल्यचिकित्सक (सिव्हिल सर्जन) वैद्यकीय मंडळाकडून तपासणी करून दिले जाणारे प्रमाणपत्र.",
    "processing_days": 30,
    "statutory_fee_inr": 0.00,
    "source_url": "https://swavlambancard.gov.in"
  },
  # 11. Residence Certificate
  {
    "slug": "residence-certificate",
    "name_en": "Residence Certificate",
    "name_mr": "रहिवासी दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate confirming current residential address in a specific village, town, or city in Maharashtra.",
    "short_description_mr": "संबंधित गाव, शहर किंवा पत्त्यावर प्रत्यक्ष वास्तव्यास असल्याचा अधिकृत रहिवासी दाखला.",
    "description_en": "Issued by the Talathi / Tahsildar to prove present residence for gas connection, bank KYC, and local admissions.",
    "description_mr": "स्थानिक रहिवासी असल्याचे सिद्ध करण्यासाठी तलाठी किंवा तहसीलदार कार्यालयाकडून दिला जाणारा दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 12. Character Certificate / Police Clearance
  {
    "slug": "character-certificate",
    "name_en": "Character Certificate (Police Clearance Certificate)",
    "name_mr": "चारित्र्य पडताळणी प्रमाणपत्र (पोलीस दाखला)",
    "dept_code": "HOME_DEPT",
    "dept_name_en": "Home Department (Maharashtra Police)",
    "dept_name_mr": "गृह विभाग (महाराष्ट्र पोलीस)",
    "short_description_en": "Official background verification report certifying no adverse criminal records.",
    "short_description_mr": "संबंधित व्यक्तीवर कोणताही फौजदारी गुन्हा दाखल नसल्याचे पोलीस पडताळणी प्रमाणपत्र.",
    "description_en": "Issued by the SP / CP Office for government service recruitment, IT company clearances, and visa.",
    "description_mr": "पोलीस आयुक्तालय किंवा पोलीस अधीक्षकांमार्फत गुन्हेगारी नोंद पडताळून दिला जाणारा दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 123.60,
    "source_url": "https://pcs.mahaonline.gov.in"
  },
  # 13. Solvency Certificate
  {
    "slug": "solvency-certificate",
    "name_en": "Solvency Certificate",
    "name_mr": "ऐपतीचा दाखला / सधनता प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certification of an individual's financial solvency and unencumbered asset net worth.",
    "short_description_mr": "व्यक्तीची आर्थिक पत आणि संपत्तीचे मूल्य प्रमाणित करणारा सधनतेचा दाखला.",
    "description_en": "Issued by Tahsildar / SDO for court sureties, bail bonds, customs warehousing, and government contracts.",
    "description_mr": "शासकीय निविदा, न्यायालयीन जामीन व कंत्राटांसाठी आवश्यक ऐपत प्रमाणपत्र.",
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 14. Agriculturist Certificate
  {
    "slug": "agriculturist-certificate",
    "name_en": "Agriculturist Certificate",
    "name_mr": "शेतकरी असल्याचा दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an applicant holds lawful agricultural land cultivation status under the Tenancy Act.",
    "short_description_mr": "अर्जदार किंवा त्याचे कुटुंबीय अधिकृत शेतकरी असल्याचे सिद्ध करणारा दाखला.",
    "description_en": "Under Maharashtra law, only a recognized farmer can buy farm land. This certificate validates farmer status.",
    "description_mr": "महाराष्ट्रात शेतजमीन खरेदी करण्यासाठी व्यक्ती शेतकरी असल्याचा पुरावा देणारा तहसीलदार दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 15. Landless Labourer Certificate
  {
    "slug": "landless-labourer-certificate",
    "name_en": "Landless Labourer Certificate",
    "name_mr": "भूमिहीन शेतमजूर असल्याचा दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that an applicant and family do not own any agricultural land in Maharashtra.",
    "short_description_mr": "अर्जदाराच्या नावावर कोणतीही शेतजमीन नसल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "Issued by Tahsildar to enable rural workers to apply for government land allotments and housing grants.",
    "description_mr": "ग्रामीण भागातील भूमिहीन मजुरांना घरकुल योजना व कल्याणकारी लाभांसाठी दिला जाणारा दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 16. Below Poverty Line (BPL) Certificate
  {
    "slug": "bpl-certificate",
    "name_en": "Below Poverty Line (BPL) Certificate",
    "name_mr": "दारिद्र्य रेषेखालील (BPL) दाखला",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Official certification confirming a family's inclusion in the verified Below Poverty Line (BPL) census.",
    "short_description_mr": "कुटुंब अधिकृत दारिद्र्य रेषेखालील (BPL) यादीत समाविष्ट असल्याचा दाखला.",
    "description_en": "Issued by Gram Sevak or Municipal Chief Officer for availing free housing, medical aid, and subsidized food schemes.",
    "description_mr": "घरकुल योजना, मोफत वैद्यकीय उपचार व शासकीय अनुदानांसाठी आवश्यक बीपीएल दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 17. Ration Card – New Application
  {
    "slug": "ration-card-new-application",
    "name_en": "Ration Card – New Application",
    "name_mr": "नवीन रेशन कार्ड अर्ज",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Application for issuance of a new subsidized household ration card under the National Food Security Act (NFSA).",
    "short_description_mr": "राष्ट्रीय अन्न सुरक्षा कायद्यांतर्गत नवीन कुटुंबासाठी शिधापत्रिका (रेशन कार्ड) मिळवण्याचा अर्ज.",
    "description_en": "Issued by the Food Distribution Officer / Tahsildar for purchasing subsidized grain.",
    "description_mr": "तहसीलदार किंवा जिल्हा पुरवठा अधिकाऱ्यांमार्फत कुटुंबातील सदस्यांची नोंद असणारे नवीन रेशन कार्ड.",
    "processing_days": 30,
    "statutory_fee_inr": 50.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  # 18. Ration Card – Name Addition
  {
    "slug": "ration-card-name-addition",
    "name_en": "Ration Card – Name Addition",
    "name_mr": "शिधापत्रिकेत नाव समाविष्ट करणे",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Service to add a newborn child or newlywed spouse into an existing ration card.",
    "short_description_mr": "विद्यमान रेशन कार्डमध्ये नवजात बालकाचे किंवा नवीन सुनेचे नाव समाविष्ट करणे.",
    "description_en": "Updates family strength to increase monthly food grain quota under NFSA.",
    "description_mr": "कुटुंबातील नवीन सदस्याचे नाव समाविष्ट करून धान्याचा कोटा वाढवण्याची सेवा.",
    "processing_days": 15,
    "statutory_fee_inr": 20.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  # 19. Ration Card – Name Deletion
  {
    "slug": "ration-card-name-deletion",
    "name_en": "Ration Card – Name Deletion",
    "name_mr": "शिधापत्रिकेतून नाव कमी करणे",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Service to delete a member from ration card and obtain a Surrender/Deletion Certificate.",
    "short_description_mr": "लग्न किंवा स्थलांतरामुळे रेशन कार्डमधून नाव कमी करून अधिकृत दाखला मिळवणे.",
    "description_en": "Mandatory Deletion Certificate needed before adding a name into another ration card.",
    "description_mr": "दुसऱ्या रेशन कार्डमध्ये नाव जोडण्यासाठी आवश्यक असणारा नाव वगळल्याचा दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 20.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  # 20. Ration Card – Address Change
  {
    "slug": "ration-card-address-change",
    "name_en": "Ration Card – Address Change",
    "name_mr": "रेशन कार्ड पत्ता बदल करणे",
    "dept_code": "FOOD_CIVIL",
    "dept_name_en": "Food, Civil Supplies and Consumer Protection",
    "dept_name_mr": "अन्न, नागरी पुरवठा व ग्राहक संरक्षण विभाग",
    "short_description_en": "Transfer of ration card and Fair Price Shop (FPS) allocation to a new residential address.",
    "short_description_mr": "निवासस्थानात बदल झाल्यास रेशन कार्ड व स्वस्त धान्य दुकान नवीन पत्त्यावर हस्तांतरित करणे.",
    "description_en": "Reallocates your household food grain quota to the local ration shop in your new neighborhood.",
    "description_mr": "नवीन पत्त्यावरील अधिकृत रास्त भाव दुकानातून धान्य मिळण्यासाठी पत्ता बदल सेवा.",
    "processing_days": 15,
    "statutory_fee_inr": 20.00,
    "source_url": "https://rcms.mahafood.gov.in"
  },
  # 21. Shop and Establishment Registration
  {
    "slug": "shop-and-establishment-registration",
    "name_en": "Shop and Establishment Registration (Gumasta License)",
    "name_mr": "दुकाने व आस्थापना नोंदणी (गुमास्ता परवाना)",
    "dept_code": "LABOUR_DEPT",
    "dept_name_en": "Labour Department",
    "dept_name_mr": "कामगार विभाग",
    "short_description_en": "Statutory registration for commercial businesses, offices, and retail shops under the Maharashtra Shops Act.",
    "short_description_mr": "महाराष्ट्र दुकाने व आस्थापना कायद्यांतर्गत व्यवसायाची अधिकृत नोंदणी (गुमास्ता परवाना).",
    "description_en": "Form F Intimation (<10 workers) or Form C Registration (10+ workers). Required for business bank accounts.",
    "description_mr": "चालू खाते (Current Account) उघडण्यासाठी व व्यवसाय सुरू करण्यासाठी आवश्यक परवाना.",
    "processing_days": 1,
    "statutory_fee_inr": 23.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 22. Temporary Residence Certificate
  {
    "slug": "temporary-residence-certificate",
    "name_en": "Temporary Residence Certificate",
    "name_mr": "तात्पुरता रहिवासी दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certificate validating temporary dwelling in Maharashtra for seasonal workers, migrant students, and temporary employees.",
    "short_description_mr": "कामासाठी किंवा शिक्षणासाठी तात्पुरत्या स्वरूपात वास्तव्यास असलेल्या नागरिकांसाठी दाखला.",
    "description_en": "Issued by Talathi / Police Authority for verification of temporary lodging and job validation.",
    "description_mr": "तात्पुरते वास्तव्य सिद्ध करण्यासाठी स्थानिक महसूल यंत्रणेमार्फत दिला जाणारा दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 23. Small Landholder Certificate
  {
    "slug": "small-landholder-certificate",
    "name_en": "Small Landholder Certificate",
    "name_mr": "अल्पभूधारक शेतकरी दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Certifies that a farmer owns agricultural land up to 2 hectares (5 acres) to claim maximum subsidies.",
    "short_description_mr": "शेतकऱ्याकडे कमाल २ हेक्टर (५ एकर) शेतजमीन असल्याचे सिद्ध करणारा दाखला.",
    "description_en": "Required for 75% drip irrigation subsidy, tractor purchase schemes, and subsidized agricultural loans.",
    "description_mr": "ठिबक सिंचन अनुदान, कृषी यांत्रिकीकरण आणि शासकीय योजनांसाठी अत्यावश्यक दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 24. Widow Certificate
  {
    "slug": "widow-certificate",
    "name_en": "Widow Certificate (Vidhavapana Dakhla)",
    "name_mr": "विधवा दाखला",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department / Social Welfare",
    "dept_name_mr": "महसूल विभाग व समाजकल्याण",
    "short_description_en": "Official certificate confirming marital status as a widow for pension and government welfare benefits.",
    "short_description_mr": "संजय गांधी निराधार योजना, पेन्शन व शासकीय योजनांचा लाभ घेण्यासाठी अधिकृत विधवा दाखला.",
    "description_en": "Issued by the Tahsildar / Talathi based on husband's death certificate and family verification.",
    "description_mr": "पतीच्या निधनानंतर शासकीय योजना, मोफत शिक्षण व पेन्शनसाठी महसूल विभागाकडून दिलेला दाखला.",
    "processing_days": 7,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 25. Legal Heir Certificate
  {
    "slug": "legal-heir-certificate",
    "name_en": "Legal Heir Certificate (Varas Certificate / Kinship)",
    "name_mr": "वारस दाखला (कायदेशीर वारसदार प्रमाणपत्र)",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official certificate certifying the lawful surviving heirs of a deceased person.",
    "short_description_mr": "मृत व्यक्तीच्या कायदेशीर वारसदारांची अधिकृत नोंद व प्रमाणपत्र.",
    "description_en": "Issued by Tahsildar / Executive Magistrate to transfer ancestral property, bank balances, and pensions.",
    "description_mr": "जमीन, घर, बँक खात्यातील रक्कम व पेन्शन वारसांच्या नावावर करण्यासाठी अनिवार्य दाखला.",
    "processing_days": 21,
    "statutory_fee_inr": 50.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 26. Duplicate Birth Certificate
  {
    "slug": "duplicate-birth-certificate",
    "name_en": "Duplicate Birth Certificate",
    "name_mr": "दुय्यम जन्म नोंद दाखला",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Re-issuance of certified true copy of a previously registered birth certificate.",
    "short_description_mr": "मूळ जन्म दाखला हरवला असल्यास नोंदवहीतून मिळणारा अधिकृत दुय्यम जन्म दाखला.",
    "description_en": "Issued from municipal or Gram Panchayat historical birth records with digital verification.",
    "description_mr": "शासकीय नोंदवहीतून पडताळणी करून दिलेली अधिकृत स्वाक्षरीत दुसरी प्रत.",
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 27. Duplicate Death Certificate
  {
    "slug": "duplicate-death-certificate",
    "name_en": "Duplicate Death Certificate",
    "name_mr": "दुय्यम मृत्यू नोंद दाखला",
    "dept_code": "RURAL_DEV",
    "dept_name_en": "Rural Development & Urban Development",
    "dept_name_mr": "ग्रामविकास व नगर विकास विभाग",
    "short_description_en": "Re-issuance of certified true copy of a previously recorded death certificate.",
    "short_description_mr": "मूळ मृत्यू दाखला हरवला असल्यास नोंदवहीतून मिळणारी अधिकृत दुय्यम प्रत.",
    "description_en": "Issued by local Registrar of Births and Deaths for pending insurance and court proceedings.",
    "description_mr": "विमा व न्यायालयाच्या कामांसाठी हरवलेल्या दाखल्याऐवजी मिळणारा प्रमाणित दाखला.",
    "processing_days": 5,
    "statutory_fee_inr": 20.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 28. Nationality Certificate
  {
    "slug": "nationality-certificate",
    "name_en": "Nationality Certificate",
    "name_mr": "भारतीय राष्ट्रीयत्व प्रमाणपत्र",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department",
    "dept_name_mr": "महसूल विभाग",
    "short_description_en": "Official legal certificate proving Indian citizenship.",
    "short_description_mr": "अर्जदार भारताचा अधिकृत नागरिक असल्याचे प्रमाणित करणारा दाखला.",
    "description_en": "Issued by the Executive Magistrate / Tahsildar under the Citizenship Act.",
    "description_mr": "परदेशी शिक्षण, पासपोर्ट व संरक्षण दलातील भरतीसाठी आवश्यक राष्ट्रीयत्व दाखला.",
    "processing_days": 15,
    "statutory_fee_inr": 33.60,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 29. Permission for Tree Cutting
  {
    "slug": "permission-for-tree-cutting",
    "name_en": "Permission for Tree Cutting (Felling)",
    "name_mr": "झाडे तोडण्याची परवानगी (वृक्षतोड परवाना)",
    "dept_code": "FOREST_DEPT",
    "dept_name_en": "Forest & Urban Development Department",
    "dept_name_mr": "वन विभाग व नगर रचना",
    "short_description_en": "Statutory permission to fell or prune trees on private or agricultural land under the Maharashtra Tree Act.",
    "short_description_mr": "खाजगी किंवा शेतजमिनीवरील धोकादायक झाडे तोडण्यासाठी अधिकृत कायदेशीर परवानगी.",
    "description_en": "Issued by the Tree Officer / Range Forest Officer (RFO) / Municipal Tree Authority.",
    "description_mr": "महाराष्ट्र वृक्ष संवर्धन कायद्यानुसार झाडे तोडण्यापूर्वी घेतली जाणारी शासकीय पूर्वपरवानगी.",
    "processing_days": 30,
    "statutory_fee_inr": 100.00,
    "source_url": "https://aaplesarkar.mahaonline.gov.in"
  },
  # 30. Land Record Certified Copy (7/12 & 8-A Satbara)
  {
    "slug": "land-record-certified-copy",
    "name_en": "Land Record Certified Copy (7/12, 8-A & Ferfar)",
    "name_mr": "जमीन अभिलेख प्रमाणित नक्कल (७/१२, ८-अ व फेरफार उतारा)",
    "dept_code": "REV_DEPT",
    "dept_name_en": "Revenue Department (Land Records / Mahabhumi)",
    "dept_name_mr": "महसूल विभाग (भूमी अभिलेख / महाभूमी)",
    "short_description_en": "Certified, digitally signed copies of 7/12 Satbara, 8-A, and Form 6 Ferfar mutation entries.",
    "short_description_mr": "जमिनीची अधिकृत मालकी व क्षेत्राची डिजिटल स्वाक्षरी असलेली प्रमाणित प्रत.",
    "description_en": "Admissible in courts, banks, and sub-registrar offices with 16-digit verification code.",
    "description_mr": "बँक कर्ज, न्यायालयीन पुरावा आणि खरेदी-विक्रीसाठी थेट वैध असणारा सातबारा व फेरफार उतारा.",
    "processing_days": 1,
    "statutory_fee_inr": 15.00,
    "source_url": "https://digitalsatbara.mahabhumi.gov.in"
  }
]

def reset_to_submission_services():
    print("Connecting to database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        mh_state = db.query(State).filter_by(code="MH").first()
        pune_district = db.query(District).filter_by(code="PUN").first()
        aaple_source = db.query(Source).filter_by(url="https://aaplesarkar.mahaonline.gov.in").first()

        # Delete all existing services and child tables
        print("Clearing out old services to keep STRICTLY your 30 requested main submission services...")
        db.query(KnowledgeChunk).delete()
        db.query(ApplicationStep).delete()
        db.query(ServiceDocument).delete()
        db.query(Service).delete()
        db.commit()

        print(f"Adding exactly {len(SUBMISSION_SERVICES)} requested submission services...")

        for s_data in SUBMISSION_SERVICES:
            # 1. Department
            dept = db.query(Department).filter_by(code=s_data["dept_code"]).first()
            if not dept:
                dept = Department(
                    code=s_data["dept_code"],
                    name_en=s_data["dept_name_en"],
                    name_mr=s_data["dept_name_mr"],
                    name_hi=s_data["dept_name_en"],
                    portal_url=s_data.get("source_url", "https://aaplesarkar.mahaonline.gov.in")
                )
                db.add(dept)
                db.flush()

            # 2. Service
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

            # 3. Standard Mandatory Documents
            docs = [
                ServiceDocument(
                    service_id=svc.id,
                    name_en="Proof of Identity (Aadhaar Card / Voter ID / PAN Card)",
                    name_mr="ओळख पुरावा (आधार कार्ड / मतदार ओळखपत्र / पॅन कार्ड)",
                    name_hi="पहचान पत्र (आधार कार्ड / मतदाता पहचान पत्र)",
                    category="identity_proof",
                    is_mandatory=True,
                    description_en="Valid government-issued photo ID.",
                    display_order=1
                ),
                ServiceDocument(
                    service_id=svc.id,
                    name_en="Proof of Address (Ration Card / Electricity Bill / Property Tax Receipt)",
                    name_mr="पत्त्याचा पुरावा (रेशन कार्ड / वीज बिल / कर पावती)",
                    name_hi="पते का प्रमाण (राशन कार्ड / बिजली बिल)",
                    category="address_proof",
                    is_mandatory=True,
                    description_en="Valid utility bill or official ration card matching current residence.",
                    display_order=2
                ),
                ServiceDocument(
                    service_id=svc.id,
                    name_en="Self-Declaration Affidavit / Prescribed Application Form",
                    name_mr="स्वयंघोषणा पत्र / विहित नमुन्यातील अर्ज",
                    name_hi="स्व-घोषणा पत्र",
                    category="other",
                    is_mandatory=True,
                    description_en="Standard statutory self-declaration affidavit available on Aaple Sarkar portal.",
                    display_order=3
                )
            ]
            db.add_all(docs)

            # 4. Standard Application Steps
            steps = [
                ApplicationStep(
                    service_id=svc.id,
                    step_number=1,
                    title_en="Login to Aaple Sarkar Portal",
                    title_mr="आपले सरकार पोर्टलवर नोंदणी / लॉगिन करा",
                    title_hi="आपले सरकार पोर्टल पर लॉगिन करें",
                    instructions_en="Visit aaplesarkar.mahaonline.gov.in and log in with your citizen credentials.",
                    instructions_mr="आपले सरकार पोर्टलवर नागरिक खात्याद्वारे लॉगिन करा.",
                    instructions_hi="पोर्टल पर लॉगिन करें।",
                    external_url="https://aaplesarkar.mahaonline.gov.in"
                ),
                ApplicationStep(
                    service_id=svc.id,
                    step_number=2,
                    title_en=f"Select Service -> {s_data['name_en']}",
                    title_mr=f"सेवा निवडा -> {s_data['name_mr']}",
                    title_hi=f"सेवा चुनें -> {s_data['name_en']}",
                    instructions_en=f"Navigate to {s_data['dept_name_en']} and select {s_data['name_en']}.",
                    instructions_mr=f"{s_data['dept_name_mr']} विभागात जाऊन {s_data['name_mr']} ही सेवा निवडा.",
                    instructions_hi="संबंधित विभाग व सेवा चुनें।",
                    external_url="https://aaplesarkar.mahaonline.gov.in"
                ),
                ApplicationStep(
                    service_id=svc.id,
                    step_number=3,
                    title_en="Upload Documents & Pay Statutory Fee",
                    title_mr="कागदपत्रे अपलोड करा व अधिकृत शुल्क भरा",
                    title_hi="दस्तावेज़ अपलोड करें और शुल्क भरें",
                    instructions_en=f"Upload scanned documents and pay official fee of ₹{s_data['statutory_fee_inr']:.2f} online.",
                    instructions_mr=f"कागदपत्रे जोडून अधिकृत शुल्क ₹{s_data['statutory_fee_inr']:.2f} ऑनलाइन भरा.",
                    instructions_hi="शुल्क भरें।",
                    external_url="https://aaplesarkar.mahaonline.gov.in"
                ),
                ApplicationStep(
                    service_id=svc.id,
                    step_number=4,
                    title_en="Download Digitally Signed Certificate",
                    title_mr="डिजिटली स्वाक्षरी केलेला दाखला डाउनलोड करा",
                    title_hi="डिजिटल प्रमाण पत्र डाउनलोड करें",
                    instructions_en=f"Under the Right to Public Services Act (RTS), the certificate will be delivered within {s_data['processing_days']} working days directly to your portal dashboard.",
                    instructions_mr=f"महाराष्ट्र लोकसेवा हमी कायद्यानुसार (RTS) विहित मुदतीत ({s_data['processing_days']} कामकाजाचे दिवस) डिजिटल स्वाक्षरी असलेला दाखला थेट डाऊनलोड करा.",
                    instructions_hi="प्रमाण पत्र डाउनलोड करें।",
                    external_url="https://aaplesarkar.mahaonline.gov.in"
                )
            ]
            db.add_all(steps)

            # 5. Knowledge Chunk for AI grounding
            kc = KnowledgeChunk(
                service_id=svc.id,
                source_id=aaple_source.id if aaple_source else None,
                section_title=f"{s_data['name_en']} Overview and Statutory Rules",
                keywords=f"{s_data['name_en']} {s_data['name_mr']} fee timeline documents eligibility aaple sarkar maharashtra",
                content_en=f"{s_data['name_en']} is administered by {s_data['dept_name_en']}. {s_data['description_en']} The statutory fee is ₹{s_data['statutory_fee_inr']:.2f} and delivery timeline under Maharashtra RTS Act is {s_data['processing_days']} working days.",
                content_mr=f"{s_data['name_mr']} ही सेवा {s_data['dept_name_mr']} मार्फत पुरविली जाते. {s_data['description_mr']} अधिकृत शासकीय शुल्क ₹{s_data['statutory_fee_inr']:.2f} असून विहित मुदत {s_data['processing_days']} कामकाजाचे दिवस आहे.",
                content_hi=f"{s_data['name_en']} सेवा {s_data['dept_name_en']} द्वारा प्रदान की जाती है।"
            )
            db.add(kc)

        db.commit()
        print(f"Successfully configured exactly {len(SUBMISSION_SERVICES)} main submission services!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise e
    finally:
        db.close()

def seed_if_empty(db):
    try:
        if db.query(Service).count() == 0:
            reset_to_submission_services()
    except Exception as e:
        print(f"Auto-seed check error: {e}")

if __name__ == "__main__":
    reset_to_submission_services()
