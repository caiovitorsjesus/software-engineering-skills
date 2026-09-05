# Frontend Engineering Concerns

> Covers: framework-neutral engineering concerns for web user interfaces — state management, rendering and performance, accessibility, forms and validation, error/loading states, security hooks
> Retrieved: 2026-09-04
> Sources: ISO/IEC 25010:2023 interaction capability vocabulary (references/quality-model.md); OWASP ASVS 5.0 chapter V3 Web Frontend Security (references/security-framework-map.md); this system's recommendations
> Evidence: STANDARD, RECOMMENDATION

Load when: implementing or reviewing a web UI story. Apply within the project's framework conventions (`references/stack-adaptation.md`).

## 1. State management
- Classify state: server data (cache with staleness policy) · UI state (local) · URL state (shareable, back-button) · form state · session/auth state. Keep each in the simplest home; avoid duplicating server data in global stores.
- Single source of truth per piece of state; derive, do not copy.
- Async data has four states: idle, loading, success, error — render all four.
- Optimistic updates only with rollback on failure.

## 2. Rendering and performance
- Measure before optimizing: initial load, interaction latency, list rendering.
- Paginate or virtualize large lists; debounce high-frequency inputs; memoize expensive derivations.
- Code-split by route/feature; lazy-load heavy components; compress and size images.
- Avoid layout thrash and unnecessary re-renders (stable references, keyed lists).

## 3. Accessibility and interaction capability
- Semantic HTML first; ARIA only to fill gaps. Keyboard operability for every interactive element; visible focus.
- Labels for every input; error messages associated with fields; colour never the only signal.
- Target the WCAG level set in `REQ-N` (interaction capability › inclusivity); run automated a11y checks in CI and a manual keyboard pass before release.
- Text scalable; contrast sufficient; motion reducible.

## 4. Forms and validation
- Validate on the client for feedback, on the server for truth; same rules from the API contract.
- Preserve user input on error; explain how to fix; disable double submit; idempotent submission where retries are possible.

## 5. Errors, loading, empty states
- Every view defines loading, empty, error and partial-failure presentations.
- Error boundary at route level; user-safe messages; log with correlation id for support.

## 6. Security hooks (ASVS V3)
- Escape/encode output by default (framework templating); never inject raw HTML from untrusted data.
- Tokens: prefer HttpOnly secure cookies for sessions; if tokens are stored client-side, understand exposure and keep lifetimes short.
- CSP, frame protections, and CSRF defenses configured with the backend.
- No secrets in the bundle; environment-specific config injected at build/deploy, not committed.

## 7. Testing hooks
- Unit tests for pure logic and state reducers; component tests for behaviour with a testing-library approach (query by role/label); few e2e journeys; visual regression optional.
- Accessibility assertions in component tests where feasible.

## 8. Observability
- Client error reporting with release version; performance metrics (navigation, interaction) if REQ-N demands; respect privacy (no PII in telemetry).
