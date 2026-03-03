from datetime import datetime
import json

class AlertManager:
    def __init__(self, log_file):
        self.log_file = log_file

    def handle(self, alert):
        if alert is None:
            return

        message = self._format(alert)
        print(message)
        self._write(message)

    def _format(self, alert):
        timestamp = datetime.utcnow().isoformat()
        return f"{timestamp} | {json.dumps(alert)}"

    def _write(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
