"""Privacy-minimized aggregate telemetry; never export protected customer data."""
from __future__ import annotations

import json
import math
import os
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlsplit
from uuid import UUID, uuid4

PROJECT_ID = 'wealth_protection'
EVENT_TYPES = {
    'customer.subscription.changed', 'customer.lifecycle.changed',
    'monitoring.run.completed', 'monitoring.run.failed', 'risk.alert.created',
    'risk.alert.resolved', 'human_review.created', 'human_review.resolved',
    'agent.execution.failed', 'integration.health.changed',
    'billing.event.received', 'cost.recorded',
}
COUNTS = {
    'active_customers', 'trial_customers', 'new_subscriptions', 'cancellations',
    'monitoring_events', 'critical_alerts', 'high_alerts', 'medium_alerts',
    'unresolved_critical_alerts', 'unresolved_high_alerts', 'human_review_queue',
}
AMOUNTS = {
    'mrr', 'arr', 'contribution_revenue', 'contribution_cost', 'ai_cost',
    'api_cost', 'provider_cost', 'infrastructure_cost', 'support_cost', 'human_review_cost',
}
RATES = {'churn_rate', 'conversion_rate', 'agent_success_rate', 'agent_failure_rate'}
HEALTH_KEYS = {'monitoring_health', 'integration_health', 'provider_health'}
HEALTH_STATES = {'healthy', 'degraded', 'stale', 'blocked', 'unknown'}
SEVERITIES = {'critical', 'high', 'medium', 'low', 'informational'}
CHANNELS = {'organic', 'referral', 'direct', 'email', 'social', 'paid', 'other', 'unknown'}
ALLOWED_KEYS = COUNTS | AMOUNTS | RATES | HEALTH_KEYS | {
    'contribution_margin', 'acquisition_source', 'alerts_by_severity',
    'last_successful_monitoring_run', 'data_freshness',
}


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _count(value):
    return type(value) is int and value >= 0


def _safe_value(key, value):
    if value is None:
        return None  # Unavailable is distinct from zero.
    valid = False
    if key in COUNTS:
        valid = _count(value)
    elif key in AMOUNTS or key == 'data_freshness':
        valid = _number(value) and value >= 0
    elif key in RATES:
        valid = _number(value) and 0 <= value <= 1
    elif key == 'contribution_margin':
        valid = _number(value)
    elif key in HEALTH_KEYS:
        valid = isinstance(value, str) and value in HEALTH_STATES
    elif key == 'acquisition_source':
        valid = isinstance(value, str) and value in CHANNELS
    elif key == 'alerts_by_severity':
        valid = (isinstance(value, dict) and set(value) <= SEVERITIES
                 and all(_count(count) for count in value.values()))
        if valid:
            return dict(value)
    elif key == 'last_successful_monitoring_run' and isinstance(value, str):
        try:
            timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
            valid = timestamp.tzinfo is not None and timestamp <= datetime.now(timezone.utc)
        except ValueError:
            pass
    if not valid:
        raise ValueError('Invalid aggregate telemetry value for ' + key)
    return value


def build_event(event_type: str, payload: dict, *, event_id: str | None = None) -> dict:
    if event_type not in EVENT_TYPES:
        raise ValueError('Unknown portfolio event type')
    if not isinstance(payload, dict):
        raise ValueError('Telemetry payload must be an object')
    safe = {key: _safe_value(key, value) for key, value in payload.items() if key in ALLOWED_KEYS}
    if not safe:
        raise ValueError('Telemetry requires at least one aggregate metric')
    ident = str(UUID(event_id)) if event_id is not None else str(uuid4())
    return {'schema_version': '1.0', 'event_id': ident, 'project_id': PROJECT_ID,
            'event_type': event_type, 'occurred_at': datetime.now(timezone.utc).isoformat(), 'payload': safe}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Do not forward bearer credentials to a redirected endpoint.


def emit(event_type: str, payload: dict, *, event_id: str | None = None) -> bool:
    url = os.getenv('JARVIS_INGEST_URL')
    token = os.getenv('JARVIS_INGEST_TOKEN')
    if not url or not token or any(char.isspace() for char in token):
        return False
    try:
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
            return False
        parsed.port  # Reject malformed ports before attempting a request.
    except ValueError:
        return False
    event = build_event(event_type, payload, event_id=event_id)
    request = urllib.request.Request(
        url, data=json.dumps(event, allow_nan=False).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}, method='POST')
    try:
        with urllib.request.build_opener(_NoRedirect()).open(request, timeout=5) as response:
            return 200 <= response.status < 300
    except (OSError, TimeoutError):
        return False
