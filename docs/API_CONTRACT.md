# SAARTHI — API Contract Specification

All endpoints are prefixed with `/api/v1`.

## Standard Envelope Format
### Success Envelope
```json
{
  "success": true,
  "data": { ... },
  "meta": null
}
```

### Error Envelope
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Specific human-readable message",
    "details": null
  }
}
```

---

## 1. Public Citizen Endpoints

### `GET /api/v1/health`
Health check and database ping.
- Response: `{"success": true, "data": {"status": "ok", "app": "SAARTHI", "version": "1.0.0", "database": "connected"}}`

### `GET /api/v1/services`
List all published government services with optional filtering.
- Query Parameters:
  - `department_id` (optional string)
  - `state` (optional string)
  - `district` (optional string)
  - `language` (optional enum: `en`, `hi`, `mr`)

### `GET /api/v1/services/{slug}`
Retrieve full details for a service, including jurisdiction, notes, verification status, and sources.

### `POST /api/v1/search`
Natural language search across service catalog.
- Request Body:
```json
{
  "query": "income certificate for scholarship",
  "language": "en",
  "state": "Maharashtra",
  "district": "Pune"
}
```

### `GET /api/v1/services/{slug}/documents`
Get required and conditional document checklist with justifications and issuing authorities.

### `GET /api/v1/services/{slug}/eligibility/questions`
Retrieve dynamic eligibility questionnaire with types (`boolean`, `single_choice`, `number`, `text`).

### `POST /api/v1/services/{slug}/eligibility/evaluate`
Evaluate user answers deterministically.
- Request Body:
```json
{
  "answers": {
    "is_maharashtra_resident": true,
    "annual_family_income": 80000
  },
  "language": "en"
}
```
- Response Status: `potentially_eligible` | `potentially_not_eligible` | `more_information_required` | `unable_to_determine`

### `GET /api/v1/services/{slug}/steps`
Retrieve ordered application steps, statutory fees, guaranteed timelines, and official portal URLs.

### `POST /api/v1/assistant/chat`
Ask the grounded AI assistant.
- Request Body:
```json
{
  "message": "What is the fee for income certificate?",
  "session_id": "optional-uuid",
  "language": "en",
  "context": {
    "service_slug": "income-certificate"
  }
}
```

### `POST /api/v1/feedback`
Submit citizen feedback on information clarity or portal issues.

---

## 2. Protected Admin Endpoints
- `POST /api/v1/admin/auth/login` (Returns Bearer JWT)
- `GET /api/v1/admin/services`
- `POST /api/v1/admin/services`
- `PATCH /api/v1/admin/services/{id}`
- `POST /api/v1/admin/sources`
- `POST /api/v1/admin/services/{id}/publish`
- `GET /api/v1/admin/feedback`
- `GET /api/v1/admin/source-checks`
