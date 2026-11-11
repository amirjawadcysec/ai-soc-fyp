"""Week-1 demo: dummy events flow through all six agents."""
from orchestrator import run_pipeline

EVENTS = [
    {"timestamp": "2026-10-14T10:00:01", "src_ip": "192.168.56.10", "dst_host": "victim-01",
     "failed_logins": 12, "service": "ssh"},
    {"timestamp": "2026-10-14T10:05:30", "src_ip": "192.168.56.10", "dst_host": "victim-01",
     "ports_scanned": 150},
    {"timestamp": "2026-10-14T10:09:12", "src_ip": "192.168.56.11", "dst_host": "victim-01",
     "request": "GET /login?id=' OR 1=1 --"},
    {"timestamp": "2026-10-14T10:12:00", "src_ip": "192.168.56.20", "dst_host": "victim-01",
     "request": "GET /index.html"},
]

for ev in EVENTS:
    inc = run_pipeline(ev, approve_high_impact=False)
    print(f"\n=== {inc.incident_id} | stage: {inc.stage} ===")
    for step in inc.audit:
        print(f"  [{step['agent']:<13}] {step['message']}")
    if inc.summary:
        print("  SUMMARY:", inc.summary)
