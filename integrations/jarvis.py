"""JARVIS telemetry adapter for Digital Estate Protection.

Only portfolio telemetry is emitted. Customer-sensitive findings stay inside
this protected domain and are never copied into JARVIS by this adapter.
"""
from __future__ import annotations
import json, os, urllib.request
from datetime import datetime, timezone
PROJECT_ID="wealth_protection"
ALLOWED_KEYS={"mrr","arr","active_customers","trial_customers","churn_rate","conversion_rate","acquisition_source","contribution_margin","ai_cost","api_cost","infrastructure_cost","support_cost","monitoring_health","critical_alerts","high_alerts","medium_alerts","human_review_queue","last_successful_monitoring_run","integration_health","data_freshness"}
def build_event(event_type:str,payload:dict)->dict:
    safe={k:v for k,v in payload.items() if k in ALLOWED_KEYS}; now=datetime.now(timezone.utc).isoformat(); return {"schema_version":"1.0","event_id":f"{PROJECT_ID}:{now}","project_id":PROJECT_ID,"event_type":event_type,"occurred_at":now,"payload":safe}
def emit(event_type:str,payload:dict)->bool:
    url=os.getenv("JARVIS_INGEST_URL")
    if not url:return False
    req=urllib.request.Request(url,data=json.dumps(build_event(event_type,payload)).encode(),headers={"Content-Type":"application/json","Authorization":f"Bearer {os.getenv('JARVIS_INGEST_TOKEN','')}"},method="POST")
    with urllib.request.urlopen(req,timeout=5) as response:return 200<=response.status<300
