# JARVIS Telemetry Contract

JARVIS is the portfolio command center. This product remains the source of truth for protected customer operations.

## Exported metrics

- active_customers
- trial_customers
- mrr
- arr
- new_subscriptions
- cancellations
- churn_rate
- conversion_rate
- contribution_revenue
- contribution_cost
- contribution_margin
- ai_cost
- provider_cost
- infrastructure_cost
- human_review_cost
- monitoring_events
- alerts_by_severity
- unresolved_critical_alerts
- unresolved_high_alerts
- agent_success_rate
- agent_failure_rate
- provider_health
- data_freshness

## Export rules

1. Aggregate by default.
2. Never export passwords, secrets, authentication tokens, raw credentials, or unnecessary customer content.
3. Customer-identifying data should not be required for portfolio dashboards.
4. Preserve source timestamps and metric definitions.
5. Mark estimated/unavailable values explicitly.
6. JARVIS must not directly execute protected-domain operations.
7. Any action initiated from JARVIS must pass through this system's own authorization and safety controls.

## Health states

`healthy`, `degraded`, `stale`, `blocked`, `unknown`.

Unknown is preferable to fabricated real-time status.

## Adapter value contract

The adapter validates values as well as metric names. Unknown keys are excluded; an invalid value under a known key rejects the event before transmission.

- Counts are nonnegative integers; booleans are not counts.
- Revenue/cost amounts are finite nonnegative numbers in one agreed reporting currency. Currency conversion must occur before aggregation.
- Churn, conversion, and agent success/failure rates are fractions from 0 to 1. Contribution margin is a finite fraction and may be negative.
- `data_freshness` is a nonnegative age in seconds.
- `alerts_by_severity` contains only `critical`, `high`, `medium`, `low`, and `informational` integer counts.
- `provider_health`, `monitoring_health`, and `integration_health` use the aggregate health states above, without provider names or upstream response bodies.
- `last_successful_monitoring_run` is a timezone-aware source timestamp, never a fabricated current timestamp.
- Optional `acquisition_source` uses only `organic`, `referral`, `direct`, `email`, `social`, `paid`, `other`, or `unknown`; it never contains a customer identifier or URL.
- Any metric may be `null` when unavailable. This does not mean zero.

Event names use the twelve normalized events in JARVIS's integration document. Callers may supply a UUID `event_id` and must reuse it when retrying the same observation. The sender requires both an HTTPS `JARVIS_INGEST_URL` and `JARVIS_INGEST_TOKEN`, refuses redirects, and returns `False` when unconfigured or delivery fails. It does not retry or claim durable delivery.

## Verified implementation status

As of the October 16, 2026 repository review, this repository contains product/domain plans and an isolated telemetry adapter with local contract tests. It does not contain an application, database, authentication, monitoring integration, billing, or customer dashboard. JARVIS has no implemented production ingest endpoint for this adapter in the reviewed code. End-to-end telemetry delivery and product readiness are therefore unverified.
