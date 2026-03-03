from collections import defaultdict
from datetime import datetime, timedelta

class EventCorrelator:
    def __init__(self, correlation_window_seconds=300):
        self.correlation_window = timedelta(seconds=correlation_window_seconds)
        self.alert_history = defaultdict(list)

    def process_alert(self, alert):

        ip = alert["ip"]
        now = datetime.now()

        self.alert_history[ip].append((alert, now))

        # Removendo os alertas antigos
        self.alert_history[ip] = [
            (a, t) for (a, t) in self.alert_history[ip]
            if now - t <= self.correlation_window
        ]

        # Exemplo simples:
        # Se 2 alertas do mesmo IP dentro da janela → escalar
        if len(self.alert_history[ip]) >= 2:
            return {
                "type": "MULTI_STAGE_ATTACK_SUSPECTED",
                "ip": ip,
                "alerts_count": len(self.alert_history[ip])
            }

        return None
