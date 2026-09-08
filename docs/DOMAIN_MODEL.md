# Domain Model

## Tenant boundary

Every protected customer record is scoped to an organization/estate tenant. Authorization must be evaluated server-side for every read/write path.

## Core entities

- User
- Organization/Estate
- FamilyMember
- Subscription
- Consent
- MonitoredIdentity
- MonitoredEmail
- MonitoredPhone
- MonitoredDomain
- MonitoringSource
- MonitoringEvent
- RiskAssessment
- Alert
- Recommendation
- Task
- Report
- Notification
- AgentExecution
- AuditEvent
- SecurityEvent
- Referral

## Event lifecycle

`observed -> normalized -> deduplicated -> risk_assessed -> prioritized -> alerted -> acknowledged -> resolved/closed`

All transitions should be timestamped and auditable.

## Risk assessment

Risk assessments must preserve:

- event type
- severity
- confidence
- explanation
- evidence references
- recommended action
- review requirement
- model/engine version
- created/updated timestamps

AI output is advisory and must not silently override deterministic policy controls.

## Privacy rule

Store the minimum data required to deliver the subscribed monitoring capability. Separate customer-facing protected content from portfolio-level telemetry. JARVIS should receive aggregate operational/business metrics rather than raw personal data whenever possible.
