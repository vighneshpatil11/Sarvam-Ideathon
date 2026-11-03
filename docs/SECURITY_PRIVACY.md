# SAARTHI — Security & Privacy Architecture

## 1. Zero-Retention Citizen Privacy Architecture
- **No Citizen Accounts**: Citizens can discover, evaluate eligibility, and review document checklists anonymously.
- **Strictly No Sensitive Identifiers**:
  - Never ask for Aadhaar numbers, PAN, Passport, or Voter ID numbers.
  - Never ask for passwords, OTPs, UPI PINs, ATM PINs, or bank account credentials.
  - No file upload of actual identity documents in MVP.
- **Ephemerality**: Dynamic eligibility calculations occur entirely in-memory and are not linked to persistent user profiles.

## 2. Admin Security Controls
- **Authentication**: Cryptographic password hashing using PBKDF2/Bcrypt with strong salt. Bearer JWT tokens signed with HS256 and configurable expiration.
- **Authorization**: Role-based access control protecting all mutative operations (`POST`, `PATCH`, `DELETE`).
- **Audit Logging**: Every administrative state change (service creation, rule modification, content publication) is recorded in `admin_audit_logs`.

## 3. Network & Transport Security
- **Strict CORS Policy**: Whitelists only designated frontend origins (e.g. `http://localhost:3000`).
- **Safe Outbound Communication**: The backend strictly validates URLs before outgoing HTTP fetch requests.
- **Secure Provider Handling**: Sarvam AI API keys reside exclusively in backend environment variables and are never surfaced to the browser or public API responses.
