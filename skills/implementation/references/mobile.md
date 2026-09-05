# Mobile Engineering Concerns

> Covers: platform-neutral engineering concerns for mobile applications — offline-first and synchronization, permissions, background work, secure storage, app lifecycle, connectivity, release channels and API compatibility
> Retrieved: 2026-09-04
> Sources: ISO/IEC 25010:2023 reliability and interaction capability vocabulary (references/quality-model.md); OWASP ASVS 5.0 chapters V6–V9, V11–V12, V14 (references/security-framework-map.md); distributed-systems triggers in references/cs-foundations.md §3–4; this system's recommendations
> Evidence: STANDARD, RECOMMENDATION

Load when: implementing or reviewing a mobile story (Flutter, React Native, Swift, Kotlin or other). Apply within the project's framework conventions.

## 1. Offline-first and synchronization
- Decide per feature: online-only, read-cache, or full offline write. Record in the story.
- Local store as the UI's source of truth; a sync layer reconciles with the API.
- Conflict policy explicit per entity: last-write-wins, server-wins, merge by field, or manual resolution; version/updated-at fields in the contract.
- Outbox queue for offline writes: durable, ordered where required, idempotency keys, retry with backoff, dead-letter on permanent failure with user-visible status.
- Sync triggers: app foreground, connectivity regained, periodic background; show sync state.
- Test with airplane mode, flaky network, clock skew, and reinstall scenarios.

## 2. Permissions
- Request at the moment of need with an explanation; degrade gracefully when denied; never block the whole app for optional permissions.
- Map each permission to the REQ that needs it; remove unused ones (store review and privacy).

## 3. Background work and lifecycle
- The OS may suspend or kill the app at any time: persist state on transitions; make operations resumable.
- Background execution is limited and platform-specific; schedule deferrable work through the platform scheduler; keep foreground-critical work out of background tasks.
- Push notifications: token lifecycle, opt-in, deep links, idempotent handling of duplicates.

## 4. Secure storage and identity (ASVS V6–V9, V11, V14)
- Secrets and tokens in the platform keystore/keychain, never in plain preferences or files.
- Short-lived access tokens with refresh; revoke on logout; biometric gate for sensitive actions where required.
- Certificate validation on; pinning only with a rotation plan.
- No sensitive data in logs, screenshots (secure flags where needed), backups (exclude when required), or analytics.
- Clipboard and deep-link inputs are untrusted.

## 5. Connectivity and API usage
- Timeouts, retries (idempotent only) with backoff and jitter; batch requests; compress payloads; paginate.
- Handle API version skew: the app in the field may be old for months — additive API changes only, feature flags server-side, minimum-supported-version check with a graceful update prompt.

## 6. Data and storage
- Local schema migrations versioned and tested (upgrade path from every supported version).
- Storage quotas and cleanup policy; large media cached with bounds.

## 7. Interaction capability
- Platform conventions (navigation, gestures); accessibility services (screen readers, dynamic type, contrast); localization and RTL if in scope; responsive to screen sizes and orientation.

## 8. Release and operations
- Build flavours per environment; signed builds; crash and performance monitoring with release version; staged rollout and rollback plan (server-side kill switches for risky features).
- Store review lead time in the deployment plan; privacy declarations match data usage.

## 9. Testing hooks
- Unit tests for logic and sync/conflict rules; widget/component tests; integration tests on emulators/devices for critical journeys; offline scenario tests; contract tests against the API.
