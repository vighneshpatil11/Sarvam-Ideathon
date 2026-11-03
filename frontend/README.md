# SAARTHI Frontend

A responsive, multilingual Next.js frontend for SAARTHI — an independent government-service navigation and explanation platform. This directory contains **frontend code only**. It does not create or replace the Django backend, database, authentication system, or AI provider integration.

## What is included

- Next.js App Router + React + TypeScript.
- Responsive homepage and service journey pages.
- Service directory, service details, eligibility questionnaire, document checklist and application guide.
- Text-only assistant interface with source and warning presentation.
- About, privacy guidance, loading, empty, error and not-found states.
- English, Hindi and Marathi UI dictionaries with browser-persisted language selection.
- Centralized typed API client for the documented `/api/v1` endpoints.
- Clearly labelled demo mode with illustrative records and no invented government rules, fees, document requirements or official links.
- URL validation for external source links (HTTPS only).
- Basic Vitest tests.

## Requirements

- Node.js 20 LTS or newer (Node 20+ recommended).
- npm 10+.
- Django backend running separately if using live mode.

## Run locally

From the project root:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Windows PowerShell:

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

The included `.env.example` enables demo mode by default so the interface can be explored without a running backend. The demo banner is persistent and explicit.

## Environment variables

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DEMO_MODE=true
```

- `NEXT_PUBLIC_API_BASE_URL`: base URL of the existing Django API. The `/api/v1` prefix belongs here once; endpoint modules append only the relative endpoint paths.
- `NEXT_PUBLIC_DEMO_MODE`: set `true` to use illustrative local demo content; set `false` to call the backend. In live mode, backend failures are shown as errors and never silently replaced with demo data.

No API secret belongs in this frontend. In particular, **do not add `SARVAM_API_KEY` or any provider secret to a `NEXT_PUBLIC_*` variable**. Sarvam credentials must remain server-side in the Django backend.

## Backend integration contract

The API modules are in `src/lib/api/`. All fetch requests pass through `src/lib/api/client.ts`.

| Method | Relative path | Frontend use |
|---|---|---|
| GET | `/health` | Health check (available to integration tooling) |
| GET | `/services` | Service directory |
| GET | `/services/{slug}` | Service detail |
| POST | `/search` | Search services |
| GET | `/services/{slug}/documents` | Document checklist |
| GET | `/services/{slug}/eligibility/questions` | Eligibility questions |
| POST | `/services/{slug}/eligibility/evaluate` | Evaluate answers |
| GET | `/services/{slug}/steps` | Application guide |
| POST | `/assistant/chat` | Text assistant |
| POST | `/feedback` | Feedback module (API client only; no unsolicited feedback form) |

The supplied frontend README defines proposed payload shapes and a common `{ success, data, meta }` success envelope. The actual Django OpenAPI schema was not supplied, so these types are a **contract proposal**, not proof of Django endpoint implementation. Before live integration, compare the Django OpenAPI schema with `src/types/index.ts` and the API modules. Update field names and request bodies to match the real backend; do not add guessed endpoints.

If the Django backend uses cookie/session authentication, configure CORS and credentials deliberately in the backend and update the API client after the backend owner confirms the auth design. No citizen login is implemented in this MVP.

## Pages and user journey

| Route | Purpose |
|---|---|
| `/` | Product introduction, service search, how-it-works journey |
| `/services` | Search and browse services |
| `/services/[slug]` | Service overview, source details and journey actions |
| `/services/[slug]/eligibility` | Backend-defined questions and preliminary result |
| `/services/[slug]/documents` | Backend-defined checklist with local checkbox state |
| `/services/[slug]/guide` | Backend-defined steps and validated HTTPS links |
| `/assistant` | Session-only text chat, sources, related services and warnings |
| `/about` | Platform role, limitations and privacy guidance |
| not-found | Friendly 404 fallback |

## Demo mode limitations

Demo service cards are illustrative examples to exercise navigation. They are not represented as verified government service records. The demo includes no official portal links, eligibility rules, fees, processing timelines or document requirements. The demo eligibility form deliberately returns `unable_to_determine`; it does not calculate eligibility. The demo assistant clearly says it is not connected to a live knowledge base.

## Quality checks

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

## Project structure

```text
frontend/
├── public/
├── src/
│   ├── app/                 # App Router pages and global styles
│   ├── components/          # Shared layout, cards, search and UI states
│   ├── context/             # Language/application context
│   ├── data/demo/           # Explicitly illustrative demo records
│   ├── i18n/                # en, hi, mr dictionaries
│   ├── lib/api/              # Central API client and endpoint modules
│   └── types/               # Shared API/domain types
├── tests/
├── .env.example
└── package.json
```

## Accessibility and privacy

- Semantic headings, labels, focusable controls and responsive navigation.
- Reduced-motion preference is respected.
- No identity-document uploads or sensitive identity-number fields.
- No passwords, OTPs, UPI PINs or banking credentials requested.
- Chat content is kept in the active page's React state only; it is not persisted to local storage.
- External source links accept HTTPS only and open with `noopener noreferrer`.

## Scope boundaries and known integration work

- Django backend implementation, database, migrations and admin console are outside this frontend deliverable.
- No real government records were verified or seeded.
- No Sarvam SDK or API call is made from the browser; provider integration belongs in Django.
- No microphone capture, speech synthesis, OCR, document verification, WhatsApp integration, citizen account system or live application tracking is implemented.
- The API contract must be reconciled with the existing Django OpenAPI schema before declaring live integration complete.
