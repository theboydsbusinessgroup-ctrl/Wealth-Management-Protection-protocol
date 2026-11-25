import json
import unittest
from urllib.request import Request
from unittest.mock import Mock, patch
from uuid import uuid4

from integrations.jarvis import build_event, emit, _NoRedirect


class TelemetryTests(unittest.TestCase):
    def test_documented_metrics_are_preserved(self):
        payload = {'new_subscriptions': 2, 'provider_cost': 1.25, 'alerts_by_severity': {'high': 3},
                   'provider_health': 'unknown', 'mrr': None, 'agent_success_rate': 0.9}
        self.assertEqual(build_event('cost.recorded', payload)['payload'], payload)

    def test_unknown_customer_fields_are_excluded(self):
        event = build_event('cost.recorded', {'mrr': 10, 'customer': {'email': 'private-marker'}})
        self.assertNotIn('private-marker', json.dumps(event))

    def test_allowed_keys_cannot_carry_private_content(self):
        for payload in ({'mrr': {'customer': 'private-marker'}}, {'monitoring_health': 'private-marker'},
                        {'acquisition_source': 'private-marker'}, {'alerts_by_severity': {'customer': 1}}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                build_event('cost.recorded', payload)

    def test_invalid_numeric_metrics_fail_closed(self):
        for payload in ({'mrr': float('nan')}, {'mrr': float('inf')}, {'active_customers': True},
                        {'active_customers': -1}, {'conversion_rate': 2}, {'provider_cost': -1}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                build_event('cost.recorded', payload)

    def test_retry_can_reuse_event_identity(self):
        ident = str(uuid4())
        self.assertEqual(build_event('cost.recorded', {'mrr': 1}, event_id=ident)['event_id'], ident)

    def test_unknown_event_or_empty_payload_is_rejected(self):
        for event_type, payload in [('private-marker', {'mrr': 1}), ('cost.recorded', {'customer': 'private-marker'})]:
            with self.subTest(event=event_type), self.assertRaises(ValueError):
                build_event(event_type, payload)

    def test_timestamp_requires_timezone(self):
        with self.assertRaises(ValueError):
            build_event('monitoring.run.completed', {'last_successful_monitoring_run': '2026-01-01T10:00:00'})

    @patch('integrations.jarvis.urllib.request.build_opener')
    def test_unconfigured_or_insecure_transport_never_sends(self, opener):
        for env in ({}, {'JARVIS_INGEST_URL': 'https://example.test'},
                    {'JARVIS_INGEST_URL': 'http://example.test', 'JARVIS_INGEST_TOKEN': 'test'},
                    {'JARVIS_INGEST_URL': 'https://user:pass@example.test', 'JARVIS_INGEST_TOKEN': 'test'}):
            with self.subTest(env=env), patch.dict('os.environ', env, clear=True):
                self.assertFalse(emit('cost.recorded', {'mrr': 1}))
        opener.assert_not_called()

    @patch.dict('os.environ', {'JARVIS_INGEST_URL': 'https://example.test/ingest', 'JARVIS_INGEST_TOKEN': 'test'}, clear=True)
    @patch('integrations.jarvis.urllib.request.build_opener')
    def test_authenticated_https_send_and_failure_are_bounded(self, opener):
        response = Mock(status=202)
        opener.return_value.open.return_value.__enter__ = Mock(return_value=response)
        opener.return_value.open.return_value.__exit__ = Mock(return_value=False)
        self.assertTrue(emit('cost.recorded', {'mrr': 1}))
        self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'], 5)
        opener.return_value.open.side_effect = OSError('unavailable')
        self.assertFalse(emit('cost.recorded', {'mrr': 1}))

    def test_redirects_do_not_forward_credentials(self):
        handler = _NoRedirect()
        handler.parent = Mock()
        request = Request('https://example.test/ingest', data=b'{}', headers={'Authorization': 'Bearer private'})
        result = handler.http_error_302(request, Mock(), 302, 'Found', {'location': 'https://other.test/ingest'})
        self.assertIsNone(result)
        handler.parent.open.assert_not_called()


if __name__ == '__main__':
    unittest.main()
