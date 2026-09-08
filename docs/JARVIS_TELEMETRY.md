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
