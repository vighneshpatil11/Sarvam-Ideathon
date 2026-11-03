# SAARTHI — Data Governance & Verification Policy

## 1. Hierarchy of Source Authority
Information published on SAARTHI must adhere strictly to the following authority tier:
1. **Tier 1 (Authoritative Law & Rule)**: Acts of Legislature, Official Government Gazettes, Government Resolutions (GRs).
2. **Tier 2 (Official Government Portals)**: Primary domain portals ending in `.gov.in` or `.nic.in` (e.g., `aaplesarkar.mahaonline.gov.in`, `mahadbt.maharashtra.gov.in`).
3. **Tier 3 (Departmental Citizen Charters)**: Published Citizen Charters signed by District Collectorates or Departmental Heads.
4. **Disallowed**: Third-party blogs, commercial aggregator websites, unverified news media, social media forums.

## 2. Verification Life Cycle
All records maintain an explicit `verification_status`:
- `draft`: Freshly created or extracted; hidden from public citizen queries.
- `needs_review`: Flagged due to source changes, user feedback, or automated link decay.
- `verified`: Manually reviewed by an administrator against an active official portal or gazette with recorded source URL and timestamp.
- `expired`: Has exceeded the maximum re-verification window (default: 90 days for statutory fees/timelines).
- `disputed`: Conflicting rules detected across departmental branches.

## 3. Provenance Retention
Every published service record, document requirement, fee structure, and eligibility rule retains a foreign-key relationship to a `Source` entity containing:
- Canonical Title
- Source URL
- Publishing Department / Authority
- Publication Date
- Verification Check Date
- Supported Data Fields
