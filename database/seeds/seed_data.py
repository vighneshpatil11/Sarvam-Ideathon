import os
import sys
from datetime import datetime, timezone

# Ensure backend app is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.database import engine, Base, SessionLocal
from app.models import (
    State, District, Department, Source, Service, ServiceDocument,
    ApplicationStep, EligibilityQuestion, EligibilityRule, KnowledgeChunk
)

def seed_database():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Service).count() > 0:
            print("Database already contains services. Skipping seed.")
            return

        print("Seeding geography & departments...")
        # State & District
        mh_state = State(name="Maharashtra", code="MH")
        db.add(mh_state)
        db.flush()

        pune_district = District(name="Pune", code="PUN", state_id=mh_state.id)
        db.add(pune_district)
        db.flush()

        # Departments
        rev_dept = Department(
            name_en="Revenue Department",
            name_hi="राजस्व विभाग",
            name_mr="महसूल विभाग",
            code="REV_DEPT",
            portal_url="https://aaplesarkar.mahaonline.gov.in"
        )
        soc_dept = Department(
            name_en="Social Justice and Special Assistance Department",
            name_hi="सामाजिक न्याय एवं विशेष सहायता विभाग",
            name_mr="सामाजिक न्याय व विशेष सहाय्य विभाग",
            code="SOC_JUSTICE",
            portal_url="https://mahadbt.maharashtra.gov.in"
        )
        db.add_all([rev_dept, soc_dept])
        db.flush()

        # Sources
        aaple_source = Source(
            title="Aaple Sarkar Citizen Services Portal - Revenue Department Guidelines",
            url="https://aaplesarkar.mahaonline.gov.in",
            publisher="Government of Maharashtra",
            source_type="official",
            supports="statutory_fees,processing_timelines,document_checklists,steps"
        )
        mahadbt_source = Source(
            title="MahaDBT Scholar Schemes and Post-Matric Guidelines",
            url="https://mahadbt.maharashtra.gov.in",
            publisher="Social Justice Department, Govt of Maharashtra",
            source_type="official",
            supports="scholarship_eligibility,mandatory_documents"
        )
        pune_rts_source = Source(
            title="Maharashtra Right to Public Services Act (RTS) Notification for Pune District",
            url="https://pune.gov.in",
            publisher="District Collectorate, Pune",
            source_type="gazette",
            supports="delivery_timelines,appeal_officers"
        )
        db.add_all([aaple_source, mahadbt_source, pune_rts_source])
        db.flush()

        # -------------------------------------------------------------
        # SERVICE 1: Income Certificate (उत्पन्नाचा दाखला)
        # -------------------------------------------------------------
        income_service = Service(
            slug="income-certificate",
            name_en="Income Certificate",
            name_hi="आय प्रमाण पत्र",
            name_mr="उत्पन्नाचा दाखला",
            short_description_en="Official certificate validating total annual family income for scholarships, fee concessions, and government welfare schemes.",
            short_description_hi="छात्रवृत्ति, शुल्क छूट और सरकारी योजनाओं के लिए वार्षिक पारिवारिक आय प्रमाणित करने वाला आधिकारिक दस्तावेज।",
            short_description_mr="शिष्यवृत्ती, शैक्षणिक सवलती आणि विविध शासकीय योजनांचा लाभ घेण्यासाठी कुटुंबाच्या वार्षिक उत्पन्नाचा अधिकृत दाखला.",
            description_en="Issued by the Sub-Divisional Officer or Tahsildar under the Revenue Department. Valid for one financial year or three consecutive financial years depending on application type.",
            description_hi="राजस्व विभाग के तहसीलदार अथवा उप-विभागीय अधिकारी द्वारा जारी किया जाता है। यह छात्रवृत्ति तथा अन्य योजनाओं के लिए मान्य है।",
            description_mr="महसूल विभागातील तहसीलदार किंवा उपविभागीय अधिकाऱ्यांमार्फत हा दाखला दिला जातो. शैक्षणिक शिष्यवृत्ती आणि शासकीय योजनांसाठी हा अनिवार्य मानला जातो.",
            department_id=rev_dept.id,
            jurisdiction_level="district",
            state="Maharashtra",
            statutory_fee_inr=33.60,
            processing_days=15,
            official_portal_url="https://aaplesarkar.mahaonline.gov.in",
            official_tracking_url="https://aaplesarkar.mahaonline.gov.in/en/TrackStatus",
            verification_status="verified",
            is_demo=False
        )
        income_service.districts.append(pune_district)
        income_service.sources.extend([aaple_source, pune_rts_source])
        db.add(income_service)
        db.flush()

        # Income Docs
        db.add_all([
            ServiceDocument(
                service_id=income_service.id,
                name_en="Proof of Identity (Voter ID, Driving License, or Passport)",
                name_hi="पहचान प्रमाण (मतदाता पहचान पत्र, ड्राइविंग लाइसेंस)",
                name_mr="ओळख पुरावा (मतदार ओळखपत्र, वाहन परवाना किंवा पासपोर्ट)",
                category="identity_proof",
                is_mandatory=True,
                description_en="Clear scanned copy of government-issued photo ID.",
                issuing_authority="Election Commission / Transport Authority",
                display_order=1
            ),
            ServiceDocument(
                service_id=income_service.id,
                name_en="Proof of Address (Ration Card, Electricity Bill, or Water Bill)",
                name_hi="पते का प्रमाण (राशन कार्ड, बिजली बिल)",
                name_mr="पत्त्याचा पुरावा (रेशन कार्ड, वीज बिल किंवा पाणी बिल)",
                category="address_proof",
                is_mandatory=True,
                description_en="Valid utility bill or official ration card matching current Pune residence.",
                issuing_authority="MSEDCL / Food & Civil Supplies",
                display_order=2
            ),
            ServiceDocument(
                service_id=income_service.id,
                name_en="Income Proof (Salary Slip Form 16, ITR, or Talathi Income Report)",
                name_hi="आय प्रमाण (वेतन पर्ची, आईटीआर, या तलाठी आय रिपोर्ट)",
                name_mr="उत्पन्नाचा पुरावा (वेतन प्रमाणपत्र फॉर्म १६, आयकर विवरणपत्र किंवा तलाठी अहवाल)",
                category="income_proof",
                is_mandatory=True,
                description_en="Certified salary slip for salaried applicants or Talathi verification certificate for agricultural/informal income.",
                issuing_authority="Employer / Revenue Talathi",
                display_order=3
            ),
            ServiceDocument(
                service_id=income_service.id,
                name_en="Self-Declaration Affidavit (Form 1)",
                name_hi="स्व-घोषणा पत्र (प्रारूप 1)",
                name_mr="स्वयंघोषणा पत्र (प्रारूप १)",
                category="other",
                is_mandatory=True,
                description_en="Standard statutory self-declaration affidavit available on Aaple Sarkar portal.",
                issuing_authority="Aaple Sarkar Portal",
                display_order=4
            )
        ])

        # Income Questions & Rules
        db.add_all([
            EligibilityQuestion(
                service_id=income_service.id,
                field_key="is_maharashtra_resident",
                question_type="boolean",
                label_en="Are you a permanent resident residing in Maharashtra?",
                label_hi="क्या आप महाराष्ट्र के स्थायी निवासी हैं?",
                label_mr="आपण महाराष्ट्राचे कायमस्वरूपी रहिवासी आहात का?",
                help_text_en="Applicant or family must reside within the territorial jurisdiction of Maharashtra.",
                required=True,
                display_order=1
            ),
            EligibilityQuestion(
                service_id=income_service.id,
                field_key="annual_family_income",
                question_type="number",
                label_en="What is your gross annual family income from all sources (in INR)?",
                label_hi="सभी स्रोतों से आपकी कुल वार्षिक पारिवारिक आय कितनी है (रुपये में)?",
                label_mr="सर्व मार्गांनी मिळणारे आपल्या कुटुंबाचे एकूण वार्षिक उत्पन्न किती आहे (रुपयांमध्ये)?",
                help_text_en="Enter your total annual household income before taxes.",
                required=True,
                display_order=2
            )
        ])

        db.add_all([
            EligibilityRule(
                service_id=income_service.id,
                rule_code="INC_RESIDENCY",
                description="Applicant must be a resident of Maharashtra state.",
                field_key="is_maharashtra_resident",
                operator="eq",
                expected_value="true",
                is_disqualifying=True,
                failure_message_en="Applicant must reside in Maharashtra to obtain a Maharashtra state income certificate.",
                failure_message_hi="महाराष्ट्र राज्य का आय प्रमाण पत्र प्राप्त करने के लिए आवेदक का महाराष्ट्र में निवास आवश्यक है।",
                failure_message_mr="महाराष्ट्र शासनाचा उत्पन्नाचा दाखला मिळवण्यासाठी अर्जदाराचे महाराष्ट्रात वास्तव्य असणे अनिवार्य आहे."
            ),
            EligibilityRule(
                service_id=income_service.id,
                rule_code="INC_POSITIVE_VAL",
                description="Annual income must be greater than or equal to 0.",
                field_key="annual_family_income",
                operator="gte",
                expected_value="0",
                is_disqualifying=True,
                failure_message_en="Annual family income must be a valid non-negative number.",
                failure_message_hi="वार्षिक पारिवारिक आय वैध गैर-ऋणात्मक संख्या होनी चाहिए।",
                failure_message_mr="वार्षिक कौटुंबिक उत्पन्न योग्य सकारात्मक संख्या असावे."
            )
        ])

        # Income Steps
        db.add_all([
            ApplicationStep(
                service_id=income_service.id,
                step_number=1,
                title_en="Register / Login on Aaple Sarkar Portal",
                title_hi="आपले सरकार पोर्टल पर पंजीकरण / लॉगिन करें",
                title_mr="आपले सरकार पोर्टलवर नोंदणी / लॉगिन करा",
                instructions_en="Visit aaplesarkar.mahaonline.gov.in. Create Citizen Profile with mobile OTP and email verification.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            ),
            ApplicationStep(
                service_id=income_service.id,
                step_number=2,
                title_en="Select Revenue Department -> Income Certificate",
                title_hi="राजस्व विभाग -> आय प्रमाण पत्र चुनें",
                title_mr="महसूल विभाग -> उत्पन्नाचा दाखला निवडा",
                instructions_en="Navigate to Revenue Services section and select 'Income Certificate (उत्पन्नाचा दाखला)'.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            ),
            ApplicationStep(
                service_id=income_service.id,
                step_number=3,
                title_en="Upload Documents & Pay Statutory Fee",
                title_hi="दस्तावेज अपलोड करें और वैधानिक शुल्क का भुगतान करें",
                title_mr="कागदपत्रे अपलोड करा आणि अधिकृत शुल्क भरा",
                instructions_en="Upload scanned PDF/JPEG proofs (Identity, Address, Income report). Pay official fee of ₹33.60 via UPI/Netbanking.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            ),
            ApplicationStep(
                service_id=income_service.id,
                step_number=4,
                title_en="Download Digitally Signed Certificate",
                title_hi="डिजिटल रूप से हस्ताक्षरित प्रमाण पत्र डाउनलोड करें",
                title_mr="डिजिटली स्वाक्षरी केलेला दाखला डाउनलोड करा",
                instructions_en="Under the Right to Public Services Act, the Tahsildar processes the request within 15 working days. Download the barcode-verified certificate directly from your dashboard.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            )
        ])

        # Knowledge Chunks
        db.add(KnowledgeChunk(
            service_id=income_service.id,
            source_id=aaple_source.id,
            section_title="Income Certificate Rules & Fees",
            keywords="income certificate fee timeline aaple sarkar maharashtra",
            content_en="The statutory fee for an Income Certificate in Maharashtra is ₹33.60 on the Aaple Sarkar portal. Under the Maharashtra Right to Public Services Act, it must be delivered within 15 working days by the local Tahsildar office.",
            content_hi="महाराष्ट्र में आय प्रमाण पत्र के लिए वैधानिक शुल्क आपले सरकार पोर्टल पर ₹33.60 है। लोक सेवा अधिकार अधिनियम के तहत, इसे स्थानीय तहसीलदार कार्यालय द्वारा 15 कार्य दिवसों में जारी किया जाना चाहिए।",
            content_mr="महाराष्ट्रात उत्पन्नाच्या दाखल्यासाठी आपले सरकार पोर्टलवर अधिकृत वैधानिक शुल्क ₹३३.६० आहे. महाराष्ट्र लोकसेवा हमी कायद्यानुसार, स्थानिक तहसीलदार कार्यालयाकडून हा दाखला १५ कामकाजाच्या दिवसांत मिळणे बंधनकारक आहे."
        ))

        # -------------------------------------------------------------
        # SERVICE 2: Domicile Certificate (अधिवास प्रमाणपत्र)
        # -------------------------------------------------------------
        domicile_service = Service(
            slug="domicile-certificate",
            name_en="Domicile & Nationality Certificate",
            name_hi="अधिवास एवं राष्ट्रीयता प्रमाण पत्र",
            name_mr="अधिवास व राष्ट्रीयत्व प्रमाणपत्र",
            short_description_en="Official legal certificate proving permanent residence in Maharashtra for admission, state government employment, and quotas.",
            short_description_hi="महाराष्ट्र में स्थायी निवास सिद्ध करने वाला आधिकारिक प्रमाण पत्र जो शिक्षा, राज्य नौकरियों और आरक्षण के लिए आवश्यक है।",
            short_description_mr="शिक्षण प्रवेश, शासकीय नोकऱ्या आणि विविध आरक्षित लाभांसाठी महाराष्ट्रात सलग वास्तव्य सिद्ध करणारे अधिवास प्रमाणपत्र.",
            description_en="Issued by the Revenue Executive Magistrate (Tahsildar). Requires verified proof of continuous 15 years physical residence in the State of Maharashtra.",
            description_hi="राजस्व कार्यपालक दंडाधिकारी (तहसीलदार) द्वारा जारी। इसके लिए महाराष्ट्र राज्य में न्यूनतम 15 वर्ष का निरंतर निवास अनिवार्य है।",
            description_mr="कार्यकारी दंडाधिकारी (तहसीलदार) यांच्याकडून जारी केले जाते. यासाठी अर्जदाराचे किंवा पालकांचे महाराष्ट्रात सलग किमान १५ वर्षे वास्तव्य असणे बंधनकारक आहे.",
            department_id=rev_dept.id,
            jurisdiction_level="district",
            state="Maharashtra",
            statutory_fee_inr=33.60,
            processing_days=15,
            official_portal_url="https://aaplesarkar.mahaonline.gov.in",
            official_tracking_url="https://aaplesarkar.mahaonline.gov.in/en/TrackStatus",
            verification_status="verified",
            is_demo=False
        )
        domicile_service.districts.append(pune_district)
        domicile_service.sources.extend([aaple_source, pune_rts_source])
        db.add(domicile_service)
        db.flush()

        db.add_all([
            ServiceDocument(
                service_id=domicile_service.id,
                name_en="Continuous 15-Year Residence Proof in Maharashtra",
                name_hi="महाराष्ट्र में लगातार 15 वर्षों के निवास का प्रमाण",
                name_mr="महाराष्ट्रात सलग १५ वर्षे वास्तव्याचा पुरावा (शाळा सोडल्याचा दाखला, भाडे करार, वीज बिले)",
                category="address_proof",
                is_mandatory=True,
                description_en="School Leaving Certificate (LC), residential utility bills spanning 15 years, or registered property records.",
                issuing_authority="School / Revenue Authority",
                display_order=1
            ),
            ServiceDocument(
                service_id=domicile_service.id,
                name_en="Birth Certificate / School Leaving Certificate",
                name_hi="जन्म प्रमाण पत्र / स्कूल लीविंग सर्टिफिकेट",
                name_mr="जन्म दाखला / शाळा सोडल्याचा दाखला (TC/LC)",
                category="identity_proof",
                is_mandatory=True,
                description_en="Showing place of birth in Maharashtra.",
                issuing_authority="Municipal Corporation / Gram Panchayat",
                display_order=2
            )
        ])

        db.add_all([
            EligibilityQuestion(
                service_id=domicile_service.id,
                field_key="residence_years_in_maharashtra",
                question_type="number",
                label_en="How many continuous years have you resided in Maharashtra?",
                label_hi="आप लगातार कितने वर्षों से महाराष्ट्र में निवास कर रहे हैं?",
                label_mr="आपण महाराष्ट्रात सलग किती वर्षे वास्तव्य करत आहात?",
                help_text_en="Statutory rule requires a minimum of 15 years of continuous residency.",
                required=True,
                display_order=1
            )
        ])

        db.add_all([
            EligibilityRule(
                service_id=domicile_service.id,
                rule_code="DOM_15_YEARS",
                description="Continuous residency must be >= 15 years.",
                field_key="residence_years_in_maharashtra",
                operator="gte",
                expected_value="15",
                is_disqualifying=True,
                failure_message_en="Domicile certificate requires minimum 15 consecutive years of residence in Maharashtra.",
                failure_message_hi="अधिवास प्रमाण पत्र के लिए महाराष्ट्र में न्यूनतम 15 वर्ष का निरंतर निवास अनिवार्य है।",
                failure_message_mr="अधिवास प्रमाणपत्रासाठी महाराष्ट्रात सलग किमान १५ वर्षे वास्तव्य असणे बंधनकारक आहे."
            )
        ])

        db.add_all([
            ApplicationStep(
                service_id=domicile_service.id,
                step_number=1,
                title_en="Aaple Sarkar Registration",
                title_hi="आपले सरकार पंजीकरण",
                title_mr="आपले सरकार नोंदणी",
                instructions_en="Login to Aaple Sarkar and choose 'Age, Nationality and Domicile Certificate' under Revenue Department.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            ),
            ApplicationStep(
                service_id=domicile_service.id,
                step_number=2,
                title_en="Submit Residence Proofs & Pay Fee",
                title_hi="निवास प्रमाण अपलोड करें और शुल्क भरें",
                title_mr="वास्तव्याचे पुरावे जोडून शुल्क भरा",
                instructions_en="Upload 15-year residency records. Pay statutory fee of ₹33.60.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            ),
            ApplicationStep(
                service_id=domicile_service.id,
                step_number=3,
                title_en="Verification and Delivery",
                title_hi="सत्यापन एवं प्राप्ति",
                title_mr="पडताळणी आणि दाखला प्राप्ती",
                instructions_en="Tahsildar office verifies records within 15 working days. Download certificate online.",
                external_url="https://aaplesarkar.mahaonline.gov.in"
            )
        ])

        # Knowledge Chunks
        db.add(KnowledgeChunk(
            service_id=domicile_service.id,
            source_id=aaple_source.id,
            section_title="Domicile Certificate 15-Year Residency Rule",
            keywords="domicile certificate 15 years maharashtra fee",
            content_en="To obtain a Domicile Certificate in Maharashtra, the applicant must have lived in the state continuously for at least 15 years. The statutory fee is ₹33.60, and statutory delivery time is 15 working days.",
            content_hi="महाराष्ट्र में अधिवास प्रमाण पत्र प्राप्त करने के लिए आवेदक का कम से कम 15 वर्ष लगातार राज्य में रहना आवश्यक है। वैधानिक शुल्क ₹33.60 है और समय सीमा 15 कार्य दिवस है।",
            content_mr="महाराष्ट्रात अधिवास प्रमाणपत्र मिळवण्यासाठी अर्जदाराचे राज्यात सलग किमान १५ वर्षे वास्तव्य असणे आवश्यक आहे. अधिकृत शुल्क ₹३३.६० असून विहित मुदत १५ कामकाजाचे दिवस आहे."
        ))

        # -------------------------------------------------------------
        # SERVICE 3: Non-Creamy Layer Certificate (नॉन-क्रीमी लेयर)
        # -------------------------------------------------------------
        ncl_service = Service(
            slug="non-creamy-layer-certificate",
            name_en="Non-Creamy Layer Certificate",
            name_hi="गैर-क्रीमी लेयर प्रमाण पत्र (NCL)",
            name_mr="नॉन-क्रीमी लेयर प्रमाणपत्र",
            short_description_en="Mandatory certificate for VJNT, OBC, and SBC categories to avail reservation benefits in education and government employment.",
            short_description_hi="शिक्षा और नौकरियों में आरक्षण लाभ प्राप्त करने के लिए ओबीसी/वीजेएनटी/एसबीसी श्रेणियों के लिए अनिवार्य प्रमाण पत्र।",
            short_description_mr="शैक्षणिक प्रवेश आणि शासकीय नोकऱ्यांमध्ये आरक्षणाचा लाभ मिळवण्यासाठी विमुक्त जाती, भटक्या जमाती, इतर मागासवर्ग (OBC) प्रवर्गासाठी आवश्यक प्रमाणपत्र.",
            description_en="Certifies that the applicant does not belong to the affluent (Creamy Layer) section of backward classes. Gross annual family income must not exceed ₹8.00 Lakhs in preceding 3 consecutive financial years.",
            description_hi="यह प्रमाणित करता है कि आवेदक क्रीमी लेयर में नहीं आता है। विगत 3 वित्तीय वर्षों में पारिवारिक सकल आय ₹8 लाख से अधिक नहीं होनी चाहिए।",
            description_mr="अर्जदार मागासवर्गीय प्रवर्गातील प्रगत व उन्नत (क्रीमी लेयर) गटात मोडत नसल्याचे हे प्रमाणपत्र असते. मागील सलग ३ आर्थिक वर्षांतील कुटुंबाचे उत्पन्न ₹८ लाखांपेक्षा जास्त नसावे.",
            department_id=soc_dept.id,
            jurisdiction_level="state",
            state="Maharashtra",
            statutory_fee_inr=33.60,
            processing_days=21,
            official_portal_url="https://aaplesarkar.mahaonline.gov.in",
            verification_status="verified",
            is_demo=False
        )
        ncl_service.districts.append(pune_district)
        ncl_service.sources.append(aaple_source)
        db.add(ncl_service)
        db.flush()

        db.add_all([
            EligibilityQuestion(
                service_id=ncl_service.id,
                field_key="annual_income_last_3_years_max",
                question_type="number",
                label_en="What was your family's highest annual income across the last 3 financial years (in INR)?",
                label_hi="पिछले 3 वित्तीय वर्षों में आपके परिवार की उच्चतम वार्षिक आय कितनी थी (रुपये में)?",
                label_mr="मागील ३ आर्थिक वर्षांमध्ये आपल्या कुटुंबाचे कमाल वार्षिक उत्पन्न किती होते (रुपयांमध्ये)?",
                help_text_en="Statutory income ceiling is ₹8,00,000 (8 Lakhs).",
                required=True,
                display_order=1
            )
        ])

        db.add_all([
            EligibilityRule(
                service_id=ncl_service.id,
                rule_code="NCL_INCOME_CEILING",
                description="Annual income across 3 years must be <= 800000.",
                field_key="annual_income_last_3_years_max",
                operator="lte",
                expected_value="800000",
                is_disqualifying=True,
                failure_message_en="Family gross income must not exceed ₹8,00,000 to be eligible for Non-Creamy Layer status.",
                failure_message_hi="गैर-क्रीमी लेयर पात्रता के लिए परिवार की सकल आय ₹8,00,000 से अधिक नहीं होनी चाहिए।",
                failure_message_mr="नॉन-क्रीमी लेयर प्रमाणपत्रासाठी कुटुंबाचे वार्षिक उत्पन्न ₹८ लाखांपेक्षा जास्त असू नये."
            )
        ])

        # -------------------------------------------------------------
        # SERVICE 4: MahaDBT Post-Matric Scholarship
        # -------------------------------------------------------------
        sch_service = Service(
            slug="mahadbt-post-matric-scholarship",
            name_en="Post-Matric Scholarship Scheme (MahaDBT)",
            name_hi="पोस्ट-मैट्रिक छात्रवृत्ति योजना (महाडीबीटी)",
            name_mr="मॅट्रिकोत्तर शिष्यवृत्ती योजना (महाडीबीटी)",
            short_description_en="State scholarship providing tuition fee waiver and maintenance allowance for post-secondary college students in Maharashtra.",
            short_description_hi="महाराष्ट्र में उच्च शिक्षा प्राप्त कर रहे विद्यार्थियों के लिए शिक्षण शुल्क प्रतिपूर्ति एवं निर्वाह भत्ता योजना।",
            short_description_mr="महाराष्ट्रातील उच्च शिक्षण घेणाऱ्या विद्यार्थ्यांसाठी परीक्षा फी, शिक्षण शुल्क माफी आणि निर्वाह भत्ता देणारी राज्य शिष्यवृत्ती योजना.",
            description_en="Administered by the Social Justice & Special Assistance Department via the central MahaDBT DBT portal.",
            description_hi="सामाजिक न्याय विभाग द्वारा महाडीबीटी पोर्टल के माध्यम से संचालित।",
            description_mr="सामाजिक न्याय व विशेष सहाय्य विभागामार्फत महाडीबीटी पोर्टलद्वारे थेट बँक खात्यात शिष्यवृत्ती वितरित केली जाते.",
            department_id=soc_dept.id,
            jurisdiction_level="state",
            state="Maharashtra",
            statutory_fee_inr=0.00,
            processing_days=30,
            official_portal_url="https://mahadbt.maharashtra.gov.in",
            verification_status="verified",
            is_demo=False
        )
        sch_service.districts.append(pune_district)
        sch_service.sources.append(mahadbt_source)
        db.add(sch_service)

        db.commit()
        print("Database successfully seeded with verified government pilot records!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
