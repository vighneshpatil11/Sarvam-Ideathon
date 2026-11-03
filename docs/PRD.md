# SAARTHI — Product Requirements Document (PRD)

## 1. Executive Summary
**SAARTHI** is an independent, multilingual Government Service Navigation Platform designed to empower citizens in Maharashtra (pilot focus: Pune district) to effortlessly discover, understand, and navigate public welfare schemes and official certificate procedures in plain language.

## 2. Problem Statement
Citizens frequently face significant friction when trying to access state services:
- Complex administrative jargon and opaque rules.
- Reliance on commercial cyber-café intermediaries who often overcharge.
- Disconnected departmental websites with varying document requirements.
- Risk of rejection due to missing or misformatted documentation.
- Uncertainty regarding actual official fees and delivery timelines.

## 3. Goals & Non-Goals
### Goals
- Accept citizen queries in ordinary language (English, Hindi, Marathi).
- Deterministically evaluate preliminary eligibility via dynamic, verifiable rule logic.
- Provide comprehensive, verified document checklists and official portal guidance.
- Offer an AI navigation assistant grounded strictly in verified government sources.
- Complete transparency: every fact includes source links, publishers, and verification dates.

### Non-Goals
- SAARTHI is **not** a government authority and does not make official determinations or approve applications.
- SAARTHI does **not** process financial transactions or collect citizen identity documents (no Aadhaar, PAN, bank accounts).
- SAARTHI does **not** replace official state portals (e.g. Aaple Sarkar, Mahadbt).

## 4. User Personas & Journeys
1. **Ramesh (Farmer / Rural Resident)**: Needs an Income Certificate for agricultural crop loans. Searches in Marathi, answers 3 simple eligibility questions, receives a checklist with Tehsildar office details and Aaple Sarkar link.
2. **Pooja (College Student)**: Seeking state post-matric scholarships. Searches in Hindi, checks income thresholds, gets step-by-step Mahadbt application guide.
3. **Kiran (Urban Citizen)**: Needs Domicile Certificate for employment. Verifies continuous 15-year residence requirement and official statutory fee (₹33.60).

## 5. Success Metrics
- 0% invented or hallucinated requirements, rules, or fees.
- 100% of published services linked to verifiable government sources.
- Sub-200ms API response time on search and eligibility evaluation.
- Responsive mobile performance accessible on basic 4G smartphones.
