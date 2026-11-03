# SAARTHI — Frontend Project Handoff

**Scope:** New frontend project only. The existing/planned Django backend is a separate workstream and has not been created or modified in this deliverable.

## 1. Product goal

SAARTHI is an independent, multilingual government-service navigation platform. Its user journey is:

**Describe a need → Discover a service → Understand the service → Review preliminary eligibility → Prepare documents → Follow available application guidance → Continue on the official government portal.**

Initial geography: Maharashtra, with a Pune pilot. Initial UI languages: English (`en`), Hindi (`hi`) and Marathi (`mr`).

SAARTHI must not present itself as a government authority, guarantee eligibility or approval, invent service requirements, or claim to submit an application.

## 2. What is implemented

| Area | Implementation | Status |
|---|---|---|
| Homepage | Product positioning, natural-language search, example prompts, journey overview, CTA and disclaimer | Implemented |
| Service directory | Search, service cards, loading/empty/error states | Implemented |
| Service details | Description, department/jurisdiction facts, notes, source list and next-step links | Implemented |
| Eligibility | Dynamic question renderer for boolean, single-choice, number and text; required-field validation; result status labels | Implemented; backend rules required |
| Documents | Backend-provided list and local checklist state | Implemented; backend content required |
| Application guide | Ordered backend steps, safe external HTTPS links, source list | Implemented; backend content required |
| Assistant | Text chat, session ID, source citations, related-service links, warnings and retry/error feedback | Implemented; backend knowledge API required |
| About | Independence, official-source primacy, preliminary guidance and privacy messaging | Implemented |
| Localization | Central dictionaries, language selector and persisted language preference | Core labels implemented; not every explanatory sentence on every page is translated yet |
| API layer | Centralized typed fetch client, endpoint builder, envelope/error handling | Implemented against proposed contract; Django OpenAPI reconciliation pending |
| Demo mode | Persistent demo banner and illustrative service records; no invented official links or rules | Implemented |
| Accessibility | Semantic controls, labels, focusable navigation, reduced-motion CSS | Baseline implemented; formal audit pending |
| Responsive design | Desktop/tablet/mobile layout with narrow-screen breakpoints | Implemented in CSS; browser/device verification pending |
| Tests | API envelope/error tests, language dictionary smoke test, service card render test | Written; not run because npm registry could not be reached in this environment |

## 3. Routes

| Route | What the user can do |
|---|---|
| `/` | Understand SAARTHI, search for a service, browse sample/backend-supplied featured services |
| `/services` | Browse and search the service directory |
| `/services/[slug]` | Read the available service summary and open the next journey step |
| `/services/[slug]/eligibility` | Answer backend-defined questions and view a cautious preliminary result |
| `/services/[slug]/documents` | Mark checklist items as prepared locally; no uploads or document verification |
| `/services/[slug]/guide` | Read ordered instructions and open validated official HTTPS links supplied by backend |
| `/assistant` | Ask a text question and see answer, source, warning and related-service data returned by backend |
| `/about` | Read purpose, limitations, source and privacy explanation |
| not-found | Friendly invalid-route fallback |

## 4. Frontend architecture

```text
SAARTHI/
├── PROJECT_HANDOFF.md
└── frontend/
    ├── public/                 # Static assets (brand mark)
    ├── src/
    │   ├── app/                # Next.js App Router routes and global styles
    │   ├── components/         # Header/footer, cards, search, shared states
    │   ├── context/            # Language state and persistence
    │   ├── data/demo/          # Explicitly illustrative data only
    │   ├── i18n/               # English, Hindi and Marathi dictionaries
    │   ├── lib/api/            # Central API client and endpoint-specific modules
    │   ├── lib/                # Config and URL/date utilities
    │   └── types/              # Shared service, source, eligibility, document, guide types
    ├── tests/                  # Vitest tests
    ├── .env.example
    ├── .gitignore
    ├── package.json
    └── README.md
```

### API request flow

Page/component → endpoint module (`src/lib/api/*.ts`) → endpoint map (`endpoints.ts`) → `apiRequest<T>` (`client.ts`) → Django base URL from environment.

The client unwraps the common `{ success, data, meta }` envelope and converts common error envelopes to `ApiError`. Pages do not assemble API URLs directly.

## 5. API routes expected by the frontend

All paths are relative to `NEXT_PUBLIC_API_BASE_URL` (which already includes `/api/v1`).

| Method | Path | Used by |
|---|---|---|
| GET | `/health` | Health check / integration diagnostics |
| GET | `/services` | Home featured services and directory |
| GET | `/services/{slug}` | Service detail |
| POST | `/search` | Service search |
| GET | `/services/{slug}/documents` | Document checklist |
| GET | `/services/{slug}/eligibility/questions` | Eligibility form schema |
| POST | `/services/{slug}/eligibility/evaluate` | Preliminary eligibility evaluation |
| GET | `/services/{slug}/steps` | Application guide |
| POST | `/assistant/chat` | Assistant messages |
| POST | `/feedback` | Typed API helper available; feedback UI is not part of current page scope |

**Important integration dependency:** The source README labels request/response examples as proposed shapes. The Django OpenAPI schema was not supplied in this session. Before connecting live mode, compare the real Django schemas with `src/types/index.ts` and the request modules. Do not assume the FastAPI example implementation is the Django contract.

## 6. Environment configuration

Create `frontend/.env.local` from `.env.example`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DEMO_MODE=true
```

Use `NEXT_PUBLIC_DEMO_MODE=true` to explore the UI without a backend. To use Django, set it to `false` and set the actual Django API base URL. Live mode intentionally does not fall back to demo data when a backend request fails.

No Sarvam key is included. No secret may be stored in a `NEXT_PUBLIC_*` variable. Sarvam API access must remain in the Django backend, and the frontend must call only the backend's approved assistant endpoint.

## 7. Run commands

```bash
cd SAARTHI/frontend
npm install
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

Windows PowerShell:

```powershell
cd SAARTHI\frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Quality checks after dependencies install:

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

## 8. Current verification and limitations

- Node.js and npm are present in the build environment.
- `npm install` was attempted but could not download packages because DNS/network access to `registry.npmjs.org` failed (`EAI_AGAIN`). Therefore `node_modules`, `package-lock.json`, Next build output and browser screenshots could not be generated here.
- A global TypeScript check was attempted but cannot be conclusive without the React/Next dependencies and type declarations.
- Source files were inspected for unresolved placeholder throws; none remain in the API client.
- The frontend has not been tested against a running Django backend because no Django project or OpenAPI schema was provided.
- The included service names are illustrative demo records, not verified government content. No eligibility criteria, fees, processing times, document requirements or real government links are invented.
- The UI's core language controls and common navigation labels are translated, but a full professional translation pass across all page copy remains a follow-up item.
- Visual responsiveness is implemented with CSS breakpoints; a real browser QA pass at 360px, 390px, tablet and desktop remains required after dependencies install.

## 9. Next integration sequence

1. Install dependencies and run the frontend in demo mode.
2. Start the actual Django backend and share its OpenAPI JSON or `/docs` schema.
3. Reconcile request/response types and endpoint paths with Django; update only the API layer/types.
4. Verify health, service list, search and service detail.
5. Verify eligibility question schema and all four allowed result statuses.
6. Verify documents and application steps with source metadata.
7. Verify assistant answer, session ID, source links, related services and warnings.
8. Complete translations and responsive/accessibility QA.
9. Run lint, typecheck, tests, production build and end-to-end journey checks.

## 10. Out of scope

Django/backend code, database/schema/migrations, admin CMS, Sarvam SDK/provider code, voice capture, speech playback, OCR, document upload or authenticity checks, WhatsApp integration, citizen authentication, application submission and live application tracking are intentionally not implemented in this frontend-only project.
