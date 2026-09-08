# Digital Estate Protection — Build Plan

## Execution mode

Autonomous implementation is authorized within the repository and product boundaries. Build in small, auditable increments. Do not fabricate integrations, monitoring results, credentials, or production readiness.

## Phase 1 — Foundation

- Establish application/service structure.
- Establish configuration and environment contract.
- Establish database schema and migrations.
- Establish typed domain models for customers, monitored assets, sources, events, risk assessments, alerts, tasks, reports, subscriptions, notifications, agent executions, consents, and audit events.
- Establish tenant isolation and authorization primitives.
- Establish automated tests and CI checks.

## Phase 2 — Secure customer foundation

- Authentication and session management.
- Email verification and password recovery.
- MFA-ready architecture.
- Progressive onboarding and consent.
- Customer/family roles and permissions.
- Protected profile and monitored-asset management.

## Phase 3 — Monitoring pipeline

- Provider abstraction.
- Select one legitimate, commercially usable monitoring source for the first live integration.
- Ingest -> normalize -> deduplicate -> persist -> analyze.
- Record source, observed timestamp, ingestion timestamp, evidence, and confidence.
- Handle retries, rate limits, provider failures, and stale data honestly.

## Phase 4 — Risk intelligence

- Deterministic risk taxonomy.
- Explainable Digital Estate Score.
- AI risk-analysis agent with structured output.
- Confidence thresholds and human-review escalation.
- Prompt-injection and untrusted-source safeguards.

## Phase 5 — Alerts and customer experience

- Alert lifecycle.
- Severity: Critical, High, Medium, Low, Informational.
- Evidence-backed explanations.
- Recommended actions.
- Configurable notification preferences.
- Overview, Alerts, Identity, Domains, Family, Tasks, Reports, Settings.

## Phase 6 — Automation and reporting

Agents:

1. Monitoring
2. Risk Analysis
3. Research
4. Reporting
5. Quality Control
6. Concierge/Intake

No irreversible external actions without explicit authorization. Add monthly premium reports and operational summaries.

## Phase 7 — Commercial layer

- Subscription plans configurable around Essential, Family, and Private Estate tiers.
- Checkout, subscription lifecycle, billing history, signed webhooks, idempotency.
- Free Digital Exposure Assessment using limited information.
- Referral attribution infrastructure.

## Phase 8 — Operations and JARVIS telemetry

Expose minimum necessary operational telemetry to JARVIS:

- active customers
- MRR/ARR
- new/cancelled subscriptions
- churn and conversion
- contribution margin inputs
- monitoring health
- alert volumes by severity
- unresolved critical/high alerts
- agent execution health
- API/provider cost
- AI cost
- infrastructure cost
- human-review queue
- data freshness

Do not export protected customer content or unnecessary personal data into JARVIS.

## Phase 9 — Security and production readiness

Test and remediate:

- authentication bypass
- authorization/IDOR
- cross-tenant access
- privilege escalation
- injection
- XSS/CSRF where applicable
- secret exposure
- unsafe file handling
- SSRF where applicable
- webhook abuse
- prompt injection
- data leakage
- rate-limit bypass
- session flaws
- agent permission escalation

Production readiness requires passing functional, security, data-integrity, integration, billing, notification, AI, accessibility, and performance checks.

## Definition of done for MVP

A real user can securely subscribe, onboard, authorize monitoring, receive at least one real monitoring signal through a legitimate integration, see an evidence-backed risk assessment, receive an actionable alert, view the event in the dashboard, receive a report, and be represented in JARVIS through privacy-minimized operational telemetry.

Nothing is considered complete merely because a UI exists. Every production feature must be backed by real data paths, validation, error handling, authorization, tests, and auditability.
