import json
from datetime import datetime

class AlertManager:
    def __init__(self, log_file):
        self.log_file = log_file

    def handle(self, alert):
        if alert is None:
            return

        message = self._format(alert)
        print(message)
        self._write(alert)  # passa o alerta, não a string formatada

    def _format(self, alert):
        timestamp = datetime.utcnow().isoformat()
        return f"{timestamp} | {json.dumps(alert)}"

    def _write(self, alert):
        """
        Grava cada alerta como uma linha JSON no arquivo.
        """
        with open(self.log_file, "a") as f:
            json.dump(alert, f)
            f.write("\n")
