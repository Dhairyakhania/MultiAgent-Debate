import json
from datetime import datetime
from pathlib import Path

class DebateLogger:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, data: dict):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
