# SAARTHI — End-to-End Demonstration Script

Follow this structured workflow to demonstrate SAARTHI's capabilities to stakeholders.

---

## Act 1: Plain-Language Discovery
1. **Open Frontend**: Navigate to `http://localhost:3000`.
2. **Observe UI**:
   - Note the bilingual/multilingual header (English, Hindi, Marathi switcher).
   - Prominent disclaimer confirming SAARTHI is an independent navigation platform.
3. **Execute Natural-Language Query**:
   - Type: `"I need an income certificate for my college scholarship"`
   - Click **Search Services** or press Enter.
   - Result: Service card for **Income Certificate (उत्पन्नाचा दाखला)** appears with verification badge, issuing department, and delivery timeline.

---

## Act 2: Service Deep-Dive & Deterministic Eligibility
1. Click on **View Service Details** for the Income Certificate.
2. Review:
   - Official Department: Revenue Department, Maharashtra
   - Statutory Processing Time: 15 Working Days
   - Official Statutory Fee: ₹33.60
   - Provenance: Clickable official source links pointing to `aaplesarkar.mahaonline.gov.in`.
3. Click **Check Eligibility**:
   - Answer Question 1: *"Are you a permanent resident of Maharashtra?"* -> Select **Yes**.
   - Answer Question 2: *"What is your gross annual family income?"* -> Enter `75000`.
   - Click **Evaluate Eligibility**.
   - Result: **Potentially Eligible** with a transparent explanation and zero hallucination.

---

## Act 3: Document Checklist & Application Steps
1. Navigate to **Document Checklist**:
   - Review categorized documents: Proof of Identity, Proof of Residence, Income Proof.
   - Check off items as a personal preparation guide (local checklist state).
2. Navigate to **Application Guide**:
   - Review ordered steps: Register on Aaple Sarkar -> Select Revenue Services -> Upload documents -> Pay statutory fee (₹33.60) -> Download signed certificate.
   - Click the external portal button to verify link to Aaple Sarkar.

---

## Act 4: Grounded Sarvam AI Assistant
1. Click **Ask Assistant** in header or on service page.
2. Prompt: *"How long does it take to get an income certificate in Pune, and what is the fee?"*
3. Response:
   - Powered by Sarvam AI (`sarvam-105b-conversations`).
   - States: Exactly 15 working days and ₹33.60 as grounded in official data.
   - Direct citations rendered at bottom of message.
4. Switch language to **Marathi (मराठी)**:
   - Prompt: *"उत्पन्नाच्या दाखल्यासाठी कोणते कागदपत्रे लागतील?"*
   - Response in fluent Marathi detailing the exact documents.

---

## Act 5: Protected Administration
1. Open Swagger Docs at `http://localhost:8000/docs`.
2. Login with `admin@saarthi.local` / `AdminSecurePassword123!` to obtain JWT token.
3. Inspect `/api/v1/admin/services` and audit log trails.
