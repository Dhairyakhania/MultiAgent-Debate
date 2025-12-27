import json
from datetime import datetime

def log_event(log_path, event, payload):
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "payload": payload
        }) + "\n")
